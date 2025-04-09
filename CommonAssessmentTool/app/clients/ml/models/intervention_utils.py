from typing import Any, List

import numpy as np


def clean_input_data(input_data: dict) -> List[Any]:
    columns = [
        "age",
        "gender",
        "work_experience",
        "canada_workex",
        "dep_num",
        "canada_born",
        "citizen_status",
        "level_of_schooling",
        "fluent_english",
        "reading_english_scale",
        "speaking_english_scale",
        "writing_english_scale",
        "numeracy_scale",
        "computer_scale",
        "transportation_bool",
        "caregiver_bool",
        "housing",
        "income_source",
        "felony_bool",
        "attending_school",
        "currently_employed",
        "substance_use",
        "time_unemployed",
        "need_mental_health_support_bool",
    ]
    output = []
    for col in columns:
        val = input_data.get(col, None)
        output.append(convert_text(val) if isinstance(val, str) else val)
    return output


def convert_text(text: Any) -> Any:
    mappings = [
        {"yes": 1, "no": 0, "true": 1, "false": 0, "": 0, "Yes": 1, "No": 0},
        {"Grade 0-8": 1, "Post graduate": 14},
        {"Renting-private": 1, "Emergency hostel": 10},
        {"No Source of Income": 1, "Other (specify)": 10},
    ]
    for mapping in mappings:
        if text in mapping:
            return mapping[text]
    return int(text) if str(text).isnumeric() else text


def get_baseline_row(features: List[Any]) -> np.ndarray:
    """
    Convert cleaned feature list into a NumPy array for prediction.
    """
    return np.array(features, dtype=np.float32)


def create_matrix(features: List[Any]) -> np.ndarray:
    """
    Simulates creating multiple intervention scenarios by modifying input features.
    This example just replicates the features with small variations.
    """
    interventions = []
    for i in range(5):
        modified = features.copy()
        if isinstance(modified[0], (int, float)):  # just for demonstration
            modified[0] += i  # e.g., vary age
        interventions.append(modified)
    return np.array(interventions, dtype=np.float32)


def intervention_row_to_names(row: np.ndarray) -> List[str]:
    """
    Convert a row of intervention data into human-readable intervention names.
    This is a placeholder — use real mapping in production.
    """
    return [f"intervention_{i}" for i, val in enumerate(row) if val > 0.5]
