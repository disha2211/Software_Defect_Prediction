from fastapi import FastAPI

from app.schemas import  SoftwareMetrics
from app.predict  import predict_defect

app = FastAPI(
    title="Software Defect Prediction API"
)

@app.get("/")
def root():

    return {
        "message":
        "Software Defect Prediction API Running"
    }

@app.post("/predict")
def predict(metrics: SoftwareMetrics):

    prediction, probability = predict_defect(
        metrics.model_dump()
    )

    return {
        "prediction": prediction,
        "probability": round(probability, 4)
    }

