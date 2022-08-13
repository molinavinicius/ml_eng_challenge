import pathlib
import json
from typing import Optional
from fastapi import FastAPI
import joblib

app = FastAPI()

BASE_DIR = pathlib.Path(__file__).resolve().parent
MODEL_DIR = BASE_DIR.parent / "model-registry"
MODEL_PATH = MODEL_DIR/"model.pkl"

AI_MODEL = None

@app.on_event("startup")
def on_startup():
    global AI_MODEL
    #load my model
    if MODEL_PATH.exists():
        AI_MODEL = joblib.load(MODEL_PATH.read_text())


def predict(params):
    global AI_MODEL
    preds_array = AI_MODEL.predict(params)
    return preds_array

@app.post("/predict") 
def read_index(params):
    global AI_MODEL
    query = params or {}
    prediction = predict(query)
    return {
        "query": query, 
        **prediction
    }