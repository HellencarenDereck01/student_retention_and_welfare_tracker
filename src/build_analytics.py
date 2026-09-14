from pathlib import Path
import duckdb


# ------------------------------------------------------------
# Project paths
# ------------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[1]

DATA_DIR = PROJECT_ROOT / "data"
PROCESSED_DIR = DATA_DIR / "processed"
SQL_DIR = PROJECT_ROOT / "sql"

DB_PATH = DATA_DIR / "student_retention.duckdb"
DASHBOARD_OUTPUT = PROCESSED_DIR / "school_dashboard.csv"


# ------------------------------------------------------------
# Helper function
# ------------------------------------------------------------

def execute_sql_file(con, sql_file):
    """Execute all SQL statements contained in a SQL file."""
    
    print(f"Executing: {sql_file.name}")
    
    sql = sql_file.read_text(encoding="utf-8")
    con.execute(sql)


# ------------------------------------------------------------
# Main analytical pipeline
# ------------------------------------------------------------

def build_analytics():
    """Build the DuckDB analytical layer and dashboard dataset."""

    print("Starting analytics pipeline...")

    con = duckdb.connect(str(DB_PATH))

    try:
        # 1. Create source views
        execute_sql_file(
            con,
            SQL_DIR / "source_views.sql"
        )

        # 2. Create school-level KPI views
        execute_sql_file(
            con,
            SQL_DIR / "school_kpis.sql"
        )

        # 3. Create welfare risk view
        execute_sql_file(
            con,
            SQL_DIR / "welfare_risk.sql"
        )

        # 4. Create final dashboard view
        execute_sql_file(
            con,
            SQL_DIR / "school_dashboard.sql"
        )

        # 5. Export final dashboard dataset
        con.execute(f"""
            COPY (
                SELECT *
                FROM school_dashboard
                ORDER BY school_id
            )
            TO '{DASHBOARD_OUTPUT.as_posix()}'
            WITH (
                HEADER,
                DELIMITER ','
            )
        """)

        # 6. Validate final dashboard
        validation = con.execute("""
            SELECT
                COUNT(*) AS total_rows,
                COUNT(DISTINCT school_id) AS unique_schools,
                COUNT(*) - COUNT(DISTINCT school_id)
                    AS duplicate_rows,
                SUM(
                    CASE
                        WHEN school_id IS NULL THEN 1
                        ELSE 0
                    END
                ) AS missing_school_ids
            FROM school_dashboard
        """).fetchone()

        total_rows, unique_schools, duplicate_rows, missing_school_ids = validation

        print()
        print("Dashboard validation:")
        print(f"  Total rows: {total_rows}")
        print(f"  Unique schools: {unique_schools}")
        print(f"  Duplicate rows: {duplicate_rows}")
        print(f"  Missing school IDs: {missing_school_ids}")

        # 7. Stop the pipeline if validation fails
        if total_rows != 600:
            raise ValueError(
                f"Expected 600 schools, but found {total_rows} rows."
            )

        if unique_schools != 600:
            raise ValueError(
                f"Expected 600 unique schools, but found {unique_schools}."
            )

        if duplicate_rows != 0:
            raise ValueError(
                f"Dashboard contains {duplicate_rows} duplicate rows."
            )

        if missing_school_ids != 0:
            raise ValueError(
                f"Dashboard contains {missing_school_ids} missing school IDs."
            )

        print()
        print("Analytics pipeline completed successfully.")
        print(f"Dashboard exported to: {DASHBOARD_OUTPUT}")

    finally:
        con.close()


# ------------------------------------------------------------
# Script entry point
# ------------------------------------------------------------

if __name__ == "__main__":
    build_analytics()