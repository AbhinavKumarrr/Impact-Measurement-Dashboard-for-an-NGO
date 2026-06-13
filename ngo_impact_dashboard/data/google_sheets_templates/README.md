# Google Sheets Templates

Copy these CSV files into Google Sheets — **one tab per file**.  
Do not rename column headers.

| File | Sheet tab name | Updated by |
|------|----------------|------------|
| ngos.csv | NGOs | Admin (once) |
| programs.csv | Programmes | Programme manager |
| beneficiaries.csv | Beneficiaries | Field coordinator |
| field_attendance.csv | Attendance | Teachers (daily) |
| assessments.csv | Assessments | M&E officer |
| expenses.csv | Expenses | Finance |
| field_submissions.csv | Submissions | Field coordinator |

**Column definitions:** See `docs/DATA_DICTIONARY.md`  
**Sync instructions:** See `docs/guides/GOOGLE_SHEETS_SETUP.md`

After filling sheets, either:
- Export CSV to `data/` and run `python scripts/clean_and_load.py`
- Publish as CSV URLs and run `python scripts/sync_google_sheets.py`
