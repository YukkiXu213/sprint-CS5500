from typing import Dict, Optional, List, Any
from app.clients.ml.models.logistic_regression import LogisticRegressionModel


class ModelManager:
    _models: Dict[str, LogisticRegressionModel] = {}
    _current_model: Optional[LogisticRegressionModel] = None

    @classmethod
    def load_models(cls) -> None:
        cls._models["logistic_regression"] = LogisticRegressionModel(
            "models/model_logreg.pkl"
        )
        cls._current_model = cls._models["logistic_regression"]

    @classmethod
    def set_model(cls, name: str) -> None:
        if name not in cls._models:
            raise ValueError(f"Model '{name}' not registered.")
        cls._current_model = cls._models[name]

    @classmethod
    def get_current_model_name(cls) -> Optional[str]:
        for name, model in cls._models.items():
            if model == cls._current_model:
                return name
        return None

    @classmethod
    def list_models(cls) -> List[str]:
        return list(cls._models.keys())

    @classmethod
    def predict(cls, X: Any) -> Any:
        if cls._current_model is None:
            raise RuntimeError("No model is currently set.")
        return cls._current_model.predict(X)
