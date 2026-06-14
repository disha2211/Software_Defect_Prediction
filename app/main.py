from fastapi import FastAPI,UploadFile,File,HTTPException
from app.metric_extractor  import extract_metrics
from app.schemas import  SoftwareMetrics
from app.predict  import predict_defect
from app.schemas import CodeRequest
from app.ocr import (
    extract_code_from_image
)
import ast
from app.ai_analyzer import (
    analyze_code_with_ai
)


def analyze_source_code(
    code: str
):

    metrics = extract_metrics(
        code
    )

    result = predict_defect(
        metrics
    )

    ai_review = analyze_code_with_ai(
        code=code,
        metrics=metrics,
        prediction=result["prediction"],
        probability=result["probability"]
    )

    return {

        "prediction":
            result["prediction"],

        "probability":
            result["probability"],

        "risk_level":
            result["risk_level"],

        "metrics":
            metrics,

        "ai_review":
            ai_review
    }

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
            detail="Only Python files are supported."
        )

    try:

        # Read file
        content = await file.read()

        code = content.decode("utf-8")

        result = analyze_source_code(code)

        return {
            "filename": file.filename,
            **result
        }

    except SyntaxError as e:

        raise HTTPException(
            status_code=400,
            detail=f"Invalid Python syntax: {e}"
        )

    except UnicodeDecodeError:

        raise HTTPException(
            status_code=400,
            detail="Unable to decode uploaded file."
        )

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=f"Unexpected error: {str(e)}"
        )

@app.post("/analyze-code")
async def analyze_code(
    request: CodeRequest
):

    try:

        return analyze_source_code(
            request.code
        )

    except SyntaxError as e:

        raise HTTPException(
            status_code=400,
            detail=f"Invalid Python syntax: {e}"
        )

@app.post(
    "/extract-code-from-image"
)
async def extract_code_endpoint(
    file: UploadFile = File(...)
):

    try:

        image_bytes = await file.read()

        extracted_code = (
            extract_code_from_image(
                image_bytes
            )
        )

        return {
            "extracted_code":
                extracted_code
        }

    except Exception as e:

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )



@app.post(
    "/validate-code"
)
async def validate_code(
    request: CodeRequest
):

    try:

        ast.parse(
            request.code
        )

        return {
            "valid": True
        }

    except SyntaxError as e:

        return {
            "valid": False,
            "error":
                f"Line {e.lineno}: {e.msg}"
        }