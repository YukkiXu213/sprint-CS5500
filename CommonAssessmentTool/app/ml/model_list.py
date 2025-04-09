from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPClassifier
import numpy as np

# Dummy training data
X_dummy = np.random.rand(100, 24)
y_dummy = np.random.randint(2, size=100)

# Initialize models
logistic_regression = LogisticRegression().fit(X_dummy, y_dummy)
random_forest = RandomForestClassifier().fit(X_dummy, y_dummy)
neural_net = MLPClassifier(hidden_layer_sizes=(64, 32), max_iter=500).fit(X_dummy, y_dummy)

# Store them in the model dictionary
available_models = {
    "logistic_regression": logistic_regression,
    "random_forest": random_forest,
    "neural_net": neural_net,
}

def list_available_models():
    return list(available_models.keys())

def get_model(model_name: str):
    return available_models.get(model_name)
