import joblib
import pandas as pd


model = joblib.load(
    "models/software_defect_model_v2.pkl"
)

feature_order = joblib.load(
    "models/feature_order_v2.pkl"
)

#-----prediction function
def predict_defect(metrics):

    df = pd.DataFrame([metrics])

    df = df[feature_order]

    probability = (
        model.predict_proba(df)[0][1]
    )

    prediction = (
        "Defective"
        if probability > 0.5
        else "Non-Defective"
    )

    return {
        "prediction": prediction,
        "probability": round(
            float(probability),
            4
        )
    }