# ===============================
# 1️⃣ استيراد المكتبات
# ===============================
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.metrics import accuracy_score
import joblib

# ===============================
# 2️⃣ قراءة ملف الإكسل
# ===============================
DATA_FILE =  r"C:\Users\Hi-TecH\OneDrive\Desktop\Backend\students.xlsx"

df = pd.read_excel(DATA_FILE)

print("الأعمدة الموجودة في الملف:")
print(df.columns)

# ===============================
# 3️⃣ اختيار الأعمدة (Features + Target)
# ===============================
FEATURES = [
    "study_hours",
    "attendance",
    "quiz_avg",
    "midterm"
]

TARGET = "risk_level"   # Low / Medium / High

# التأكد إن الأعمدة موجودة
for col in FEATURES + [TARGET]:
    if col not in df.columns:
        raise ValueError(f"Column '{col}' not found in Excel")

X = df[FEATURES]
y = df[TARGET]

# ===============================
# 4️⃣ تحويل Target لأرقام
# ===============================
label_encoder = LabelEncoder()
y = label_encoder.fit_transform(y)

# ===============================
# 5️⃣ تقسيم الداتا
# ===============================
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# ===============================
# 6️⃣ Scaling (مهم جدًا)
# ===============================
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# ===============================
# 7️⃣ تدريب الموديل
# ===============================
model = LogisticRegression(max_iter=1000)
model.fit(X_train, y_train)

# ===============================
# 8️⃣ التقييم
# ===============================
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

print(f"\nModel Accuracy: {accuracy*100:.2f}%")

# ===============================
# 9️⃣ حفظ الموديل
# ===============================
joblib.dump(model, "student_model.pkl")
joblib.dump(label_encoder, "label_encoder.pkl")
joblib.dump(scaler, "scaler.pkl")

print("\n✅ ML model saved successfully!")