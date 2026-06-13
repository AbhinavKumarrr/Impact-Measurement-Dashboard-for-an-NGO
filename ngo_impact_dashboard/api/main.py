import json
import os
import time
from contextlib import asynccontextmanager
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware

from db import get_dashboard_data, is_db_available

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

origins = os.getenv("CORS_ORIGINS", "http://localhost:5173").split(",")

app = FastAPI(
    title="Udaan Education Foundation — Impact Dashboard API",
    description="Real-time KPIs: cost-per-impact, programme progress, demographic reach, and trends",
    version="1.0.0",
)

app.add_middleware(GZipMiddleware, minimum_size=500)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[o.strip() for o in origins if o.strip()],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

CACHE_TTL = 30
_dashboard_cache = None
_cache_timestamp = 0.0


@asynccontextmanager
async def lifespan(app: FastAPI):
    get_data()
    yield


app.router.lifespan_context = lifespan


def get_data():
    global _dashboard_cache, _cache_timestamp
    now = time.time()

    if _dashboard_cache is not None and (now - _cache_timestamp) < CACHE_TTL:
        return _dashboard_cache

    data = get_dashboard_data()

    if "data_source" not in data:
        data["data_source"] = "postgresql" if is_db_available() else "csv_fallback"

    _dashboard_cache = data
    _cache_timestamp = now
    return data


@app.get("/api/health")
def health():
    return {
        "status": "ok",
        "database": "connected" if is_db_available() else "csv_fallback",
    }


@app.get("/api/overview")
def overview():
    return get_data()["overview"]


@app.get("/api/kpi-tree")
def kpi_tree():
    return get_data()["kpi_tree"]


@app.get("/api/demographics")
def demographics():
    return get_data()["demographics"]


@app.get("/api/program-progress")
def program_progress():
    return get_data()["program_progress"]


@app.get("/api/cost-per-impact")
def cost_per_impact():
    return get_data()["cost_per_impact"]


@app.get("/api/trends")
def trends():
    d = get_data()
    return {
        "attendance": d["monthly_trends"],
        "learning": d["learning_trends"],
        "spend": d["spend_trends"],
    }


@app.get("/api/data-quality")
def data_quality():
    return get_data()["data_quality"]


@app.get("/api/dashboard")
def dashboard():
    return get_data()


@app.get("/api/performance")
def performance():
    start = time.perf_counter()
    data = get_data()
    elapsed_ms = round((time.perf_counter() - start) * 1000, 1)
    payload_bytes = len(json.dumps(data, default=str))

    return {
        "api_response_ms": elapsed_ms,
        "payload_bytes": payload_bytes,
        "cache_ttl_seconds": CACHE_TTL,
        "target_page_load_seconds": 3.0,
        "status": "pass" if elapsed_ms < 3000 else "fail",
        "data_source": data.get("data_source", "unknown"),
    }