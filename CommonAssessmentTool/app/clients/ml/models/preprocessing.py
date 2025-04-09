import numpy as np

def clean_input_data(input_data: dict) -> list:
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

def convert_text(text):
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
