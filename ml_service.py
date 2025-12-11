import joblib
import pandas as pd

MODEL_PATH = "student_risk_model.pkl"   # غيّري الاسم لو ملفك مختلف

# Load model once
model = joblib.load(MODEL_PATH)

# Get expected feature names from the trained model
FEATURES = getattr(model, "feature_names_in_", None)

if FEATURES is None:
    raise RuntimeError(
        "Model has no feature_names_in_. "
        "You likely trained using NumPy array. Re-train using a DataFrame with column names."
    )

# Optional: mapping (عدّليه لو encoding عندك مختلف)
LABEL_MAP = {0: "High", 1: "Medium", 2: "Low"}

def predict_student(student_dict: dict):
    """
    student_dict: dict of feature_name -> value
    Missing features will be filled with 0
    Extra keys will be ignored
    """
    # Create a single-row dataframe with EXACT feature order
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