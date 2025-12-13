import pandas as pd
import json

# قراءة بيانات الطلاب
df = pd.read_excel("student_performance_dataset.xlsx")

# تحويل كل الطلاب لقائمة JSON
students_json = df.to_dict(orient="records")

# حفظها في ملف JSON
with open("students_payload.json", "w") as f:
    json.dump(students_json, f, indent=4)

print("JSON payload جاهز لكل الطلاب في students_payload.json")
