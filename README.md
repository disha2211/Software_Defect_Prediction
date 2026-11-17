# 🔍 Software Defect Predictor

> **ML-based static code analysis with AI-assisted code review**

Software Defect Predictor analyzes Python source code using **static software metrics**, predicts defect probability with an **XGBoost classifier**, assigns a risk level, and generates an additional code review using a **locally hosted Qwen 2.5 3B model through Ollama**.

### Input

- 📁 Python file
- 📝 Python source code
- 🖼️ Code screenshot

### Output

- Defective / Non-Defective prediction
- Defect probability
- Low / Medium / High risk
- Software metrics
- AI-generated code review

---

## Architecture

```text
Python File / Code / Screenshot
              │
              ▼
        ┌─────────────┐
        │    OCR      │  ← screenshot input only
        └──────┬──────┘
               │
               ▼
        Python Source Code
               │
               ▼
        ┌─────────────┐
        │    Radon    │
        │Static Metrics│
        └──────┬──────┘
               │
               ▼
        11 Runtime Features
               │
               ▼
        ┌─────────────┐
        │   XGBoost   │
        └──────┬──────┘
               │
        ┌──────┴──────┐
        ▼             ▼
   Prediction     Probability
                      │
                      ▼
                 Risk Level
                      │
                      ▼
        ┌─────────────────────┐
        │ Qwen 2.5 3B / Ollama│
        │   Code Review Layer  │
        └──────────┬──────────┘
                   ▼
             Final Analysis
```

The ML model is responsible for **defect prediction**. The LLM is used separately for **code review and recommendations**, rather than replacing the classifier.

---

## Core Features

| Component | Purpose |
|---|---|
| **Radon** | Extract source-code metrics |
| **XGBoost** | Predict defect probability |
| **FastAPI** | Serve the analysis pipeline |
| **Streamlit** | Interactive frontend |
| **EasyOCR** | Extract code from screenshots |
| **AST** | Validate Python syntax |
| **Ollama + Qwen 2.5 3B** | Local AI code review |

The production model uses 11 features that can be extracted directly from arbitrary Python source code:

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

These were selected to maintain consistency between training-time and runtime feature availability.

---

## Model

The project uses the **KC1 software defect dataset** and experiments with multiple classifiers before selecting XGBoost for the production inference pipeline.

The final model uses class weighting to address the imbalanced defect distribution.

Prediction is converted into risk using:

```text
Probability < 0.30       → Low
0.30 ≤ Probability < 0.70 → Medium
Probability ≥ 0.70      → High
```

The model and its feature-order contract are stored under [`models/`](models/).

---

## API

| Endpoint | Purpose |
|---|---|
| `GET /` | API health check |
| `GET /model-info` | Model and feature information |
| `POST /analyze-code` | Analyze Python source |
| `POST /analyze-file` | Analyze `.py` file |
| `POST /extract-code-from-image` | Extract code using OCR |
| `POST /validate-code` | Validate Python syntax |

FastAPI also provides interactive documentation at `/docs`.

---

## Run Locally

### 1. Install dependencies

```bash
git clone https://github.com/disha2211/Software_Defect_Prediction.git
cd Software_Defect_Prediction

python -m venv venv
venv\Scripts\activate

pip install -r requirements.txt
```

### 2. Start Ollama

```bash
ollama pull qwen2.5:3b
ollama serve
```

### 3. Start the backend

```bash
uvicorn app.main:app --reload
```

API:

```text
http://localhost:8000
```

Swagger:

```text
http://localhost:8000/docs
```

### 4. Start the frontend

In another terminal:

```bash
streamlit run frontend/streamlit_app.py
```

---

## Repository Documentation

The implementation details are intentionally separated from this README.

- [`app/README.md`](app/README.md) — backend and inference pipeline
- [`frontend/README.md`](frontend/README.md) — Streamlit interface and request flow
- [`models/README.md`](models/README.md) — model artifacts and feature contract
- [`notebooks/README.md`](notebooks/README.md) — dataset, experiments, feature selection and training methodology

---

## Tech Stack

**Python · FastAPI · Streamlit · Radon · XGBoost · Scikit-learn · EasyOCR · OpenCV · Ollama · Qwen 2.5 3B · Pandas · NumPy**

---

## Limitations

- Currently supports Python source code.
- OCR output may require manual correction.
- The ML model is trained on the KC1 dataset and may not generalize to all codebases.
- The LLM review is advisory and does not determine the primary defect label.
- Risk thresholds are application-level thresholds, not calibrated probability guarantees.

---

## License

MIT License
