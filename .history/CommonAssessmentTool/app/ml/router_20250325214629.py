from fastapi import APIRouter, UploadFile, File
import os
import pickle

from app.clients.service import logic
from app.ml.model_list import list_available_models
from app.clients.service.logic import *

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


@router.post("/change")
async def change_model(file: UploadFile = File(...)):
    """
    Changes the model being used by the application.

    Accepts a model file upload, saves it to disk, loads the new model,
    and updates the global MODEL and MODEL_PATH variables in the logic module.
    """
    model_dir = os.path.dirname(logic.MODEL_PATH)

    new_model_path = os.path.join(model_dir, file.filename)

    with open(new_model_path, "wb") as f:
        content = await file.read()
        f.write(content)

    try:
        with open(new_model_path, "rb") as f:
            new_model = pickle.load(f)
    except Exception as e:
        return {"error": f"Failed to load model: {str(e)}"}

    logic.MODEL = new_model
    logic.MODEL_PATH = new_model_path

    return {"message": "Model updated successfully",
            "current_model": type(new_model).__name__,
            "model_path": new_model_path}