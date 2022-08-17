import json
import os
import joblib
import pathlib
from typing import Optional, List, Union
from fastapi import FastAPI
from fastapi.responses import StreamingResponse

from .core import (
    models, 
    schemas, 
    settings
)

from .ml import predict as ai

app = FastAPI()

BASE_DIR = pathlib.Path(__file__).resolve().parent
MODEL_STORE_DIR = BASE_DIR.parent / "models_store"

AI_MODEL = None

@app.on_event("startup")
def on_startup():
    global AI_MODEL
    print(MODEL_STORE_DIR)
    AI_MODEL = ai.AIModel(MODEL_STORE_DIR)

@app.post("/prediction") 
def make_prediction(payload:schemas.ModelInput) -> schemas.PredictionOutput:
    global AI_MODEL
    prediction = AI_MODEL.predict(payload)
    return schemas.PredictionOutput(predictions=prediction)
  
# @app.get("/prediction") 
# def read_index(params):
#     global AI_MODEL
#     query = params or {}
#     prediction = predict(query)
#     return {
#         "query": query, 
#         **prediction
#     }  
    
# @app.get("/prediction/{pred_uuid}") 
# def fetch_prediction(pred_uuid):
#     obj = Prediction.objects.get(uuid=my_uuid)
#     return obj

# /models:
# GET: retornar uma lista dos modelos disponíveis
# /models/<uuid>
# GET: retorna detalhes e metadados de um modelo específico (período de dados que foi usado no treinamento, shape do conjunto de treino, e métricas importantes)
# /models/train
# POST: dispara o trigger para um novo treinamento (executa o pipeline, avalia as métricas de performance, e vejo se faz sentido substituir o modelo atual ou não)
# /prediction
# POST: realiza a predição com base no conjunto de dados enviado e salva num banco (Predictions)
# GET: recupera todas as últimas predições realizadas (uuid + payload + inferences + uuid do modelo utilizado)
# /prediction/<uuid>
# GET: recupera uma predição específica
# /assert
# POST: recebe o mesmo payload do /prediction, mas também recebe o y_hat. Devolve métricas sobre o assert e salva no banco (Assertions)