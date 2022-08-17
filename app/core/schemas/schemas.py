from pydantic import BaseModel
from typing import List, Union, Dict

from .basic import Precipitaciones, PIB, Imacec, Ventas

class Payload(BaseModel):
    ano: int
    mes: int
    precipitaciones: Precipitaciones
    pib: PIB
    imacec: Imacec
    ventas: Ventas
    
ModelInput = Union[Payload, List[Payload]]
    
class PredictionOutput(BaseModel):
    predictions: List[float]
    
    
class Evaluation(BaseModel):
    payload: Payload
    real: float
    
class EvaluationOutput(BaseModel):
    predicted: Union[float, List[float]]
    real: Union[float, List[float]]
    metrics: Dict[str, float]