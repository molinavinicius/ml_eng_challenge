from pathlib import Path
from load_data import DataLoader
from dataclasses import dataclass
from pathlib import Path
import joblib
import json
import os
import pandas as pd
import numpy as np
from fastapi.encoders import jsonable_encoder
from typing import Union, List

from .preprocessors import Preprocessor

@dataclass
class TrainPipeline:
    DATASETS_DIR: Path
    EXPORT_MODEL_DIR: Path
    model_uuid: str

    data_loader = None
    model_dir = None
    
    def __post_init__(self):
        if self.DATASETS_DIR.exists():
            self.data_loader = DataLoader(self.DATASETS_DIR)
        
        if not self.EXPORT_MODEL_DIR.exists():
            init_path = self.EXPORT_MODEL_DIR / '__init__'
            init_path.mkdir(exist_ok=True, parents=True)
        else:
            self.model_path = self.EXPORT_MODEL_DIR / self.model_uuid
    
    def train(self):
        data = self.data_loader.load_to_df(files_format='.csv')        
        preprocessor = Preprocessor(list(data.keys()), data)
        
        X, y = preprocessor.clean()
        


