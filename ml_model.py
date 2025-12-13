import joblib
import pandas as pd

MODEL_PATH = "student_risk_model.pkl"

model = joblib.load(MODEL_PATH)
FEATURES = getattr(model, "feature_names_in_", None)

if FEATURES is None:
    raise RuntimeError(
        "Model has no feature_names_in_. Re-train using DataFrame"
    )

LABEL_MAP = {0: "High", 1: "Medium", 2: "Low"}

def predict_student(student_dict: dict):
    X = pd.DataFrame([[student_dict.get(f, 0) for f in FEATURES]], columns=FEATURES)
    pred = model.predict(X)[0]
    risk = LABEL_MAP.get(int(pred), int(pred))

    result = {"pred_code": int(pred), "risk_level": risk}

    if hasattr(model, "predict_proba"):
        proba = model.predict_proba(X)[0].tolist()
        result["probabilities"] = proba

    return result

def model_info():
    return {
        "n_features": int(getattr(model, "n_features_in_", len(FEATURES))),
        "features": list(FEATURES),
    }