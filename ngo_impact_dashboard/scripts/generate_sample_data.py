import random
from datetime import date, timedelta
import pandas as pd
import numpy as np
from pathlib import Path

random.seed(42)
np.random.seed(42)

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

ngo_name = "Udaan Education Foundation"
sector = "Education"
city = "Delhi"
state = "Delhi"

programs = [
    {"program_name": "Remedial Learning", "program_type": "Education", "budget_allocated": 250000},
    {"program_name": "Digital Literacy", "program_type": "Skill Development", "budget_allocated": 180000},
    {"program_name": "Girls Attendance Support", "program_type": "Retention", "budget_allocated": 150000},
]

districts = ["North Delhi", "South Delhi", "East Delhi", "West Delhi", "Noida", "Ghaziabad"]
villages = ["Village A", "Village B", "Village C", "Village D", "Village E"]
genders = ["Male", "Female", "Other"]

def rand_date(start_days_ago=365, end_days_ago=0):
    today = date.today()
    delta_days = random.randint(end_days_ago, start_days_ago)
    return today - timedelta(days=delta_days)

# NGO
ngos_df = pd.DataFrame([{
    "ngo_id": 1,
    "ngo_name": ngo_name,
    "sector": sector,
    "city": city,
    "state": state
}])

# Programs
program_rows = []
for i, p in enumerate(programs, start=1):
    program_rows.append({
        "program_id": i,
        "ngo_id": 1,
        "program_name": p["program_name"],
        "program_type": p["program_type"],
        "start_date": date.today() - timedelta(days=300),
        "end_date": None,
        "budget_allocated": p["budget_allocated"]
    })
programs_df = pd.DataFrame(program_rows)

# Beneficiaries
beneficiaries = []
for i in range(1, 801):
    program_id = random.choice([1, 2, 3])
    beneficiaries.append({
        "beneficiary_id": i,
        "ngo_id": 1,
        "program_id": program_id,
        "beneficiary_name": f"Student {i}",
        "gender": random.choice(genders),
        "age": random.randint(6, 18),
        "district": random.choice(districts),
        "village": random.choice(villages),
        "enrollment_date": rand_date(300, 1),
        "is_active": random.choice([True, True, True, False])
    })
beneficiaries_df = pd.DataFrame(beneficiaries)

# Attendance
attendance_rows = []
aid = 1
for _, row in beneficiaries_df.iterrows():
    sessions = random.randint(4, 16)
    for _ in range(sessions):
        attendance_rows.append({
            "attendance_id": aid,
            "beneficiary_id": row["beneficiary_id"],
            "program_id": row["program_id"],
            "visit_date": rand_date(250, 1),
            "present": random.choice([True, True, True, False]),
            "session_type": random.choice(["Class", "Workshop", "Counselling"])
        })
        aid += 1
attendance_df = pd.DataFrame(attendance_rows)

# Assessments
assessment_rows = []
ass_id = 1
for _, row in beneficiaries_df.sample(500, random_state=42).iterrows():
    pre = random.randint(20, 70)
    improvement = random.randint(0, 30)
    post = min(pre + improvement, 100)
    assessment_rows.append({
        "assessment_id": ass_id,
        "beneficiary_id": row["beneficiary_id"],
        "program_id": row["program_id"],
        "assessment_date": rand_date(200, 1),
        "pre_score": pre,
        "post_score": post,
        "score_type": "Learning Test"
    })
    ass_id += 1
assessments_df = pd.DataFrame(assessment_rows)

# Expenses
expense_rows = []
exp_id = 1
for program_id in [1, 2, 3]:
    for _ in range(12):
        expense_rows.append({
            "expense_id": exp_id,
            "program_id": program_id,
            "expense_date": rand_date(365, 1),
            "category": random.choice(["Staff", "Materials", "Transport", "Training", "Monitoring"]),
            "amount": round(random.uniform(5000, 30000), 2),
            "vendor": random.choice(["Vendor A", "Vendor B", "Vendor C"])
        })
        exp_id += 1
expenses_df = pd.DataFrame(expense_rows)

# Field submissions
submissions_df = pd.DataFrame([{
    "submission_id": 1,
    "ngo_id": 1,
    "submitted_by": "Field Coordinator",
    "submission_date": pd.Timestamp.now(),
    "total_records": len(beneficiaries_df),
    "invalid_records": 0,
    "duplicate_records": 0,
    "notes": "Sample generated data"
}])

# Save CSVs
ngos_df.to_csv(DATA_DIR / "ngos.csv", index=False)
programs_df.to_csv(DATA_DIR / "programs.csv", index=False)
beneficiaries_df.to_csv(DATA_DIR / "beneficiaries.csv", index=False)
attendance_df.to_csv(DATA_DIR / "field_attendance.csv", index=False)
assessments_df.to_csv(DATA_DIR / "assessments.csv", index=False)
expenses_df.to_csv(DATA_DIR / "expenses.csv", index=False)
submissions_df.to_csv(DATA_DIR / "field_submissions.csv", index=False)

print("Sample data generated in /data")