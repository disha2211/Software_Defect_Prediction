# Model Artifacts

This folder contains the serialized artifacts used by the production inference pipeline.

## Active Production Artifacts

### `software_defect_model_v2.pkl`

Serialized XGBoost classifier used for defect prediction.

The model receives the following 11 features:

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

### `feature_order_v2.pkl`

Stores the exact feature order expected by the trained model.

At inference time:

```text
Extracted Metrics
      ↓
Feature Reordering
      ↓
XGBoost Model
```

Keeping the feature order as a separate artifact prevents incorrect column ordering during prediction.

---

## Inference Contract

The production model expects:

```text
11 numeric features
+
fixed feature ordering
```

The runtime extractor and training pipeline must remain synchronized.

If the feature set changes, the model should be retrained and a new feature-order artifact should be generated.

---

## Other Model File

```text
software_defect_model.pkl
```

This is an earlier model artifact.

The current FastAPI inference implementation uses:

```text
software_defect_model_v2.pkl
```

together with:

```text
feature_order_v2.pkl
```

Therefore, `v2` should be treated as the active production artifact.
