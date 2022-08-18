from pathlib import Path
from .load_data import DataLoader
from dataclasses import dataclass
from pathlib import Path
import joblib
import json
import os
import pandas as pd
import numpy as np
from fastapi.encoders import jsonable_encoder


from .preprocessors import Preprocessor
from .train import model_training

@dataclass
class TrainPipeline:
    DATASETS_DIR: Path
    MODELS_STORE_DIR: Path

    data_loader = None
    
    def __post_init__(self):
        if self.DATASETS_DIR.exists():
            self.data_loader = DataLoader(self.DATASETS_DIR)
        
        if not self.MODELS_STORE_DIR.exists():
            init_path = self.MODELS_STORE_DIR / '__init__'
            init_path.mkdir(exist_ok=True, parents=True)
    
    def train(self, model_uuid):
        data = self.data_loader.load_to_df(files_format='.csv')        
        preprocessor = Preprocessor(list(data.keys()), data)
        
        X, y = preprocessor.clean()
        
        print(X)
        print(y)
        
        trained = model_training(X, y)
        
        MODEL_DIR = self.MODELS_STORE_DIR/model_uuid
        MODEL_DIR.mkdir(exist_ok=True, parents=True)
        
        joblib.dump(trained['model'], MODEL_DIR/'model.pkl')
        
        MODELS_REGISTRY_PATH = self.MODELS_STORE_DIR /'model_registry.json'
        model_registry = json.loads(MODELS_REGISTRY_PATH.read_text())

        model_registry['last'], model_registry['current'] = model_registry['current'], model_uuid
        MODELS_REGISTRY_PATH.write_text(json.dumps(model_registry, indent=4))
        
        return trained['metrics']
        


