-- ============================================================
-- Student Retention & Welfare Tracker
-- Source Views
-- ============================================================


CREATE OR REPLACE VIEW attendance AS
SELECT *
FROM read_csv_auto(
    'data/processed/attendance_clean.csv'
);


CREATE OR REPLACE VIEW infrastructure AS
SELECT *
FROM read_csv_auto(
    'data/processed/infrastructure_clean.csv'
);


CREATE OR REPLACE VIEW mdm AS
SELECT *
FROM read_csv_auto(
    'data/processed/mid_day_meal_procurement_cleaned.csv'
);


CREATE OR REPLACE VIEW school_master AS
SELECT *
FROM read_csv_auto(
    'data/processed/school_master_cleaned.csv'
);


CREATE OR REPLACE VIEW test_scores AS
SELECT *
FROM read_csv_auto(
    'data/processed/test_scores_clean.csv'
);