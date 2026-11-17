# Backend — Analysis Pipeline

The `app/` package contains the FastAPI backend and the complete source-code analysis pipeline.

## Responsibility

```text
Input
  ↓
Metric Extraction
  ↓
ML Prediction
  ↓
Risk Classification
  ↓
AI Code Review
  ↓
Response
```

The backend does not execute uploaded Python code. It analyzes the source text using static-analysis tools.

---

## Components

### `main.py`

FastAPI entry point and pipeline orchestrator.

It exposes:

- `/`
- `/model-info`
- `/analyze-code`
- `/analyze-file`
- `/extract-code-from-image`
- `/validate-code`

The main analysis flow is:

```python
metrics = extract_metrics(code)

result = predict_defect(metrics)

ai_review = analyze_code_with_ai(
    code=code,
    metrics=metrics,
    prediction=result["prediction"],
    probability=result["probability"]
)
```

---

### `metric_extractor.py`

Converts Python source code into the feature vector required by the production model.

It uses Radon to calculate:

- Raw source metrics
- Cyclomatic complexity
- Halstead metrics

The returned feature dictionary contains:

```text
LOC_TOTAL
LOC_EXECUTABLE
LOC_BLANK
LOC_COMMENTS
CYCLOMATIC_COMPLEXITY
HALSTEAD_LENGTH
HALSTEAD_VOLUME
HALSTEAD_DIFFICULTY
HALSTEAD_EFFORT
HALSTEAD_PROG_TIME
HALSTEAD_ERROR_EST
```

The important design constraint is that these features must be computable directly from the submitted source code.

---

### `predict.py`

Responsible only for ML inference.

At startup it loads:

```text
models/software_defect_model_v2.pkl
models/feature_order_v2.pkl
```

Before prediction, the extracted metrics are reordered according to the saved feature order.

```text
Extracted Metrics
       ↓
Feature Order
       ↓
XGBoost
       ↓
Defect Probability
```

The model returns:

```text
prediction
probability
risk_level
```

Prediction threshold:

```text
probability > 0.50 → Defective
otherwise           → Non-Defective
```

Risk thresholds:

```text
< 0.30 → Low
< 0.70 → Medium
≥ 0.70 → High
```

---

### `ocr.py`

OCR is an **input adapter**, not a separate prediction pipeline.

```text
Image
  ↓
EasyOCR
  ↓
Confidence Filtering
  ↓
Noise Removal
  ↓
Extracted Code
  ↓
Normal Analysis Pipeline
```

OCR detections below `0.70` confidence are discarded.

The implementation also removes common editor/desktop UI noise before returning the extracted text.

The extracted code is intentionally returned to the frontend for review/editing before analysis.

---

### `ai_analyzer.py`

Provides the qualitative AI review layer.

The current local model is:

```text
Qwen 2.5 3B
      ↓
Ollama
      ↓
http://localhost:11434
```

The LLM receives:

- source code
- defect prediction
- defect probability
- extracted metrics

and is instructed to return:

```text
SUMMARY

ISSUES

RECOMMENDATIONS

RISK_ASSESSMENT
```

The LLM does **not** replace the XGBoost prediction.

The architecture deliberately separates:

```text
XGBoost → quantitative prediction

Qwen    → qualitative review
```

---

### `schemas.py`

Contains Pydantic request models used by the API.

The active API request model is:

```python
class CodeRequest(BaseModel):
    code: str
```

The source file also contains an older `SoftwareMetrics` schema representing the original KC1 metric space; the production runtime feature set is narrower.

---

## Backend Design

The backend follows a lightweight service-oriented structure:

```text
FastAPI
  │
  ├── Source Code Handling
  │
  ├── Static Metric Extraction
  │
  ├── ML Inference
  │
  ├── OCR Adapter
  │
  └── Local LLM Review
```

This keeps the frontend independent from the actual analysis implementation.
