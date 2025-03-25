from fastapi import APIRouter
from ...app.ml.model_list import list_available_models
from ...app.clients.service.logic import MODEL, MODEL_PATH

router = APIRouter(prefix="/ml", tags=["machine_learning"])

@router.get("/models")
async def get_available_models():
    """
    Return a list of all available ML models
    """
    return {"available_models": list_available_models()}

@router.get("/current")
def get_current_model():
    """
    Returns the current model in use.
    It returns the model type (e.g., RandomForestRegressor) and the model file path.
    """
    model_type = type(MODEL).__name__ if MODEL else "No model loaded"
    return {"current_model": model_type, "model_path": MODEL_PATH}