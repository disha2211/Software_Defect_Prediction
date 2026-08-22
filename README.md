# 🔍 Software Defect Predictor

> **Machine Learning Powered Static Code Analysis for Python**

Software Defect Predictor is an end-to-end AI/ML application that analyzes Python source code, extracts software engineering metrics, predicts the likelihood of defects using an **XGBoost classifier**, and generates an additional **AI-powered code review** using a locally hosted Qwen 2.5 model through Ollama.

The system supports three input modes:

- 📁 Python file upload
- 📝 Direct Python code input
- 🖼️ Code screenshot → OCR → code analysis

The project combines **static code analysis, supervised machine learning, OCR, REST APIs, and local LLM-based reasoning** into a single workflow.

---

## ✨ Features

### 1. Static Code Analysis

The application analyzes Python source code without executing it.

Using **Radon**, it extracts 11 source-code metrics:

| Feature | Description |
|---|---|
| `LOC_TOTAL` | Total lines of code |
| `LOC_EXECUTABLE` | Executable/source lines |
| `LOC_BLANK` | Blank lines |
| `LOC_COMMENTS` | Comment lines |
| `CYCLOMATIC_COMPLEXITY` | Average cyclomatic complexity |
| `HALSTEAD_LENGTH` | Halstead program length |
| `HALSTEAD_VOLUME` | Halstead volume |
| `HALSTEAD_DIFFICULTY` | Halstead difficulty |
| `HALSTEAD_EFFORT` | Halstead effort |
| `HALSTEAD_PROG_TIME` | Estimated programming time |
| `HALSTEAD_ERROR_EST` | Estimated number of defects |

These metrics form the input to the production ML model.

---

### 2. ML-Based Defect Prediction

The extracted metrics are passed to a trained **XGBoost classifier**.

The model produces:

- Defective / Non-Defective prediction
- Defect probability
- Risk level

Risk levels are determined from the predicted probability:

```text
Probability < 0.30     → Low Risk
0.30 – < 0.70          → Medium Risk
≥ 0.70                 → High Risk
```

The prediction threshold is:

```text
Probability > 0.50 → Defective
Otherwise           → Non-Defective
```

---

### 3. AI Code Review

After the ML prediction, the application sends the source code, extracted metrics, prediction and probability to a local LLM.

The current implementation uses:

```text
Ollama
└── Qwen 2.5 3B
```

The AI reviewer generates:

- Summary
- Potential issues
- Recommendations
- Risk assessment

This creates a two-layer analysis:

```text
Machine Learning
      ↓
Defect Probability
      ↓
Risk Classification
      ↓
Local LLM
      ↓
Human-readable Code Review
```

The LLM therefore acts as an **interpretation/review layer**, rather than replacing the statistical defect classifier.

---

### 4. OCR-Based Code Extraction

The application can analyze code from screenshots.

Pipeline:

```text
Code Screenshot
      ↓
EasyOCR
      ↓
Confidence Filtering
      ↓
OCR Noise Removal
      ↓
Extracted Code
      ↓
User Review / Editing
      ↓
Normal Code Analysis Pipeline
```

OCR detections below a confidence threshold are discarded, and common desktop/editor noise is removed before the extracted code is returned.

---

### 5. Python Syntax Validation

The backend provides a dedicated validation endpoint using Python's `ast` module.

It checks whether submitted code can be parsed as valid Python without executing it.

---

### 6. Interactive Streamlit Dashboard

The Streamlit frontend provides:

- Defect prediction
- Probability visualization
- Risk classification
- Confidence display
- Software metric visualization
- AI code review
- Raw API response inspection
- Python file upload
- Direct code input
- OCR screenshot input

The interface uses a dark theme optimized for code-analysis workflows.

---

# 🏗️ System Architecture

```text
                    ┌─────────────────────┐
                    │      User           │
                    └──────────┬──────────┘
                               │
              ┌────────────────┼────────────────┐
              │                │                │
              ▼                ▼                ▼
        Python File       Paste Code       Screenshot
              │                │                │
              │                │                ▼
              │                │             EasyOCR
              │                │                │
              │                │                ▼
              │                │          Cleaned Code
              │                │                │
              └────────────────┴────────────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │     FastAPI         │
                    │      Backend        │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Static Code Metrics  │
                    │       Radon         │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ 11 Extractable      │
                    │ Features            │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ XGBoost Classifier  │
                    │     v2.0            │
                    └──────────┬──────────┘
                               │
                 ┌─────────────┴─────────────┐
                 │                           │
                 ▼                           ▼
          Defect Probability            Risk Level
                 │
                 ▼
        ┌─────────────────────┐
        │ Local LLM Review    │
        │ Ollama + Qwen 2.5 3B│
        └──────────┬──────────┘
                   │
                   ▼
          AI Code Review
                   │
                   ▼
        ┌─────────────────────┐
        │ Streamlit Dashboard │
        └─────────────────────┘
```

---

# 🧠 Machine Learning Pipeline

The model was developed using the **KC1 software defect dataset**.

The modeling process explored multiple approaches before selecting XGBoost.

### Model experimentation

```text
KC1 Dataset
     │
     ▼
Exploratory Data Analysis
     │
     ├── Class distribution
     ├── Correlation analysis
     ├── Feature distributions
     └── Defect-related patterns
     │
     ▼
Model Experiments
     │
     ├── Logistic Regression
     ├── Balanced Logistic Regression
     ├── Random Forest
     └── XGBoost
     │
     ▼
Feature Availability Analysis
     │
     ▼
Select source-code-extractable features
     │
     ▼
Retrain XGBoost
     │
     ▼
Save production artifacts
```

The project also explores feature importance and SHAP-based model interpretation in the notebooks.

---

# 🎯 Why 11 Features?

The original KC1 dataset contains metrics that are not all directly obtainable from arbitrary Python source code using the current static-analysis implementation.

For production inference, the project therefore narrowed the model input to features that can actually be extracted from source code.

The production feature set is:

```python
[
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
```

This creates consistency between:

```text
Training Features
        ↕
Runtime Features
```

rather than relying on unavailable manually supplied metrics during inference.

---

# 🧩 Architectural Decisions

## 1. Static Analysis Instead of Code Execution

The system analyzes source code without executing it.

This provides a safer and deterministic analysis pipeline and avoids executing potentially unsafe uploaded code.

---

## 2. Radon for Metric Extraction

Radon was selected as the static-analysis engine because it provides Python-oriented:

- Raw code metrics
- Cyclomatic complexity
- Halstead metrics

This makes it possible to transform arbitrary Python source code into structured ML features.

---

## 3. XGBoost for Defect Classification

Multiple classification approaches were investigated during experimentation.

The project ultimately uses XGBoost because defect prediction involves nonlinear relationships between code metrics and defect probability.

The training configuration includes:

```python
n_estimators=300
max_depth=4
learning_rate=0.05
subsample=0.8
colsample_bytree=0.8
scale_pos_weight=...
```

`scale_pos_weight` addresses class imbalance in the defect dataset.

---

## 4. Separate Feature-Order Artifact

The model and feature order are stored independently:

```text
models/
├── software_defect_model_v2.pkl
└── feature_order_v2.pkl
```

At inference time, metrics are explicitly reordered according to the saved feature order before prediction.

This prevents subtle feature-column ordering errors.

---

## 5. FastAPI as the Backend Layer

FastAPI exposes the analysis pipeline through REST endpoints.

This keeps the ML logic independent from the UI and makes the system usable by other clients in the future.

```text
Frontend
   │
   │ HTTP
   ▼
FastAPI
   │
   ├── Metric Extraction
   ├── Prediction
   ├── OCR
   └── AI Review
```

---

## 6. Streamlit as the Presentation Layer

Streamlit was chosen to provide a lightweight interactive interface without introducing a separate JavaScript frontend.

The frontend communicates with FastAPI through HTTP requests.

This keeps presentation and analysis responsibilities separate.

---

## 7. OCR as an Input Adapter

OCR is not treated as a separate prediction system.

Instead:

```text
Image
 ↓
OCR
 ↓
Text
 ↓
Normal Analysis Pipeline
```

This avoids duplicating the defect-analysis logic.

---

## 8. LLM as an Explainability / Review Layer

The LLM does not make the primary defect prediction.

Instead:

```text
Code
 ↓
Static Metrics
 ↓
XGBoost
 ↓
Prediction + Probability
 ↓
Qwen
 ↓
Explanation / Recommendations
```

This separates quantitative prediction from qualitative code review.

---

## 9. Local LLM Inference

The project uses Ollama with:

```text
qwen2.5:3b
```

This allows AI code-review inference to run locally rather than requiring a cloud LLM API.

---

# 📁 Project Structure

```text
Software_Defect_Prediction/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── metric_extractor.py
│   ├── predict.py
│   ├── schemas.py
│   ├── ocr.py
│   └── ai_analyzer.py
│
├── frontend/
│   ├── streamlit_app.py
│   └── .streamlit/
│       └── config.toml
│
├── models/
│   ├── software_defect_model.pkl
│   ├── software_defect_model_v2.pkl
│   └── feature_order_v2.pkl
│
├── notebooks/
│   ├── initial_EDA.ipynb
│   ├── EDA.ipynb
│   ├── logistic_regression.ipynb
│   ├── train_extractable_features.ipynb
│   ├── best_model.ipynb
│   └── converting.ipynb
│
├── data/
│   └── .gitkeep
│
├── sample.py
├── test.png
├── requirements.txt
└── README.md
```

---

# 🔌 API Endpoints

## `GET /`

Health/status endpoint.

```http
GET /
```

Returns:

```json
{
  "message": "Software Defect Prediction API Running"
}
```

---

## `GET /model-info`

Returns information about the production model and supported features.

```http
GET /model-info
```

---

## `POST /analyze-code`

Analyzes Python code supplied in the request body.

### Request

```json
{
  "code": "def divide(a, b):\n    return a / b"
}
```

### Response

```json
{
  "prediction": "Non-Defective",
  "probability": 0.21,
  "risk_level": "Low",
  "metrics": {},
  "ai_review": "..."
}
```

---

## `POST /analyze-file`

Uploads and analyzes a Python file.

```http
POST /analyze-file
```

Supported file type:

```text
.py
```

---

## `POST /extract-code-from-image`

Extracts source code from an image using EasyOCR.

```http
POST /extract-code-from-image
```

Supported image formats:

```text
.png
.jpg
.jpeg
```

---

## `POST /validate-code`

Validates Python syntax using the AST parser.

```http
POST /validate-code
```

Example response:

```json
{
  "valid": false,
  "error": "Line 4: invalid syntax"
}
```

---

# ⚙️ Installation

## 1. Clone the repository

```bash
git clone https://github.com/disha2211/Software_Defect_Prediction.git

cd Software_Defect_Prediction
```

---

## 2. Create a virtual environment

### Windows

```bash
python -m venv venv

venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv venv

source venv/bin/activate
```

---

## 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

# 🤖 Setup Ollama

The AI code-review feature requires Ollama.

Install Ollama and pull the model:

```bash
ollama pull qwen2.5:3b
```

Start Ollama if it is not already running:

```bash
ollama serve
```

The application expects the Ollama API at:

```text
http://localhost:11434
```

---

# 🚀 Running the Application

The project consists of two processes:

```text
FastAPI Backend
        +
Streamlit Frontend
```

## Start FastAPI

From the project root:

```bash
uvicorn app.main:app --reload
```

The API will be available at:

```text
http://localhost:8000
```

FastAPI's interactive documentation:

```text
http://localhost:8000/docs
```

---

## Start Streamlit

Open another terminal and activate the same environment.

Then:

```bash
streamlit run frontend/streamlit_app.py
```

The Streamlit interface will open in your browser.

---

# 🔄 End-to-End Workflow

### File Analysis

```text
Python File
    ↓
FastAPI
    ↓
Read Source
    ↓
Radon Metric Extraction
    ↓
11 Features
    ↓
Feature Ordering
    ↓
XGBoost
    ↓
Prediction + Probability
    ↓
Risk Classification
    ↓
Qwen Code Review
    ↓
Streamlit Dashboard
```

### Screenshot Analysis

```text
Screenshot
    ↓
EasyOCR
    ↓
Confidence Filtering
    ↓
Noise Cleaning
    ↓
Extracted Python Code
    ↓
User Review / Edit
    ↓
FastAPI /analyze-code
    ↓
Normal ML + AI Pipeline
```

---

# 📊 Model Development

The notebooks contain the experimental ML workflow.

### `initial_EDA.ipynb`

Initial exploration of the software defect dataset.

### `EDA.ipynb`

Includes:

- Class distribution
- Correlation analysis
- Feature distributions
- Defect-related metric analysis

The analysis identified relationships between defect likelihood and metrics such as:

- LOC
- Cyclomatic Complexity
- Halstead Effort
- Halstead Volume
- Branch-related complexity

### `logistic_regression.ipynb`

Experiments with:

- Logistic Regression
- Feature scaling
- Balanced Logistic Regression
- Confusion matrices
- Precision
- Recall
- F1
- ROC-AUC

The experiments highlighted the importance of handling class imbalance, particularly because false negatives are costly in defect prediction.

### `best_model.ipynb`

Compares multiple models and explores:

- Random Forest
- XGBoost
- Feature engineering
- Feature importance
- SHAP explanations

### `train_extractable_features.ipynb`

Creates the production-oriented model using only features that can be extracted directly from source code.

The resulting artifacts are:

```text
software_defect_model_v2.pkl
feature_order_v2.pkl
```

---

# 🏷️ Project Evolution

The repository evolved through several major versions.

```text
v1.0.0
 │
 └── Initial Software Defect Prediction API
       │
       ▼
     ML inference
       │
       ▼
v2.0.0
 │
 └── Streamlit frontend
       │
       ▼
     End-to-end workflow
       │
       ▼
 OCR integration
       │
       ▼
 Image → Code analysis
       │
       ▼
 Local LLM integration
       │
       ▼
v3.0.0
 │
 └── AI Code Review
       │
       └── Ollama + Qwen 2.5 3B
```

The Git history shows the major development stages:

```text
Static metric extraction
        ↓
XGBoost prediction
        ↓
FastAPI endpoints
        ↓
Streamlit UI
        ↓
OCR
        ↓
Ollama
        ↓
Qwen 2.5 3B
        ↓
AI Code Review
```

---

# 🛡️ Safety Considerations

The primary defect-analysis pipeline performs static analysis rather than executing submitted Python code.

This is an important architectural property because uploaded code should not need to be executed simply to calculate software metrics.

The AI review layer also receives the source code as text and does not execute it.

---

# ⚠️ Current Limitations

- The current production model supports **Python source code**.
- OCR quality depends on screenshot resolution, formatting and image quality.
- OCR may require manual correction before analysis.
- The current AI review depends on a locally running Ollama server.
- The model is trained on the KC1 defect dataset, so its predictions should not be interpreted as universal ground truth for every Python project.
- The current system uses static metrics and does not perform semantic program analysis.
- No CI/CD integration is currently implemented.
- Model retraining is notebook-driven rather than exposed as a production training pipeline.
- The current risk thresholds are fixed rather than calibrated dynamically.
- The repository contains both an older model artifact and the newer v2 production artifact; inference currently uses the v2 model.

---

# 🔮 Future Improvements

Potential extensions include:

- [ ] Add support for Java, C/C++ and JavaScript
- [ ] Add AST-based semantic features
- [ ] Add code smell detection
- [ ] Add vulnerability/security analysis
- [ ] Add explainable prediction using SHAP directly in the API
- [ ] Calibrate defect probabilities
- [ ] Add model version management
- [ ] Add automated model retraining
- [ ] Add CI/CD integration
- [ ] Analyze complete repositories instead of individual files
- [ ] Add historical defect analysis using Git commits
- [ ] Add batch analysis for multiple files
- [ ] Add downloadable analysis reports
- [ ] Containerize the backend and frontend using Docker
- [ ] Add authentication and API security
- [ ] Add automated unit/integration tests
- [ ] Add monitoring for model performance and drift

---

# 🧰 Technology Stack

| Layer | Technology |
|---|---|
| Language | Python |
| ML | XGBoost, scikit-learn |
| Static Analysis | Radon |
| Data Processing | Pandas, NumPy |
| Model Serialization | Joblib |
| Backend | FastAPI |
| API Server | Uvicorn |
| Validation | Pydantic |
| Syntax Analysis | Python AST |
| OCR | EasyOCR |
| LLM Runtime | Ollama |
| LLM | Qwen 2.5 3B |
| Frontend | Streamlit |
| Visualization | Streamlit charts |
| Explainability | SHAP |
| Experimentation | Jupyter Notebook |

---

# 📌 Project Highlights

**Software Defect Predictor transforms raw Python source code into actionable software-quality intelligence through a multi-stage ML + AI pipeline.**

### Core pipeline

```text
Python Source
     ↓
Static Code Metrics
     ↓
XGBoost Defect Prediction
     ↓
Probability + Risk
     ↓
Local Qwen Code Review
     ↓
Actionable Recommendations
```

### Input flexibility

```text
.py File ──────────────┐
                       │
Pasted Code ───────────┼──→ Analysis Pipeline
                       │
Screenshot → OCR ──────┘
```

### Key architectural principle

> **Use deterministic static analysis and supervised ML for defect prediction, then use a local LLM for contextual explanation and recommendations.**

This separation allows the system to combine **quantitative prediction** with **qualitative AI-assisted code review** without making the LLM responsible for the core classification decision.

---

# 👩‍💻 Author

**Disha Kaushal**

Computer Science & Engineering  
AI / ML Engineering Portfolio Project

---

# 📄 License

Distributed under the MIT License. See 'LICENSE' for more information.
