from app.ml.model_list import get_model

_current_model = "logistic_regression"


def get_current_model():
    return _current_model


def set_current_model(model_name: str):
    global _current_model
    if get_model(model_name):
        _current_model = model_name
    else:
        raise ValueError(f"Model {model_name} not found.")


def predict(X):
    model = get_model(_current_model)
    if model is None:
        raise ValueError("Model is not loaded")
    return model.predict_proba(X)[:, 1]
