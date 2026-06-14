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

#-------------creating a model info endpoint
@app.get("/model-info")
def model_info():

    return {
        "model": "XGBoost",
        "version": "2.0",
        "supported_files": [".py"],
        "features": [
            "LOC_TOTAL",
            "LOC_EXECUTABLE",
            "LOC_BLANK",
            "LOC_COMMENTS",
            "CYCLOMATIC_COMPLEXITY",
            "HALSTEAD_LENGTH",
            "HALSTEAD_VOLUME",
            "HALSTEAD_DIFFICULTY",
            "HALSTEAD_EFFORT",
            "HALSTEAD_PROG_TIME",
            "HALSTEAD_ERROR_EST"
        ]
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

        "risk_level": result["risk_level"],

        "metrics":
            metrics
    }



