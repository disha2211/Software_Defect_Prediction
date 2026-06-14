from fastapi import FastAPI,UploadFile,File,HTTPException
from app.metric_extractor  import extract_metrics
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


#--------upload endpoint
@app.post("/analyze-file")
async def analyze_file(
    file: UploadFile = File(...)
):
    if not file.filename.endswith(".py"):

        raise HTTPException(
            status_code=400,
            detail=
            "Only Python files are supported."
        )
    #----------Read Content
    content = await file.read()

    code = content.decode(
        "utf-8"
    )

    #-------------Extract Metrics
    metrics = extract_metrics(
        code
    )

    #-------Predict
    result = predict_defect(
        metrics
    )

    #---------Return Everything
    return {

        "filename":
            file.filename,

        "prediction":
            result["prediction"],

        "probability":
            result["probability"],

        "metrics":
            metrics
    }



