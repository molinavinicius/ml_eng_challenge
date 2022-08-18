from genericpath import isfile
import pandas as pd
from pathlib import Path
from dataclasses import dataclass

@dataclass
class DataLoader:
    DATASETS_DIR: Path
    
    datasets = None
    
    def __post_init__(self):
        if self.DATASETS_DIR.exists():
            p = Path(self.DATASETS_DIR).glob('**/*')
            self.datasets = [x.name.replace('.csv','') for x in p if x.is_file() and x.name.endswith("csv")]

    def load_to_df(self, files_format='.csv'):
        dfs = {}
        for dataset in self.datasets:
            dfs[dataset] = pd.read_csv(self.DATASETS_DIR/(dataset+files_format))
        return dfs