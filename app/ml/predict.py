from dataclasses import dataclass
from pathlib import Path
import joblib
import json
import pandas as pd
from fastapi.encoders import jsonable_encoder

from ..core.schemas import ModelInput, PredictionOutput

from . import encoders

import json

@dataclass
class AIModel:
    MODEL_STORE_DIR: Path
    
    model = None
    
    def __post_init__(self):
        if self.MODEL_STORE_DIR.exists():
            MODEL_REGISTRY_PATH = self.MODEL_STORE_DIR/"model_registry.json"
            if MODEL_REGISTRY_PATH.name.endswith("json"):
                model_registry = json.loads(MODEL_REGISTRY_PATH.read_text())
                print(model_registry)
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

        if not isinstance(payload, list):
            payload = [payload]

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
            results = encoders.encode_to_json(prediction)
        
        return results
        