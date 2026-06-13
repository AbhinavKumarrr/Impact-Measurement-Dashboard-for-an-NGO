"""
Sync Google Sheets published CSV URLs into local data/ folder.

Usage:
  python scripts/sync_google_sheets.py              # sync all configured sheets
  python scripts/sync_google_sheets.py --dry-run    # show URLs without downloading

Configure published CSV URLs in .env:
  SHEET_URL_BENEFICIARIES=https://docs.google.com/.../pub?output=csv
  SHEET_URL_ATTENDANCE=...
  (etc.)

If no URLs configured, copies google_sheets_templates/ to data/ as fallback demo.
"""
import os
import sys
import shutil
from pathlib import Path
from urllib.request import urlopen
from urllib.error import URLError

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
TEMPLATE_DIR = DATA_DIR / "google_sheets_templates"

load_dotenv(BASE_DIR / ".env")

SHEET_MAP = {
    "SHEET_URL_NGOS": "ngos.csv",
    "SHEET_URL_PROGRAMS": "programs.csv",
    "SHEET_URL_BENEFICIARIES": "beneficiaries.csv",
    "SHEET_URL_ATTENDANCE": "field_attendance.csv",
    "SHEET_URL_ASSESSMENTS": "assessments.csv",
    "SHEET_URL_EXPENSES": "expenses.csv",
    "SHEET_URL_SUBMISSIONS": "field_submissions.csv",
}


def download_sheet(url: str, dest: Path) -> bool:
    try:
        with urlopen(url, timeout=30) as resp:
            content = resp.read()
        if b"<html" in content[:500].lower():
            print(f"  ERROR: URL returned HTML, not CSV: {url[:60]}...")
            return False
        dest.write_bytes(content)
        print(f"  Downloaded {dest.name} ({len(content):,} bytes)")
        return True
    except URLError as exc:
        print(f"  ERROR downloading {dest.name}: {exc}")
        return False


def copy_templates():
    if not TEMPLATE_DIR.exists():
        print("No templates found. Run generate_sample_data.py first.")
        return False
    for src in TEMPLATE_DIR.glob("*.csv"):
        shutil.copy2(src, DATA_DIR / src.name)
        print(f"  Copied template {src.name}")
    return True


def main():
    dry_run = "--dry-run" in sys.argv
    configured = {k: v for k, v in SHEET_MAP.items() if os.getenv(k)}

    if not configured:
        print("No SHEET_URL_* variables in .env — using local templates.")
        if dry_run:
            print("Would copy templates from data/google_sheets_templates/")
            return
        copy_templates()
        print("\nTo connect Google Sheets:")
        print("  1. Publish each tab as CSV (File → Share → Publish to web)")
        print("  2. Add SHEET_URL_* entries to .env")
        print("  3. Re-run this script")
        return

    print(f"Syncing {len(configured)} sheet(s)...")
    ok = 0
    for env_key, filename in SHEET_MAP.items():
        url = os.getenv(env_key)
        if not url:
            continue
        dest = DATA_DIR / filename
        if dry_run:
            print(f"  Would download {filename} from {url[:60]}...")
            ok += 1
            continue
        if download_sheet(url, dest):
            ok += 1

    print(f"\nSynced {ok}/{len(configured)} files.")
    if not dry_run and ok:
        print("Next: python scripts/clean_and_load.py")


if __name__ == "__main__":
    main()
