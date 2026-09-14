-- ============================================================
-- Student Retention & Welfare Tracker
-- School-Level KPI Views
-- ============================================================


-- ------------------------------------------------------------
-- 1. School Attendance KPI
-- ------------------------------------------------------------

CREATE OR REPLACE VIEW school_attendance_kpi AS
SELECT
    school_id,

    AVG(attendance_rate) AS avg_attendance_rate,

    COUNT(*) AS total_attendance_records,

    SUM(
        CASE
            WHEN proxy_attendance_flag = 1 THEN 1
            ELSE 0
        END
    ) AS proxy_attendance_records,

    (
        100.0 *
        SUM(
            CASE
                WHEN proxy_attendance_flag = 1 THEN 1
                ELSE 0
            END
        ) / NULLIF(COUNT(*), 0)
    ) AS proxy_attendance_rate,

    SUM(
        CASE
            WHEN attendance_count_anomaly = 1 THEN 1
            ELSE 0
        END
    ) AS count_anomaly_records,

    (
        100.0 *
        SUM(
            CASE
                WHEN attendance_count_anomaly = 1 THEN 1
                ELSE 0
            END
        ) / NULLIF(COUNT(*), 0)
    ) AS count_anomaly_rate,

    AVG(total_students) AS avg_total_students,

    AVG(present_students) AS avg_present_students

FROM attendance
GROUP BY school_id;


-- ------------------------------------------------------------
-- 2. School MDM KPI
-- ------------------------------------------------------------

CREATE OR REPLACE VIEW school_mdm_kpi AS

WITH mdm_summary AS (
    SELECT
        school_id,

        SUM(quantity) AS total_mdm_quantity_kg,

        COUNT(*) AS total_mdm_records,

        SUM(total_cost) AS total_mdm_cost,

        AVG(total_cost) AS avg_mdm_cost,

        COUNT(DISTINCT vendor_name) AS unique_vendors,

        COUNT(DISTINCT grain_type) AS unique_grain_types

    FROM mdm
    GROUP BY school_id
),

max_records AS (
    SELECT
        MAX(total_mdm_records) AS max_mdm_records
    FROM mdm_summary
)

SELECT
    m.school_id,

    m.total_mdm_quantity_kg,

    m.total_mdm_records,

    m.total_mdm_cost,

    m.avg_mdm_cost,

    m.unique_vendors,

    m.unique_grain_types,

    (
        100.0 * m.total_mdm_records
        / NULLIF(x.max_mdm_records, 0)
    ) AS mdm_regularity_rate

FROM mdm_summary m
CROSS JOIN max_records x;


-- ------------------------------------------------------------
-- 3. School Infrastructure KPI
-- ------------------------------------------------------------

CREATE OR REPLACE VIEW school_infrastructure_kpi AS

WITH school_infrastructure AS (
    SELECT
        school_id,

        AVG(has_electricity) AS has_electricity,

        AVG(has_drinking_water) AS has_drinking_water,

        AVG(has_functional_toilet) AS has_functional_toilet,

        AVG(has_boundary_wall) AS has_boundary_wall,

        AVG(has_playground) AS has_playground

    FROM infrastructure
    GROUP BY school_id
),

infrastructure_summary AS (
    SELECT
        school_id,

        has_electricity,

        has_drinking_water,

        has_functional_toilet,

        has_boundary_wall,

        has_playground,

        (
            CASE
                WHEN has_electricity IS NOT NULL THEN 1
                ELSE 0
            END

            + CASE
                WHEN has_drinking_water IS NOT NULL THEN 1
                ELSE 0
            END

            + CASE
                WHEN has_functional_toilet IS NOT NULL THEN 1
                ELSE 0
            END

            + CASE
                WHEN has_boundary_wall IS NOT NULL THEN 1
                ELSE 0
            END

            + CASE
                WHEN has_playground IS NOT NULL THEN 1
                ELSE 0
            END
        ) AS assessed_facilities,

        COALESCE(has_electricity, 0)
        + COALESCE(has_drinking_water, 0)
        + COALESCE(has_functional_toilet, 0)
        + COALESCE(has_boundary_wall, 0)
        + COALESCE(has_playground, 0)
        AS functional_facilities

    FROM school_infrastructure
)

SELECT
    school_id,

    has_electricity,

    has_drinking_water,

    has_functional_toilet,

    has_boundary_wall,

    has_playground,

    assessed_facilities,

    functional_facilities,

    (
        100.0 *
        (assessed_facilities - functional_facilities)
        / NULLIF(assessed_facilities, 0)
    ) AS infrastructure_deficit_index

FROM infrastructure_summary;


-- ------------------------------------------------------------
-- 4. School Test Score KPI
-- ------------------------------------------------------------

CREATE OR REPLACE VIEW school_test_score_kpi AS
SELECT
    school_id,

    AVG(score_percentage) AS average_test_score,

    COUNT(*) AS total_assessments,

    COUNT(DISTINCT subject) AS subjects_assessed

FROM test_scores
GROUP BY school_id;