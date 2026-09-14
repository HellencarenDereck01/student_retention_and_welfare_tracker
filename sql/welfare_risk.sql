-- ============================================================
-- Student Retention & Welfare Tracker
-- Student Welfare Risk
-- ============================================================


-- ------------------------------------------------------------
-- Student Welfare Risk View
-- ------------------------------------------------------------

CREATE OR REPLACE VIEW school_welfare_risk AS

WITH risk_base AS (

    SELECT
        s.school_id,
        s.school_name,
        s.district,
        s.block,

        a.avg_attendance_rate,
        a.proxy_attendance_rate,
        a.count_anomaly_rate,

        m.mdm_regularity_rate,

        i.infrastructure_deficit_index,

        t.average_test_score

    FROM school_master s

    LEFT JOIN school_attendance_kpi a
        ON s.school_id = a.school_id

    LEFT JOIN school_mdm_kpi m
        ON s.school_id = m.school_id

    LEFT JOIN school_infrastructure_kpi i
        ON s.school_id = i.school_id

    LEFT JOIN school_test_score_kpi t
        ON s.school_id = t.school_id
),

risk_flags AS (

    SELECT
        *,

        CASE
            WHEN avg_attendance_rate < 79.93 THEN 1
            ELSE 0
        END AS low_attendance_flag,

        CASE
            WHEN proxy_attendance_rate > 6.90 THEN 1
            ELSE 0
        END AS high_proxy_flag,

        CASE
            WHEN count_anomaly_rate > 6.06 THEN 1
            ELSE 0
        END AS high_count_anomaly_flag,

        CASE
            WHEN mdm_regularity_rate < 51.52 THEN 1
            ELSE 0
        END AS low_mdm_regularity_flag,

        CASE
            WHEN infrastructure_deficit_index > 35.94 THEN 1
            ELSE 0
        END AS high_infrastructure_deficit_flag,

        CASE
            WHEN average_test_score < 63.41 THEN 1
            ELSE 0
        END AS low_test_score_flag

    FROM risk_base
)

SELECT
    *,

    (
        low_attendance_flag
        + high_proxy_flag
        + high_count_anomaly_flag
        + low_mdm_regularity_flag
        + high_infrastructure_deficit_flag
        + low_test_score_flag
    ) AS student_welfare_risk_score,

    CASE
        WHEN (
            low_attendance_flag
            + high_proxy_flag
            + high_count_anomaly_flag
            + low_mdm_regularity_flag
            + high_infrastructure_deficit_flag
            + low_test_score_flag
        ) <= 1
        THEN 'Low'

        WHEN (
            low_attendance_flag
            + high_proxy_flag
            + high_count_anomaly_flag
            + low_mdm_regularity_flag
            + high_infrastructure_deficit_flag
            + low_test_score_flag
        ) <= 3
        THEN 'Moderate'

        ELSE 'High'
    END AS risk_level

FROM risk_flags;