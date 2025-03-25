from fastapi import APIRouter
from app.ml.model_registry import list_available_models

router = APIRouter(prefix="/ml", tags=["machine_learning"])

@router.get("/models")
async def get_available_models():
    """
    Return a list of all available ML models
    """
    return {"available_models": list_available_models()}