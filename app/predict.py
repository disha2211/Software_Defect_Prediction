import joblib
import pandas as pd

model = joblib.load("models/software_defect_model.pkl")

def engineer_features(df):

    df["COMPLEXITY_DENSITY"] = (
        df["CYCLOMATIC_COMPLEXITY"] /
        (df["LOC_TOTAL"] + 1)
    )

    df["BRANCH_DENSITY"] = (
        df["BRANCH_COUNT"] /
        (df["LOC_TOTAL"] + 1)
    )

    df["COMMENT_RATIO"] = (
        df["LOC_COMMENTS"] /
        (df["LOC_TOTAL"] + 1)
    )

    df["OPERAND_VARIETY"] = (
        df["NUM_UNIQUE_OPERANDS"] /
        (df["NUM_OPERANDS"] + 1)
    )

    df["OPERATOR_VARIETY"] = (
        df["NUM_UNIQUE_OPERATORS"] /
        (df["NUM_OPERATORS"] + 1)
    )

    df["DESIGN_RATIO"] = (
        df["DESIGN_COMPLEXITY"] /
        (df["CYCLOMATIC_COMPLEXITY"] + 1)
    )

    return df

def predict_defect(data):

    df = pd.DataFrame([data])

    df = engineer_features(df)

    probability = model.predict_proba(df)[0][1]

    prediction = (
        "Defective"
        if probability > 0.5
        else "Non-Defective"
    )

    return prediction, float(probability)