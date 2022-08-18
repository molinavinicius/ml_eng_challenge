from dataclasses import dataclass
from pathlib import Path
import joblib
import json
import os
import pandas as pd
import numpy as np
from fastapi.encoders import jsonable_encoder
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error

from ..core.schemas import ModelInput, Evaluation, EvaluationOutput
from typing import Union, List

from . import encoders

import json

@dataclass
class AIModel:
    MODEL_STORE_DIR: Path
    
    model = None
    
    def __post_init__(self):
        if self.MODEL_STORE_DIR.exists():
            # models = next(os.walk(self.MODEL_STORE_DIR))[1]
            # print('available models:',models)
            MODEL_REGISTRY_PATH = self.MODEL_STORE_DIR/"model_registry.json"
            if MODEL_REGISTRY_PATH.name.endswith("json"):
                model_registry = json.loads(MODEL_REGISTRY_PATH.read_text())
                MODEL_DIR = self.MODEL_STORE_DIR/model_registry['current']
                if MODEL_DIR.exists():
                    self.model = joblib.load(MODEL_DIR/'model.pkl')
                
    def get_model(self):
        if not self.model:
            raise NotImplementedError("Model not implemented")
        return self.model
    
    def get_metadata(self):
        if not self.metadata:
            raise NotImplementedError("Metadata not implemented")
        return self.metadata
    
    def __prepare_payload_for_input(self, payload:ModelInput):
        
        payload = np.array(payload).flatten().tolist()

        for idx, elem in enumerate(payload):
            elem = jsonable_encoder(elem)
            result = {}
            for k,v in elem.items():
                if isinstance(v, dict):
                    result = {**result, **v}
                else:
                    result = {**result, k: v}
            payload[idx] = result
        df = pd.DataFrame(payload)
        return df 
        
    def predict(self, payload:ModelInput, encode_to_json=True):
        model = self.get_model()
        model_input = self.__prepare_payload_for_input(payload)
        prediction = model.predict(model_input)

        if encode_to_json:
            prediction = encoders.encode_to_json(prediction)
        
        return prediction
    
    def evaluate(self, eval:Union[Evaluation, List[Evaluation]]):
        evals = np.array(eval).flatten().tolist()
        payload = [e.payload for e in evals]
        real_value = [e.real for e in evals]
        predicted = self.predict(payload)
        
        metrics = {
            "rmse": mean_squared_error(real_value, predicted),
            'rmae': mean_absolute_error(real_value, predicted),
        }
        if len(predicted) >= 2:
            metrics["r2"] = r2_score(real_value, predicted)
            
        result = EvaluationOutput(
            real = real_value,
            predicted = predicted,
            metrics = metrics
        )

        return result
        
        
        