"""Create PostgreSQL database, apply schema/views, and load cleaned sample data."""
import os
import sys
from pathlib import Path

import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
SQL_DIR = BASE_DIR / "sql"

load_dotenv(BASE_DIR / ".env")

DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "ngo_dashboard_2026")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "ngo_dashboard")


def run_sql_file(cursor, filepath: Path):
    sql = filepath.read_text(encoding="utf-8")
    cursor.execute(sql)
    print(f"  Applied {filepath.name}")


def create_database():
    print(f"Connecting to PostgreSQL at {DB_HOST}:{DB_PORT}...")
    conn = psycopg2.connect(
        dbname="postgres",
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT,
    )
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = conn.cursor()

    cur.execute("SELECT 1 FROM pg_database WHERE datname = %s", (DB_NAME,))
    if not cur.fetchone():
        cur.execute(f'CREATE DATABASE "{DB_NAME}"')
        print(f"Created database: {DB_NAME}")
    else:
        print(f"Database already exists: {DB_NAME}")

    cur.close()
    conn.close()


def apply_schema():
    print("Applying schema and views...")
    conn = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT,
    )
    cur = conn.cursor()

    for sql_file in ["schema.sql", "kpi_tree.sql", "kpi_views.sql"]:
        run_sql_file(cur, SQL_DIR / sql_file)

    conn.commit()
    cur.close()
    conn.close()
    print("Schema applied successfully.")


def load_data():
    print("Loading cleaned sample data...")
    sys.path.insert(0, str(BASE_DIR / "scripts"))
    from clean_and_load import main as load_main
    load_main()
    print("Data loaded successfully.")


def main():
    try:
        create_database()
        apply_schema()
        load_data()
        print("\nDatabase setup complete!")
        print(f"  Connection: postgresql://{DB_USER}:***@{DB_HOST}:{DB_PORT}/{DB_NAME}")
    except psycopg2.OperationalError as exc:
        print("\nCould not connect to PostgreSQL.")
        print(f"  Error: {exc}")
        print("\nStart PostgreSQL first:")
        print("  docker compose up -d postgres")
        print("  OR install PostgreSQL and update .env credentials")
        sys.exit(1)


if __name__ == "__main__":
    main()
