from app.clients.ml.models.logistic_regression import LogisticRegressionModel

class ModelManager:
    _models = {}
    _current_model = None

    @classmethod
    def load_models(cls):
        cls._models["logistic_regression"] = LogisticRegressionModel("models/model_logreg.pkl")
        cls._current_model = cls._models["logistic_regression"]

    @classmethod
    def set_model(cls, name: str):
        if name not in cls._models:
            raise ValueError(f"Model '{name}' not registered.")
        cls._current_model = cls._models[name]

    @classmethod
    def get_current_model_name(cls):
        for name, model in cls._models.items():
            if model == cls._current_model:
                return name
        return None

    @classmethod
    def list_models(cls):
        return list(cls._models.keys())

    @classmethod
    def predict(cls, X):
        if cls._current_model is None:
            raise RuntimeError("No model is currently set.")
        return cls._current_model.predict(X)

