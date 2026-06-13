# Udaan Education Foundation — mpact Measurement Dashboard

Interactive impact measurement dashboard for NGOs, built to transform field-level data into meaningful KPIs and visual insights.

The dashboard demonstrates how education-focused NGOs can track programme performance, learning outcomes, demographic reach, spending efficiency, and overall impact using a modern analytics stack.

---

## Features

### Executive Dashboard

* Executive Monday Score
* Beneficiaries reached
* Attendance rate
* Learning gain
* Programme expenditure
* Cost per beneficiary

### KPI Ladder

Activity -> Output -> Outcome -> Impact framework

* Activity: Sessions delivered, data submissions, expenditure
* Output: Enrolments, attendance records, assessments
* Outcome: Attendance rate, learning gain, retention
* Impact: Cost per beneficiary, cost per learning point, impact efficiency

### Programme Monitoring

* Programme-wise progress tracking
* Attendance monitoring
* Assessment completion
* Budget utilization

### Demographic Reach

* District-wise beneficiary distribution
* Gender-wise participation analysis

### Trends & Analytics

* Attendance trends
* Learning score trends
* Spending trends
* Cost-per-impact comparison

### Data Quality Monitoring

* Submission tracking
* Data quality score
* Invalid and duplicate record detection

---

## Technology Stack

### Frontend

* React
* TypeScript
* Vite
* Recharts

### Backend

* FastAPI
* Python
* Pandas

### Database

* PostgreSQL (optional)
* CSV fallback mode

---

## Project Structure

```text
.
├── api/
├── frontend/
├── data/
├── docs/
├── config/
├── sql/
├── scripts/
├── requirements.txt
├── .env.example
└── README.md
```

---

## Sample Dataset

The project includes an anonymized sample dataset representing:

* 800 beneficiaries
* Attendance records
* Learning assessments
* Programme expenditure
* Field submissions

This dataset is used for demonstration and dashboard development purposes.

---

## Running the Dashboard Locally

### 1. Create Virtual Environment

```bash
python -m venv .venv
```

Activate:

```bash
.venv\Scripts\activate
```

### 2. Install Backend Dependencies

```bash
pip install -r requirements.txt
```

### 3. Start Backend API

Navigate to the project root and run:

```bash
uvicorn api.main:app --reload
```

Backend runs at:

```text
http://localhost:8000
```

API documentation:

```text
http://localhost:8000/docs
```

---

### 4. Start Frontend

Open a new terminal:

```bash
cd frontend
npm install
npm run dev
```

Frontend runs at:

```text
http://localhost:5173
```

---

## API Endpoints

### Health Check

```text
GET /api/health
```

### Dashboard Data

```text
GET /api/dashboard
```

### KPI Tree

```text
GET /api/kpi-tree
```

### Demographics

```text
GET /api/demographics
```

### Programme Progress

```text
GET /api/program-progress
```

### Cost Per Impact

```text
GET /api/cost-per-impact
```

### Performance Metrics

```text
GET /api/performance
```

---

## Data Sources

The dashboard supports:

### CSV Files

Data is automatically loaded from:

```text
data/
```

### PostgreSQL

If PostgreSQL is configured and available, the API reads data directly from the database.

If PostgreSQL is unavailable, the system automatically falls back to CSV mode.

---

## NGO Profile (Sample)

Udaan Education Foundation

Programmes:

* Remedial Learning
* Digital Literacy
* Girls Attendance Support

Location:

* Delhi NCR

---

## Future Enhancements

* Google Sheets integration
* Power BI connectivity
* Tableau connectivity
* Metabase integration
* User authentication
* Role-based access control
* Automated reporting

---

## Author

Abhinav Kumar
