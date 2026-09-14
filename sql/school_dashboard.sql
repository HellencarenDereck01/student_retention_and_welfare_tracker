-- ============================================================
-- Student Retention & Welfare Tracker
-- Final School Dashboard View
-- ============================================================


-- ------------------------------------------------------------
-- Final one-row-per-school dashboard dataset
-- ------------------------------------------------------------

CREATE OR REPLACE VIEW school_dashboard AS

SELECT
    -- School information
    s.school_id,
    s.school_name,
    s.district,
    s.block,
    s.total_enrolled_students,
    s.school_type,
    s.medium,

    -- Attendance KPIs
    a.avg_attendance_rate,
    a.total_attendance_records,
    a.proxy_attendance_records,
    a.proxy_attendance_rate,
    a.count_anomaly_records,
    a.count_anomaly_rate,

    -- MDM KPIs
    m.total_mdm_quantity_kg,
    m.total_mdm_records,
    m.total_mdm_cost,
    m.avg_mdm_cost,
    m.mdm_regularity_rate,
    m.unique_vendors,
    m.unique_grain_types,

    -- Infrastructure KPIs
    i.assessed_facilities,
    i.functional_facilities,
    i.infrastructure_deficit_index,

    -- Test-score KPIs
    t.average_test_score,
    t.total_assessments,
    t.subjects_assessed,

    -- Welfare risk
    r.student_welfare_risk_score,
    r.risk_level

FROM school_master s

LEFT JOIN school_attendance_kpi a
    ON s.school_id = a.school_id

LEFT JOIN school_mdm_kpi m
    ON s.school_id = m.school_id

LEFT JOIN school_infrastructure_kpi i
    ON s.school_id = i.school_id

LEFT JOIN school_test_score_kpi t
    ON s.school_id = t.school_id

LEFT JOIN school_welfare_risk r
    ON s.school_id = r.school_id;