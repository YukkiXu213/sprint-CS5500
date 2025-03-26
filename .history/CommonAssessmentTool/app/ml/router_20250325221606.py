# app/ml/router.py

from fastapi import APIRouter, HTTPException
from app.ml.model_registry import list_available_models
from app.ml.model_state import get_current_model, set_current_model

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

    set_current_model(model_name)
    return {"message": f"Model switched to {model_name}"}