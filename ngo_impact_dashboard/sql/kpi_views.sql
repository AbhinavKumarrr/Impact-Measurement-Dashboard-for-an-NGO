CREATE OR REPLACE VIEW vw_executive_overview AS
SELECT
    p.program_id,
    p.program_name,
    COUNT(DISTINCT b.beneficiary_id) AS total_beneficiaries,
    COUNT(DISTINCT a.attendance_id) AS total_attendance_records,
    COUNT(DISTINCT asmt.assessment_id) AS total_assessments,
    COALESCE(SUM(e.amount), 0) AS total_spend,
    ROUND(
        COALESCE(AVG(asmt.post_score - asmt.pre_score), 0)::numeric, 2
    ) AS avg_learning_gain,
    ROUND(
        CASE 
            WHEN COALESCE(SUM(e.amount), 0) = 0 THEN 0
            ELSE (COALESCE(AVG(asmt.post_score - asmt.pre_score), 0) / SUM(e.amount)) * 10000
        END::numeric, 4
    ) AS impact_efficiency_score
FROM programs p
LEFT JOIN beneficiaries b ON p.program_id = b.program_id
LEFT JOIN field_attendance a ON b.beneficiary_id = a.beneficiary_id
LEFT JOIN assessments asmt ON b.beneficiary_id = asmt.beneficiary_id
LEFT JOIN expenses e ON p.program_id = e.program_id
GROUP BY p.program_id, p.program_name;

CREATE OR REPLACE VIEW vw_demographic_reach AS
SELECT
    district,
    gender,
    COUNT(*) AS beneficiaries_reached,
    ROUND(AVG(age)::numeric, 2) AS avg_age
FROM beneficiaries
GROUP BY district, gender;

CREATE OR REPLACE VIEW vw_program_progress AS
SELECT
    p.program_name,
    COUNT(DISTINCT b.beneficiary_id) AS enrolled,
    COUNT(DISTINCT CASE WHEN a.present = TRUE THEN a.attendance_id END) AS attended_sessions,
    COUNT(DISTINCT asmt.assessment_id) AS assessed_students,
    ROUND(
        (COUNT(DISTINCT CASE WHEN a.present = TRUE THEN a.attendance_id END)::numeric
        / NULLIF(COUNT(DISTINCT a.attendance_id), 0)) * 100, 2
    ) AS attendance_rate,
    ROUND(
        AVG(asmt.post_score - asmt.pre_score)::numeric, 2
    ) AS avg_test_score_gain
FROM programs p
LEFT JOIN beneficiaries b ON p.program_id = b.program_id
LEFT JOIN field_attendance a ON b.beneficiary_id = a.beneficiary_id
LEFT JOIN assessments asmt ON b.beneficiary_id = asmt.beneficiary_id
GROUP BY p.program_name;

CREATE OR REPLACE VIEW vw_cost_per_impact AS
SELECT
    p.program_name,
    COALESCE(SUM(e.amount), 0) AS total_spend,
    COUNT(DISTINCT b.beneficiary_id) AS beneficiaries,
    ROUND(
        COALESCE(SUM(e.amount), 0) / NULLIF(COUNT(DISTINCT b.beneficiary_id), 0),
        2
    ) AS cost_per_beneficiary,
    ROUND(
        COALESCE(SUM(e.amount), 0) / NULLIF(SUM(asmt.post_score - asmt.pre_score), 0),
        2
    ) AS cost_per_learning_point
FROM programs p
LEFT JOIN beneficiaries b ON p.program_id = b.program_id
LEFT JOIN assessments asmt ON b.beneficiary_id = asmt.beneficiary_id
LEFT JOIN expenses e ON p.program_id = e.program_id
GROUP BY p.program_name;

CREATE OR REPLACE VIEW vw_data_quality AS
SELECT
    COUNT(*) AS total_submissions,
    SUM(total_records) AS total_records,
    SUM(invalid_records) AS invalid_records,
    SUM(duplicate_records) AS duplicate_records,
    ROUND(
        (SUM(total_records) - SUM(invalid_records) - SUM(duplicate_records))::numeric
        / NULLIF(SUM(total_records), 0) * 100, 2
    ) AS data_quality_score
FROM field_submissions;