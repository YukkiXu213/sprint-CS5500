_current_model = "logistic_regression"

def get_current_model():
    return _current_model

def set_current_model(model_name: str):
    global _current_model
    _current_model = model_name