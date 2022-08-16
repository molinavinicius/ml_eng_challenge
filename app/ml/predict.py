from dataclasses import dataclass
from pathlib import Path
import joblib
import json
import pandas as pd

from ..core.schemas import ModelInput, Payload, PredictionOutput

@dataclass
class AIModel:
    model_path: Path
    metadata_path: Path
    
    model = None
    metadata = None
    
    def __post_init__(self):
        if self.model_path.exists():
            self.model = joblib.load(self.model_path)
        
        if self.metadata_path.exists():
            if self.metadata_path.name.endswith("json"):
                self.metadata = json.loads(self.metadata_path.read_text())
                
    def get_model(self):
        if not self.model:
            raise NotImplementedError("Model not implemented")
        return self.model
    
    def get_metadata(self):
        if not self.metadata:
            raise NotImplementedError("Metadata not implemented")
        return self.metadata
    
    def __prepare_payload_for_input(self, payload:ModelInput):
        if isinstance(payload, Payload):
            payload = [payload]
        return pd.DataFrame(payload)
        
    def predict(self, payload:ModelInput):
        model = self.get_model()
        model_input = self.__prepare_payload_for_input(payload)
        prediction = model.predict(model_input)
        return PredictionOutput(prediction)
        