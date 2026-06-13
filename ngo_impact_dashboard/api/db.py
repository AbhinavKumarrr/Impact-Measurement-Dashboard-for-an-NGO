import os
import functools
from pathlib import Path
from contextlib import contextmanager

import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

load_dotenv(BASE_DIR / ".env")

DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "ngo_dashboard_2026")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "ngo_dashboard")

DATABASE_URL = (
    f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

_engine = None
_db_checked = False
_db_available = False


def get_engine():
    global _engine, _db_available, _db_checked
    if _db_checked:
        return _engine

    _db_checked = True
    try:
        _engine = create_engine(
            DATABASE_URL,
            pool_pre_ping=True,
            connect_args={"connect_timeout": 1},
        )
        with _engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        _db_available = True
    except Exception:
        _engine = None
        _db_available = False

    return _engine


def is_db_available() -> bool:
    get_engine()
    return _db_available


@contextmanager
def db_session():
    engine = get_engine()
    if not engine:
        raise RuntimeError("Database unavailable")
    with engine.connect() as conn:
        yield conn


def query_df(sql: str) -> pd.DataFrame:
    engine = get_engine()
    if not engine:
        return pd.DataFrame()
    with engine.connect() as conn:
        return pd.read_sql(text(sql), conn)


def _load_csv_tables():
    return {
        "ngos": pd.read_csv(DATA_DIR / "ngos.csv"),
        "programs": pd.read_csv(DATA_DIR / "programs.csv"),
        "beneficiaries": pd.read_csv(DATA_DIR / "beneficiaries.csv"),
        "field_attendance": pd.read_csv(DATA_DIR / "field_attendance.csv"),
        "assessments": pd.read_csv(DATA_DIR / "assessments.csv"),
        "expenses": pd.read_csv(DATA_DIR / "expenses.csv"),
        "field_submissions": pd.read_csv(DATA_DIR / "field_submissions.csv"),
    }


def _load_db_tables():
    return {
        "ngos": query_df("SELECT * FROM ngos"),
        "programs": query_df("SELECT * FROM programs"),
        "beneficiaries": query_df("SELECT * FROM beneficiaries"),
        "field_attendance": query_df("SELECT * FROM field_attendance"),
        "assessments": query_df("SELECT * FROM assessments"),
        "expenses": query_df("SELECT * FROM expenses"),
        "field_submissions": query_df("SELECT * FROM field_submissions"),
    }


def _safe_div(numerator, denominator, default=0):
    try:
        if denominator in (0, 0.0, None) or pd.isna(denominator):
            return default
        return numerator / denominator
    except Exception:
        return default


def _build_payload(t):
    ngos = t["ngos"].copy()
    programs = t["programs"].copy()
    beneficiaries = t["beneficiaries"].copy()
    attendance = t["field_attendance"].copy()
    assessments = t["assessments"].copy()
    expenses = t["expenses"].copy()
    submissions = t["field_submissions"].copy()

    if ngos.empty:
        raise RuntimeError("No NGO data found")

    for df, cols in [
        (beneficiaries, ["age", "program_id", "beneficiary_id"]),
        (attendance, ["program_id", "beneficiary_id"]),
        (assessments, ["program_id", "beneficiary_id", "pre_score", "post_score"]),
        (expenses, ["program_id", "amount"]),
        (submissions, ["total_records", "invalid_records", "duplicate_records"]),
    ]:
        for c in cols:
            if c in df.columns:
                df[c] = pd.to_numeric(df[c], errors="coerce")

    if "present" in attendance.columns:
        attendance["present"] = attendance["present"].astype(str).str.lower().isin(
            ["true", "1", "yes", "y"]
        )

    for c in ["visit_date", "assessment_date", "expense_date", "enrollment_date", "submission_date"]:
        for df in [attendance, assessments, expenses, beneficiaries, submissions]:
            if c in df.columns:
                df[c] = pd.to_datetime(df[c], errors="coerce")

    # Metrics Aggregations
    total_spend = float(expenses["amount"].fillna(0).sum()) if not expenses.empty else 0.0
    enrolled = int(beneficiaries["beneficiary_id"].nunique()) if "beneficiary_id" in beneficiaries.columns else 0
    sessions = int(len(attendance))
    assessed = int(len(assessments))
    att_rate = round(float(attendance["present"].mean() * 100), 2) if not attendance.empty and "present" in attendance.columns else 0.0

    gain_series = pd.Series(dtype="float64")
    if not assessments.empty and {"pre_score", "post_score"}.issubset(assessments.columns):
        gain_series = (assessments["post_score"] - assessments["pre_score"]).dropna()

    learn_gain = round(float(gain_series.mean()), 2) if len(gain_series) else 0.0
    retention = round(float(beneficiaries["is_active"].astype(str).str.lower().isin(["true", "1", "yes"]).mean() * 100), 2) if "is_active" in beneficiaries.columns and len(beneficiaries) else 0.0

    cost_per_beneficiary = round(_safe_div(total_spend, enrolled), 2) if enrolled else 0
    impact_efficiency = round(_safe_div(learn_gain * att_rate, cost_per_beneficiary if cost_per_beneficiary else 1), 4)
    ngo_name = ngos.iloc[0]["ngo_name"] if "ngo_name" in ngos.columns else "NGO Dashboard"

    # Executive Score Calculation
    executive_score = round(
        (
            min(_safe_div(att_rate, 75), 1.0) * 0.40 +
            min(_safe_div(learn_gain, 12), 1.0) * 0.30 +
            min(_safe_div(retention, 80), 1.0) * 0.30
        ),
        2
    )

    overview = {
        "ngo_name": ngo_name,
        "total_beneficiaries": enrolled,
        "total_sessions": sessions,
        "total_assessments": assessed,
        "total_spend": total_spend,
        "avg_learning_gain": learn_gain,
        "attendance_rate": att_rate,
        "cost_per_beneficiary": cost_per_beneficiary,
        "executive_score": executive_score,
        "data_source": "postgresql" if is_db_available() else "csv_fallback",
    }

    kpi_tree = [
        {
            "level": "activity",
            "kpi_code": "ACT_SESSIONS",
            "kpi_name": "Field Sessions Delivered",
            "actual_value": sessions,
            "target_value": 5000,
            "unit": "sessions",
            "progress_pct": round(_safe_div(sessions, 5000) * 100, 1),
        },
        {
            "level": "activity",
            "kpi_code": "ACT_SUBMISSIONS",
            "kpi_name": "Field Data Submissions",
            "actual_value": int(len(submissions)),
            "target_value": 12,
            "unit": "submissions",
            "progress_pct": round(_safe_div(len(submissions), 12) * 100, 1),
        },
        {
            "level": "activity",
            "kpi_code": "ACT_SPEND",
            "kpi_name": "Programme Expenditure",
            "actual_value": round(total_spend, 2),
            "target_value": 580000,
            "unit": "INR",
            "progress_pct": round(_safe_div(total_spend, 580000) * 100, 1),
        },
        {
            "level": "output",
            "kpi_code": "OUT_ENROLLED",
            "kpi_name": "Beneficiaries Enrolled",
            "actual_value": enrolled,
            "target_value": 800,
            "unit": "people",
            "progress_pct": round(_safe_div(enrolled, 800) * 100, 1),
        },
        {
            "level": "output",
            "kpi_code": "OUT_ATTENDANCE",
            "kpi_name": "Attendance Records",
            "actual_value": sessions,
            "target_value": 6000,
            "unit": "records",
            "progress_pct": round(_safe_div(sessions, 6000) * 100, 1),
        },
        {
            "level": "output",
            "kpi_code": "OUT_ASSESSED",
            "kpi_name": "Assessments Completed",
            "actual_value": assessed,
            "target_value": 500,
            "unit": "assessments",
            "progress_pct": round(_safe_div(assessed, 500) * 100, 1),
        },
        {
            "level": "outcome",
            "kpi_code": "OUT_ATT_RATE",
            "kpi_name": "Attendance Rate",
            "actual_value": att_rate,
            "target_value": 75,
            "unit": "%",
            "progress_pct": round(_safe_div(att_rate, 75) * 100, 1),
        },
        {
            "level": "outcome",
            "kpi_code": "OUT_LEARN_GAIN",
            "kpi_name": "Average Learning Gain",
            "actual_value": learn_gain,
            "target_value": 12,
            "unit": "points",
            "progress_pct": round(_safe_div(learn_gain, 12) * 100, 1),
        },
        {
            "level": "outcome",
            "kpi_code": "OUT_RETENTION",
            "kpi_name": "Active Beneficiary Rate",
            "actual_value": retention,
            "target_value": 80,
            "unit": "%",
            "progress_pct": round(_safe_div(retention, 80) * 100, 1),
        },
        {
            "level": "impact",
            "kpi_code": "IMP_COST_BEN",
            "kpi_name": "Cost per Beneficiary",
            "actual_value": cost_per_beneficiary,
            "target_value": 725,
            "unit": "INR/person",
            "progress_pct": None,
        },
        {
            "level": "impact",
            "kpi_code": "IMP_COST_LEARN",
            "kpi_name": "Cost per Learning Point",
            "actual_value": round(_safe_div(total_spend, gain_series.sum()), 2) if len(gain_series) else 0,
            "target_value": 500,
            "unit": "INR/point",
            "progress_pct": None,
        },
        {
            "level": "impact",
            "kpi_code": "IMP_REACH",
            "kpi_name": "Demographic Reach Index",
            "actual_value": int(beneficiaries.groupby(["district", "gender"]).ngroups) if {"district", "gender"}.issubset(beneficiaries.columns) else 0,
            "target_value": 100,
            "unit": "index",
            "progress_pct": None,
        },
        {
            "level": "impact",
            "kpi_code": "IMP_EFFICIENCY",
            "kpi_name": "Impact Efficiency Score",
            "actual_value": impact_efficiency,
            "target_value": 1.5,
            "unit": "score",
            "progress_pct": None,
        },
    ]

    if {"district", "gender", "beneficiary_id", "age"}.issubset(beneficiaries.columns):
        demographics = (
            beneficiaries.groupby(["district", "gender"], dropna=False)
            .agg(beneficiaries_reached=("beneficiary_id", "count"), avg_age=("age", "mean"))
            .reset_index()
            .round(2)
            .to_dict(orient="records")
        )
    else:
        demographics = []

    program_progress = []
    for _, prog in programs.iterrows():
        pid = prog.get("program_id")
        ben = beneficiaries[beneficiaries["program_id"] == pid] if "program_id" in beneficiaries.columns else pd.DataFrame()
        att = attendance[attendance["program_id"] == pid] if "program_id" in attendance.columns else pd.DataFrame()
        asm = assessments[assessments["program_id"] == pid] if "program_id" in assessments.columns else pd.DataFrame()
        exp = expenses[expenses["program_id"] == pid] if "program_id" in expenses.columns else pd.DataFrame()

        program_progress.append({
            "program_name": prog.get("program_name", "Programme"),
            "enrolled": int(ben["beneficiary_id"].nunique()) if not ben.empty and "beneficiary_id" in ben.columns else 0,
            "attended_sessions": int(att[att["present"]].shape[0]) if not att.empty and "present" in att.columns else 0,
            "assessed_students": int(len(asm)),
            "attendance_rate": round(float(att["present"].mean() * 100), 2) if not att.empty and "present" in att.columns else 0,
            "avg_test_score_gain": round(float((asm["post_score"] - asm["pre_score"]).mean()), 2) if not asm.empty and {"post_score", "pre_score"}.issubset(asm.columns) else 0,
            "budget_allocated": float(prog.get("budget_allocated", 0) or 0),
            "total_spend": float(exp["amount"].fillna(0).sum()) if not exp.empty and "amount" in exp.columns else 0,
        })

    cost_per_impact = []
    for _, prog in programs.iterrows():
        pid = prog.get("program_id")
        ben = beneficiaries[beneficiaries["program_id"] == pid] if "program_id" in beneficiaries.columns else pd.DataFrame()
        asm = assessments[assessments["program_id"] == pid] if "program_id" in assessments.columns else pd.DataFrame()
        exp = expenses[expenses["program_id"] == pid] if "program_id" in expenses.columns else pd.DataFrame()

        spend = float(exp["amount"].fillna(0).sum()) if not exp.empty and "amount" in exp.columns else 0
        bcount = int(ben["beneficiary_id"].nunique()) if not ben.empty and "beneficiary_id" in ben.columns else 0
        gain_sum = float((asm["post_score"] - asm["pre_score"]).sum()) if not asm.empty and {"post_score", "pre_score"}.issubset(asm.columns) else 0

        cost_per_impact.append({
            "program_name": prog.get("program_name", "Programme"),
            "total_spend": round(spend, 2),
            "beneficiaries": bcount,
            "cost_per_beneficiary": round(_safe_div(spend, bcount), 2) if bcount else 0,
            "cost_per_learning_point": round(_safe_div(spend, gain_sum), 2) if gain_sum else 0,
        })

    if not attendance.empty and "visit_date" in attendance.columns:
        attendance["month"] = pd.to_datetime(attendance["visit_date"], errors="coerce").dt.to_period("M").astype(str)
        monthly_trends = (
            attendance.groupby("month")
            .agg(
                active_beneficiaries=("beneficiary_id", "nunique"),
                sessions_held=("attendance_id", "count"),
                attendance_rate=("present", "mean"),
            )
            .reset_index()
        )
        monthly_trends["attendance_rate"] = (monthly_trends["attendance_rate"] * 100).round(2)
        monthly_trends = monthly_trends.to_dict(orient="records")
    else:
        monthly_trends = []

    if not assessments.empty and "assessment_date" in assessments.columns:
        assessments["month"] = pd.to_datetime(assessments["assessment_date"], errors="coerce").dt.to_period("M").astype(str)
        learning_trends = (
            assessments.groupby("month")
            .agg(
                assessments=("assessment_id", "count"),
                avg_pre_score=("pre_score", "mean"),
                avg_post_score=("post_score", "mean"),
            )
            .reset_index()
        )
        learning_trends["avg_gain"] = (learning_trends["avg_post_score"] - learning_trends["avg_pre_score"]).round(2)
        learning_trends = learning_trends.round(2).to_dict(orient="records")
    else:
        learning_trends = []

    if not expenses.empty and "expense_date" in expenses.columns:
        expenses["month"] = pd.to_datetime(expenses["expense_date"], errors="coerce").dt.to_period("M").astype(str)
        spend_trends = (
            expenses.groupby("month")
            .agg(total_spend=("amount", "sum"), expense_count=("expense_id", "count"))
            .reset_index()
            .round(2)
            .to_dict(orient="records")
        )
    else:
        spend_trends = []

    if submissions.empty:
        data_quality = {
            "total_submissions": 0,
            "total_records": 0,
            "invalid_records": 0,
            "duplicate_records": 0,
            "data_quality_score": 100.0,
        }
    else:
        dq = submissions.iloc[0]
        total_records = int(dq.get("total_records", 0) or 0)
        invalid_records = int(dq.get("invalid_records", 0) or 0)
        duplicate_records = int(dq.get("duplicate_records", 0) or 0)
        data_quality = {
            "total_submissions": int(len(submissions)),
            "total_records": total_records,
            "invalid_records": invalid_records,
            "duplicate_records": duplicate_records,
            "data_quality_score": round(
                _safe_div(total_records - invalid_records - duplicate_records, total_records, 1.0) * 100, 2
            ) if total_records else 100.0,
        }

    return {
        "data_source": "postgresql" if is_db_available() else "csv_fallback",
        "overview": overview,
        "kpi_tree": kpi_tree,
        "demographics": demographics,
        "program_progress": program_progress,
        "cost_per_impact": cost_per_impact,
        "monthly_trends": monthly_trends,
        "learning_trends": learning_trends,
        "spend_trends": spend_trends,
        "data_quality": data_quality,
    }


def compute_kpis_from_csv() -> dict:
    return _build_payload(_load_csv_tables())


def compute_kpis_from_db() -> dict:
    return _build_payload(_load_db_tables())


def get_dashboard_data() -> dict:
    if is_db_available():
        return compute_kpis_from_db()
    return compute_kpis_from_csv()

@functools.lru_cache(maxsize=1)
def get_dashboard_data() -> dict:
    if is_db_available():
        return compute_kpis_from_db()
    return compute_kpis_from_csv()