-- KPI Tree: Activity → Output → Outcome → Impact
-- Aligned with Logical Framework, Theory of Change, and IRIS+ indicators

CREATE TABLE IF NOT EXISTS kpi_definitions (
    kpi_id SERIAL PRIMARY KEY,
    level VARCHAR(20) NOT NULL CHECK (level IN ('activity', 'output', 'outcome', 'impact')),
    kpi_code VARCHAR(50) NOT NULL UNIQUE,
    kpi_name VARCHAR(255) NOT NULL,
    description TEXT,
    iris_indicator VARCHAR(100),
    parent_kpi_code VARCHAR(50),
    unit VARCHAR(50),
    target_value NUMERIC(12,2)
);

INSERT INTO kpi_definitions (level, kpi_code, kpi_name, description, iris_indicator, parent_kpi_code, unit, target_value)
VALUES
    -- ACTIVITY (inputs & actions)
    ('activity', 'ACT_SESSIONS', 'Field Sessions Delivered', 'Number of classroom, workshop, and counselling sessions conducted', 'OD5755', NULL, 'sessions', 5000),
    ('activity', 'ACT_SUBMISSIONS', 'Field Data Submissions', 'Data batches received from field coordinators', NULL, NULL, 'submissions', 12),
    ('activity', 'ACT_SPEND', 'Programme Expenditure', 'Total funds deployed across programmes', 'FP0401', NULL, 'INR', 580000),

    -- OUTPUT (direct deliverables)
    ('output', 'OUT_ENROLLED', 'Beneficiaries Enrolled', 'Students registered in programmes', 'OD5755', 'ACT_SESSIONS', 'people', 800),
    ('output', 'OUT_ATTENDANCE', 'Attendance Records', 'Session attendance events logged', 'OD5755', 'ACT_SESSIONS', 'records', 6000),
    ('output', 'OUT_ASSESSED', 'Assessments Completed', 'Pre/post learning tests administered', 'OD5755', 'ACT_SESSIONS', 'assessments', 500),

    -- OUTCOME (short-term changes)
    ('outcome', 'OUT_ATT_RATE', 'Attendance Rate', 'Share of scheduled sessions attended', 'OD5755', 'OUT_ATTENDANCE', '%', 75),
    ('outcome', 'OUT_LEARN_GAIN', 'Average Learning Gain', 'Mean improvement in assessment scores', 'OD5755', 'OUT_ASSESSED', 'points', 12),
    ('outcome', 'OUT_RETENTION', 'Active Beneficiary Rate', 'Share of enrolled beneficiaries still active', 'OD5755', 'OUT_ENROLLED', '%', 80),

    -- IMPACT (long-term value & efficiency)
    ('impact', 'IMP_COST_BEN', 'Cost per Beneficiary', 'Spend divided by unique beneficiaries reached', 'FP0401', 'OUT_ENROLLED', 'INR/person', 725),
    ('impact', 'IMP_COST_LEARN', 'Cost per Learning Point', 'Spend per unit of learning gain achieved', 'FP0401', 'OUT_LEARN_GAIN', 'INR/point', 500),
    ('impact', 'IMP_REACH', 'Demographic Reach Index', 'Beneficiaries reached across districts and genders', 'OD5755', 'OUT_ENROLLED', 'index', 100),
    ('impact', 'IMP_EFFICIENCY', 'Impact Efficiency Score', 'Learning gain per ₹10,000 spent', 'FP0401', 'OUT_LEARN_GAIN', 'score', 1.5)
ON CONFLICT (kpi_code) DO NOTHING;

CREATE OR REPLACE VIEW vw_kpi_tree AS
WITH metrics AS (
    SELECT
        (SELECT COUNT(*) FROM field_attendance) AS sessions_delivered,
        (SELECT COUNT(*) FROM field_submissions) AS field_submissions,
        (SELECT COALESCE(SUM(amount), 0) FROM expenses) AS total_spend,
        (SELECT COUNT(DISTINCT beneficiary_id) FROM beneficiaries) AS enrolled,
        (SELECT COUNT(*) FROM field_attendance) AS attendance_records,
        (SELECT COUNT(*) FROM assessments) AS assessments_done,
        (SELECT ROUND(
            COUNT(CASE WHEN present THEN 1 END)::numeric / NULLIF(COUNT(*), 0) * 100, 2
        ) FROM field_attendance) AS attendance_rate,
        (SELECT ROUND(AVG(post_score - pre_score)::numeric, 2) FROM assessments) AS learning_gain,
        (SELECT ROUND(
            COUNT(CASE WHEN is_active THEN 1 END)::numeric / NULLIF(COUNT(*), 0) * 100, 2
        ) FROM beneficiaries) AS retention_rate,
        (SELECT ROUND(
            COALESCE(SUM(e.amount), 0) / NULLIF(COUNT(DISTINCT b.beneficiary_id), 0), 2
        ) FROM expenses e, beneficiaries b) AS cost_per_beneficiary,
        (SELECT ROUND(
            COALESCE(SUM(e.amount), 0) / NULLIF(SUM(a.post_score - a.pre_score), 0), 2
        ) FROM expenses e, assessments a) AS cost_per_learning_point,
        (SELECT COUNT(DISTINCT district || gender) FROM beneficiaries) AS reach_index,
        (SELECT ROUND(
            CASE WHEN COALESCE(SUM(e.amount), 0) = 0 THEN 0
            ELSE (COALESCE(AVG(asmt.post_score - asmt.pre_score), 0) / SUM(e.amount)) * 10000
            END::numeric, 4
        ) FROM expenses e, assessments asmt) AS efficiency_score
)
SELECT
    kd.level,
    kd.kpi_code,
    kd.kpi_name,
    kd.description,
    kd.iris_indicator,
    kd.parent_kpi_code,
    kd.unit,
    kd.target_value,
    CASE kd.kpi_code
        WHEN 'ACT_SESSIONS' THEN m.sessions_delivered
        WHEN 'ACT_SUBMISSIONS' THEN m.field_submissions
        WHEN 'ACT_SPEND' THEN m.total_spend
        WHEN 'OUT_ENROLLED' THEN m.enrolled
        WHEN 'OUT_ATTENDANCE' THEN m.attendance_records
        WHEN 'OUT_ASSESSED' THEN m.assessments_done
        WHEN 'OUT_ATT_RATE' THEN m.attendance_rate
        WHEN 'OUT_LEARN_GAIN' THEN m.learning_gain
        WHEN 'OUT_RETENTION' THEN m.retention_rate
        WHEN 'IMP_COST_BEN' THEN m.cost_per_beneficiary
        WHEN 'IMP_COST_LEARN' THEN m.cost_per_learning_point
        WHEN 'IMP_REACH' THEN m.reach_index
        WHEN 'IMP_EFFICIENCY' THEN m.efficiency_score
        ELSE NULL
    END AS actual_value,
    CASE
        WHEN kd.target_value IS NULL OR kd.target_value = 0 THEN NULL
        ELSE ROUND(
            (CASE kd.kpi_code
                WHEN 'ACT_SESSIONS' THEN m.sessions_delivered
                WHEN 'ACT_SUBMISSIONS' THEN m.field_submissions
                WHEN 'ACT_SPEND' THEN m.total_spend
                WHEN 'OUT_ENROLLED' THEN m.enrolled
                WHEN 'OUT_ATTENDANCE' THEN m.attendance_records
                WHEN 'OUT_ASSESSED' THEN m.assessments_done
                WHEN 'OUT_ATT_RATE' THEN m.attendance_rate
                WHEN 'OUT_LEARN_GAIN' THEN m.learning_gain
                WHEN 'OUT_RETENTION' THEN m.retention_rate
                WHEN 'IMP_COST_BEN' THEN m.cost_per_beneficiary
                WHEN 'IMP_COST_LEARN' THEN m.cost_per_learning_point
                WHEN 'IMP_REACH' THEN m.reach_index
                WHEN 'IMP_EFFICIENCY' THEN m.efficiency_score
                ELSE NULL
            END / kd.target_value) * 100, 1
        )
    END AS progress_pct
FROM kpi_definitions kd
CROSS JOIN metrics m
ORDER BY
    CASE kd.level
        WHEN 'activity' THEN 1
        WHEN 'output' THEN 2
        WHEN 'outcome' THEN 3
        WHEN 'impact' THEN 4
    END,
    kd.kpi_id;

CREATE OR REPLACE VIEW vw_monthly_trends AS
SELECT
    DATE_TRUNC('month', visit_date)::date AS month,
    COUNT(DISTINCT beneficiary_id) AS active_beneficiaries,
    COUNT(*) AS sessions_held,
    ROUND(AVG(CASE WHEN present THEN 1 ELSE 0 END)::numeric * 100, 2) AS attendance_rate
FROM field_attendance
GROUP BY DATE_TRUNC('month', visit_date)
ORDER BY month;

CREATE OR REPLACE VIEW vw_learning_trends AS
SELECT
    DATE_TRUNC('month', assessment_date)::date AS month,
    COUNT(*) AS assessments,
    ROUND(AVG(pre_score)::numeric, 2) AS avg_pre_score,
    ROUND(AVG(post_score)::numeric, 2) AS avg_post_score,
    ROUND(AVG(post_score - pre_score)::numeric, 2) AS avg_gain
FROM assessments
GROUP BY DATE_TRUNC('month', assessment_date)
ORDER BY month;

CREATE OR REPLACE VIEW vw_spend_trends AS
SELECT
    DATE_TRUNC('month', expense_date)::date AS month,
    SUM(amount) AS total_spend,
    COUNT(*) AS expense_count
FROM expenses
GROUP BY DATE_TRUNC('month', expense_date)
ORDER BY month;
