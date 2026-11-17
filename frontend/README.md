# Frontend

The `frontend/` folder contains the Streamlit interface for the Software Defect Predictor.

## Input Modes

The interface provides three analysis modes.

### 1. Upload Python File

```text
.py file
   ↓
FastAPI /analyze-file
   ↓
Analysis Result
```

### 2. Paste Python Code

```text
Python source
   ↓
FastAPI /analyze-code
   ↓
Analysis Result
```

### 3. OCR Screenshot

```text
Screenshot
   ↓
FastAPI /extract-code-from-image
   ↓
Extracted Code
   ↓
User Review / Edit
   ↓
FastAPI /analyze-code
   ↓
Analysis Result
```

The OCR flow intentionally allows the user to correct extraction errors before prediction.

---

## Result View

The dashboard displays:

- Defect prediction
- Defect probability
- Risk level
- Derived confidence indicator
- Static software metrics
- Metric visualization
- AI code review
- Raw API response

The frontend communicates with the backend through HTTP:

```text
Streamlit
    │
    │ HTTP
    ▼
FastAPI :8000
```

The frontend does not load or execute the ML model directly.

---

## Run

Start the backend first:

```bash
uvicorn app.main:app --reload
```

Then start Streamlit:

```bash
streamlit run frontend/streamlit_app.py
```

The backend URL is currently configured as:

```text
http://localhost:8000
```
