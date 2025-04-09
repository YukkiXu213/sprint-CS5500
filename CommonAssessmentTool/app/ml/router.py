from fastapi import APIRouter, HTTPException
from app.ml.model_list import list_available_models, get_model
from app.ml.model_state import get_current_model, set_current_model
from pydantic import BaseModel
import numpy as np

router = APIRouter(prefix="/ml", tags=["machine_learning"])

@router.get("/models")
async def get_models():
    """
    List all available machine learning models
    """
    return {"available_models": list_available_models()}


@router.get("/model/current")
async def current_model():
    """
    Get the currently selected machine learning model
    """
    return {"current_model": get_current_model()}


@router.post("/model/switch")
async def switch_model(model_name: str):
    """
    Switch the current machine learning model
    """
    if model_name not in list_available_models():
        raise HTTPException(status_code=400, detail="Model not available")

    try:
        set_current_model(model_name)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return {"message": f"Model switched to {model_name}"}

class ModelInput(BaseModel):
    features: list[float]  # expecting 24 numbers

@router.post("/predict/{model_name}")
def predict(model_name: str, input: ModelInput):
    model = get_model(model_name)
    if model is None:
        return {"error": "Model not found"}
    
    if len(input.features) != 24:
        return {"error": "Input must contain exactly 24 features"}

    X = np.array(input.features).reshape(1, -1)
    prediction = model.predict(X)
    return {"model": model_name, "prediction": int(prediction[0])}