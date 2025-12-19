from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import os

app = Flask(__name__)

# ---------------- Excel ----------------
EXCEL_PATH = os.path.join(os.path.dirname(__file__), "students.xlsx")

def read_students():
    if os.path.exists(EXCEL_PATH):
        df = pd.read_excel(EXCEL_PATH)
    else:
        columns = ['StudentID','name','email','department','level','College_of',
                   'attendance','assignment_avg','midterm','practical','project',
                   'final','quiz_avg','oral_avg','GPA','risk_level',
                   'fail_probability','participation','study_hours','mood',
                   'Previous GPA','Class Interaction']
        df = pd.DataFrame(columns=columns)
        df.to_excel(EXCEL_PATH, index=False)
    df["StudentID"] = df["StudentID"].astype(str).str.strip().str.lower()
    df["email"] = df["email"].astype(str).str.strip().str.lower()
    return df

def save_students(df):
    df.to_excel(EXCEL_PATH, index=False)

# ---------------- AI Recommendation ----------------
def generate_recommendation(student):
    rec = []
    if student['attendance'] < 75:
        rec.append("Improve attendance to boost performance.")
    if student['GPA'] < 2.5:
        rec.append("Focus on key subjects to increase GPA.")
    if student['study_hours'] < 10:
        rec.append("Increase study hours for better results.")
    if not rec:
        rec.append("Keep up the good work! Your performance is stable.")
    return " ".join(rec)

# ---------------- Welcome ----------------
@app.route("/")
def welcome():
    return render_template("welcome.html")

# ---------------- Login ----------------
@app.route("/login", methods=["GET", "POST"])
def login_page():
    error = None
    if request.method == "POST":
        username = request.form.get("username", "").strip().lower()
        email = request.form.get("email", "").strip().lower()

        if username == "admin" and email == "admin@uni.com":
            return redirect(url_for("doctor_dashboard"))

        df = read_students()
        student = df[(df["StudentID"] == username) & (df["email"] == email)]

        if student.empty:
            error = "Student not found"
            return render_template("index.html", error=error)

        return redirect(url_for("student_dashboard", student_id=username))

    return render_template("index.html", error=error)

# ---------------- Signup ----------------
@app.route("/signup", methods=["GET", "POST"])
def signup_page():
    if request.method == "POST":
        role = request.form.get("role")
        if role == "doctor":
            return redirect(url_for("login_page"))

        df = read_students()
        new_student = {
            "StudentID": request.form.get("student_id").strip().lower(),
            "name": request.form.get("name"),
            "email": request.form.get("email").strip().lower(),
            "department": "Unknown",
            "level": 1,
            "College_of": "Unknown",
            "attendance": 0,
            "assignment_avg": 0,
            "midterm": 0,
            "practical": 0,
            "project": 0,
            "final": 0,
            "quiz_avg": 0,
            "oral_avg": 0,
            "GPA": 0,
            "risk_level": "Unknown",
            "fail_probability": 0,
            "participation": 0,
            "study_hours": 0,
            "mood": "Unknown",
            "Previous GPA": 0,
            "Class Interaction": 0
        }
        df = pd.concat([df, pd.DataFrame([new_student])], ignore_index=True)
        save_students(df)
        return redirect(url_for("login_page"))

    return render_template("signup.html")

# ---------------- Student Dashboard ----------------
@app.route("/dashboard/student/<student_id>")
def student_dashboard(student_id):
    df = read_students()
    student = df[df["StudentID"] == student_id.strip().lower()]
    if student.empty:
        return "Student not found", 404
    student_data = student.iloc[0].to_dict()
    recommendation = generate_recommendation(student_data)
    return render_template(
        "dashboard.html",
        role="student",
        username=student_data["name"],
        student=student_data,
        recommendation=recommendation
    )

# ---------------- Doctor Dashboard ----------------
@app.route("/dashboard/doctor")
def doctor_dashboard():
    df = read_students()
    if df.empty:
        return "No students found", 404
    student_data = df.iloc[0].to_dict()
    recommendation = generate_recommendation(student_data)
    return render_template(
        "dashboard.html",
        role="doctor",
        username="Admin",
        student=student_data,
        recommendation=recommendation
    )

# ---------------- Run App ----------------
if __name__ == "__main__":
    app.run(debug=True)