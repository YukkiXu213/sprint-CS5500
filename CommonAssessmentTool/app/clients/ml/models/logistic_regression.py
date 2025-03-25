import pickle
from app.clients.ml.models.base_model import BaseModel

class LogisticRegressionModel(BaseModel):
    def __init__(self, model_path: str):
        with open(model_path, "rb") as f:
            self.model = pickle.load(f)

    def predict(self, X):
        return self.model.predict(X)
