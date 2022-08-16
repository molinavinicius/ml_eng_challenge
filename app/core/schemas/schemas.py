from pydantic import BaseModel
from typing import List, Union

from .basic import Precipitaciones, PIB, Imacec, Ventas

class Payload(BaseModel):
    ano: int
    mes: int
    precipitaciones: Precipitaciones
    pib: PIB
    imacec: Imacec
    ventas: Ventas
    
class ModelInput(BaseModel):
    payload: Union[Payload, List[Payload]]
    
class PredictionOutput(BaseModel):
    prediction: float