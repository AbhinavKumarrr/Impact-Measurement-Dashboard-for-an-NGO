import os
from pathlib import Path
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "password")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "ngo_dashboard")

engine = create_engine(
    f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

def clean_beneficiaries(df):
    df = df.drop_duplicates(subset=["beneficiary_id"])
    df["age"] = pd.to_numeric(df["age"], errors="coerce")
    df = df[(df["age"] >= 5) & (df["age"] <= 25)]
    df["gender"] = df["gender"].fillna("Unknown")
    df["is_active"] = df["is_active"].astype(bool)
    return df

def clean_attendance(df):
    df = df.drop_duplicates()
    df["present"] = df["present"].astype(bool)
    return df

def clean_assessments(df):
    df = df.drop_duplicates()
    df["pre_score"] = pd.to_numeric(df["pre_score"], errors="coerce")
    df["post_score"] = pd.to_numeric(df["post_score"], errors="coerce")
    df = df[df["pre_score"].between(0, 100)]
    df = df[df["post_score"].between(0, 100)]
    return df

def clean_expenses(df):
    df = df.drop_duplicates()
    df["amount"] = pd.to_numeric(df["amount"], errors="coerce")
    df = df[df["amount"] > 0]
    return df

def load_table(df, table_name):
    df.to_sql(table_name, engine, if_exists="replace", index=False)
    print(f"Loaded {table_name}: {len(df)} rows")

def main():
    ngos = pd.read_csv(DATA_DIR / "ngos.csv")
    programs = pd.read_csv(DATA_DIR / "programs.csv")
    beneficiaries = pd.read_csv(DATA_DIR / "beneficiaries.csv")
    attendance = pd.read_csv(DATA_DIR / "field_attendance.csv")
    assessments = pd.read_csv(DATA_DIR / "assessments.csv")
    expenses = pd.read_csv(DATA_DIR / "expenses.csv")
    submissions = pd.read_csv(DATA_DIR / "field_submissions.csv")

    beneficiaries = clean_beneficiaries(beneficiaries)
    attendance = clean_attendance(attendance)
    assessments = clean_assessments(assessments)
    expenses = clean_expenses(expenses)

    load_table(ngos, "ngos")
    load_table(programs, "programs")
    load_table(beneficiaries, "beneficiaries")
    load_table(attendance, "field_attendance")
    load_table(assessments, "assessments")
    load_table(expenses, "expenses")
    load_table(submissions, "field_submissions")

if __name__ == "__main__":
    main()