from typing import Any, Dict

import numpy as np

from app.clients.ml.models.intervention_utils import (
    create_matrix,
    get_baseline_row,
    intervention_row_to_names,
)
from app.clients.ml.models.model_manager import ModelManager
from app.clients.ml.models.preprocessing import clean_input_data


def process_results(baseline_pred: Any, matrix: np.ndarray) -> Dict[str, Any]:
    return {
        "baseline": float(baseline_pred[0]),
        "interventions": [
            {
                "predicted_score": float(row[-1]),
                "interventions": intervention_row_to_names(row[:-1]),
            }
            for row in matrix
        ],
    }


def interpret_and_calculate(input_data: Dict[str, Any]) -> Dict[str, Any]:
    features = clean_input_data(input_data)
    baseline_row = get_baseline_row(features).reshape(1, -1)
    intervention_matrix = create_matrix(features)

    baseline_pred = ModelManager.predict(baseline_row)
    pred_results = ModelManager.predict(intervention_matrix).reshape(-1, 1)

    full_matrix = np.concatenate((intervention_matrix, pred_results), axis=1)
    sorted_matrix = full_matrix[full_matrix[:, -1].argsort()][-3:, -8:]
    return process_results(baseline_pred, sorted_matrix)
