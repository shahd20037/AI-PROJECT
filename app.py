from flask import Flask, jsonify, request
import pandas as pd

app = Flask(__name__)  # صححت _name لـ _name_

# ---------- 1) Load Your Excel Dataset ----------
df = pd.read_excel("student_performance_dataset.xlsx")  # الداتا الحالية

# ---------- 2) Basic Route ----------
@app.route("/")
def home():
    return "Backend is working! 🎉"

# ---------- 3) Get All Student Data ----------
@app.route("/students", methods=["GET"])
def get_students():
    data = df.to_dict(orient="records")
    return jsonify(data)

# ---------- 4) Health Check ----------
@app.route("/health")
def health():
    return jsonify({"status": "running", "students_count": len(df)})

# ---------- 5) Prediction API placeholder ----------
@app.route("/predict", methods=["POST"])
def predict():
    student_data = request.json
    predicted_result = {
        "predicted_risk_level": "Unknown",  # placeholder
        "note": "ML model not integrated yet"
    }
    return jsonify(predicted_result)

# ---------- 6) Upload Dataset ----------
@app.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return {"error": "No file part"}, 400

    file = request.files["file"]

    if file.filename == "":
        return {"error": "No selected file"}, 400

    try:
        # اقرأ الملف الجديد كـ Excel
        global df
        df = pd.read_excel(file)

        return {"status": "uploaded", "rows": len(df)}, 200
    except Exception as e:
        return {"error": str(e)}, 500

# ---------- Run Server ----------
if __name__ == "__main__":
    app.run(debug=True)