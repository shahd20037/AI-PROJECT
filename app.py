from flask import Flask, jsonify, request
import pandas as pd
import joblib

# ---------- Flask App ----------
app = Flask(__name__)

# ---------- Load Dataset ----------
df = pd.read_excel("student_performance_dataset.xlsx")  # غيري الاسم لو الملف مختلف

# ---------- Load ML Model ----------
MODEL_PATH = "student_risk_model.pkl"
model = joblib.load(MODEL_PATH)
FEATURES = getattr(model, "feature_names_in_", None)
if FEATURES is None:
    raise RuntimeError("Model has no feature_names_in_. Re-train using DataFrame")
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

# ---------- Basic Routes ----------
@app.route("/")
def home():
    return "Backend is working! 🎉"

@app.route("/students", methods=["GET"])
def get_students():
    return jsonify(df.to_dict(orient="records"))

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "running", "students_count": len(df)})

# ---------- Prediction Route ----------
@app.route("/predict", methods=["POST"])
def predict():
    data = request.json

    # طالب واحد
    if isinstance(data, dict):
        return jsonify(predict_student(data))

    # أكتر من طالب
    elif isinstance(data, list):
        results = [predict_student(student) for student in data]
        return jsonify(results)

    else:
        return jsonify({"error": "Invalid input format"}), 400

# ---------- Upload New Dataset ----------
@app.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return {"error": "No file part"}, 400
    file = request.files["file"]
    if file.filename == "":
        return {"error": "No selected file"}, 400
    try:
        global df
        df = pd.read_excel(file)
        return {"status": "uploaded", "rows": len(df)}, 200
    except Exception as e:
        return {"error": str(e)}, 500

# ---------- Run Server ----------
if __name__ == "__main__":
    app.run(debug=True)