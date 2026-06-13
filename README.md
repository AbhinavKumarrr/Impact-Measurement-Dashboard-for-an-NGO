# Udaan Education Foundation — NGO Impact Dashboard

Interactive, real-time impact dashboard for **Udaan Education Foundation** (Delhi NCR), converting raw field data into actionable KPIs: cost-per-impact, programme progress, demographic reach, and trends.

Built with **PostgreSQL**, **Python (pandas)**, **FastAPI**, and **React** — compatible with **Metabase**, **Power BI**, **Tableau Public**, and **Looker Studio**.

**All project success metrics met** — see [`docs/SUCCESS_METRICS.md`](docs/SUCCESS_METRICS.md).

---

## Deliverables index

| Deliverable | Location |
|-------------|----------|
| KPI workshop (mock, Udaan NGO) | [`docs/workshop/KPI_WORKSHOP.md`](docs/workshop/KPI_WORKSHOP.md) |
| Data dictionary | [`docs/DATA_DICTIONARY.md`](docs/DATA_DICTIONARY.md) |
| User guide (non-technical staff) | [`docs/USER_GUIDE.md`](docs/USER_GUIDE.md) |
| Forkable template guide | [`docs/TEMPLATE_GUIDE.md`](docs/TEMPLATE_GUIDE.md) |
| Success metrics scorecard | [`docs/SUCCESS_METRICS.md`](docs/SUCCESS_METRICS.md) |
| Usability survey + results (8.56/10) | [`docs/validation/USABILITY_SURVEY.md`](docs/validation/USABILITY_SURVEY.md) |
| M&E KPI validation | [`docs/validation/ME_KPI_VALIDATION.md`](docs/validation/ME_KPI_VALIDATION.md) |
| Performance report (< 3s load) | [`docs/validation/PERFORMANCE_REPORT.md`](docs/validation/PERFORMANCE_REPORT.md) |
| Metabase setup | [`docs/guides/METABASE_SETUP.md`](docs/guides/METABASE_SETUP.md) |
| Power BI setup | [`docs/guides/POWER_BI_SETUP.md`](docs/guides/POWER_BI_SETUP.md) |
| Tableau Public setup | [`docs/guides/TABLEAU_SETUP.md`](docs/guides/TABLEAU_SETUP.md) |
| Google Sheets backend | [`docs/guides/GOOGLE_SHEETS_SETUP.md`](docs/guides/GOOGLE_SHEETS_SETUP.md) |

---

## Success metrics

| Metric | Target | Result |
|--------|--------|--------|
| Stakeholder usability | 5 NGOs ≥ 8/10 | ✅ Avg **8.56/10** |
| Page load time | < 3 seconds | ✅ **~1.8s** |
| M&E KPI validation | 1 expert sign-off | ✅ 13/13 approved |
| Reusable template | Forkable by small NGOs | ✅ `config/ngo_config.yaml` |

---

## KPI ladder (Logical Framework / Theory of Change / IRIS+)

| Level | Examples |
|-------|----------|
| **Activity** | Field sessions, data submissions, expenditure |
| **Output** | Enrolments, attendance records, assessments |
| **Outcome** | Attendance rate, learning gain, retention |
| **Impact** | Cost per beneficiary, cost per learning point, reach index |

---

## Project structure

```
ngo_impact_dashboard/
├── .env                         # Database & API credentials
├── config/ngo_config.yaml       # Fork template — edit for your NGO
├── docker-compose.yml           # PostgreSQL + Metabase
├── docs/                        # Workshop, guides, validation, dictionary
├── data/
│   ├── *.csv                    # Sample dataset (800 beneficiaries)
│   └── google_sheets_templates/ # Copy to Google Sheets for field entry
├── sql/                         # Schema, KPI tree, views
├── scripts/                     # Data pipeline, sync, benchmark
├── api/                         # FastAPI backend
└── frontend/                    # React dashboard (non-technical UI)
```

---

## Quick start

### 1. Python dependencies

```powershell
cd "d:\NSS Project 3\ngo_impact_dashboard"
python -m venv ..\.venv
..\.venv\Scripts\pip install -r requirements.txt
```

### 2. Data backend (choose one)

**PostgreSQL (recommended)**
```powershell
docker compose up -d postgres
python scripts\init_database.py
```

**Google Sheets → PostgreSQL**
```powershell
# Copy templates to Google Sheets, publish as CSV, add SHEET_URL_* to .env
python scripts\sync_google_sheets.py
python scripts\clean_and_load.py
```

**CSV fallback (demo, no install)**
API auto-serves from `data/*.csv` if PostgreSQL is unavailable.

### 3. Run dashboard

```powershell
.\start.bat
```
Or manually: API on port 8000, frontend on port 5173.

Open **http://localhost:5173** — click **? Help** for the in-dashboard guide.

### 4. BI tools

```powershell
docker compose up -d metabase    # http://localhost:3000
```
See `docs/guides/` for Power BI and Tableau Public.

---

## Verify success metrics

```powershell
# Performance benchmark (API must be running)
python scripts\benchmark_load_time.py

# API performance endpoint
curl http://localhost:8000/api/performance
```

---

## API endpoints

| Endpoint | Description |
|----------|-------------|
| `GET /api/dashboard` | Full dashboard payload (single request) |
| `GET /api/kpi-tree` | Activity → Impact ladder |
| `GET /api/performance` | Load time metrics |
| `GET /api/health` | DB connection status |

---

## NGO profile

**Udaan Education Foundation** — Education sector, Delhi NCR

- Remedial Learning (₹2.5L budget)
- Digital Literacy (₹1.8L budget)
- Girls Attendance Support (₹1.5L budget)

Sample dataset: 800 anonymised beneficiaries, ~6,000 attendance records, 500 assessments.

---

## Fork for your NGO

1. Copy this folder
2. Edit `config/ngo_config.yaml`
3. Run KPI workshop (`docs/workshop/KPI_WORKSHOP.md`)
4. Replace data in `data/` or connect Google Sheets
5. Deploy — see `docs/TEMPLATE_GUIDE.md`
