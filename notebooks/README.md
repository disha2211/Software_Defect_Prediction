# ML Methodology

This folder contains the experiments used to develop the production defect-prediction model.

## 1. Dataset

The project uses the **KC1 software defect dataset**.

The dataset contains:

```text
Samples: 1183
Features: 21
Target: Defective
```

The target contains:

```text
Non-Defective: 869
Defective:     314
```

The original dataset contains 21 software metrics plus the defect label.

---

## 2. Exploratory Data Analysis

The initial notebooks inspect:

- Dataset dimensions
- Feature types
- Missing values
- Feature distributions
- Target distribution
- Correlations
- Defect-related patterns

The target is converted from:

```text
Y / N
```

to:

```text
1 / 0
```

for binary classification.

---

## 3. Model Experiments

Multiple classical ML approaches were explored during development.

```text
Logistic Regression
        ↓
Balanced Logistic Regression
        ↓
Random Forest
        ↓
XGBoost
```

The objective was not only to compare model performance, but also to determine which approach could operate on features available during real source-code inference.

---

## 4. Runtime Feature Constraint

The original KC1 dataset contains metrics that cannot all be extracted from arbitrary Python source code using the current Radon-based implementation.

Therefore, the production pipeline uses only features that can be generated directly from submitted source code.

### Production feature set

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

This creates the required alignment:

```text
Training
   │
   │ same features
   ▼
Runtime
```

The model therefore does not depend on manually supplied KC1-only metrics during inference.

---

## 5. Train/Test Split

The extractable-feature dataset is split using:

```python
train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)
```

`stratify=y` preserves the class distribution between training and testing data.

---

## 6. Class Imbalance

The dataset contains substantially fewer defective samples than non-defective samples.

The training pipeline calculates:

```python
scale_pos_weight = negative_samples / positive_samples
```

The resulting value is approximately:

```text
2.77
```

This weight is passed to XGBoost to increase the influence of the minority defective class.

---

## 7. XGBoost Training

The production model uses:

```text
n_estimators      = 300
max_depth         = 4
learning_rate     = 0.05
subsample         = 0.8
colsample_bytree  = 0.8
eval_metric       = logloss
random_state      = 42
scale_pos_weight  ≈ 2.77
```

The trained model is serialized for use by the FastAPI inference service.

---

## 8. Production Artifacts

Training produces two important artifacts:

```text
models/
├── software_defect_model_v2.pkl
└── feature_order_v2.pkl
```

### Model artifact

Contains the trained XGBoost classifier.

### Feature-order artifact

Contains the exact feature ordering expected by the model.

During inference:

```text
Extracted Metrics
       ↓
Reorder using feature_order_v2.pkl
       ↓
XGBoost
```

This prevents feature-column ordering mismatches.

---

## 9. Interpretation Experiments

The notebooks also explore feature importance and SHAP-based interpretation.

These experiments are part of the research/development workflow.

They are not currently part of the production API response.

---

## Notebook Roles

| Notebook | Purpose |
|---|---|
| `initial_EDA.ipynb` | Initial dataset inspection |
| `EDA.ipynb` | Exploratory analysis and feature investigation |
| `logistic_regression.ipynb` | Logistic regression experiments |
| `best_model.ipynb` | Model comparison / selection |
| `train_extractable_features.ipynb` | Production feature selection and XGBoost training |
| `converting.ipynb` | Dataset / feature conversion experiments |

The most important notebook for understanding the current production model is:

```text
train_extractable_features.ipynb
```
