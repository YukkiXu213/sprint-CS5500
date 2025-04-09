import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
import pickle


def train_logistic_model(
    data_path="data_commontool.csv", save_path="models/model_logreg.pkl"
):
    df = pd.read_csv(data_path)

    feature_cols = [
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
        "employment_assistance",
        "life_stabilization",
        "retention_services",
        "specialized_services",
        "employment_related_financial_supports",
        "employer_financial_supports",
        "enhanced_referrals",
    ]

    X = df[feature_cols]
    y = df["success_rate"] > 70

    X_train, _, y_train, _ = train_test_split(X, y, test_size=0.2, random_state=42)

    model = LogisticRegression(max_iter=500)
    model.fit(X_train, y_train)

    with open(save_path, "wb") as f:
        pickle.dump(model, f)

    print(f" Logistic Regression model saved to {save_path}")


if __name__ == "__main__":
    train_logistic_model()
