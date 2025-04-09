from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.clients.ml.models.model_manager import ModelManager
from app.clients.ml.models.prediction_logic import interpret_and_calculate

router = APIRouter(prefix="/ml", tags=["ML Model"])

class SetModelRequest(BaseModel):
    model_name: str

class PredictRequest(BaseModel):
    features: list

@router.post("/set_model")
def set_model(req: SetModelRequest):
    try:
        ModelManager.set_model(req.model_name)
        return {"message": f"Model set to {req.model_name}"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/current_model")
def get_current_model():
    return {"current_model": ModelManager.get_current_model_name()}

@router.get("/available_models")
def list_models():
    return {"available_models": ModelManager.list_models()}

@router.post("/predict")
def predict(req: PredictRequest):
    try:
        prediction = ModelManager.predict([req.features])
        return {"prediction": int(prediction[0])}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/predict/structured")
def predict_with_full_input(input_data: dict):
    return interpret_and_calculate(input_data)
