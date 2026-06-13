CREATE TABLE IF NOT EXISTS ngos (
    ngo_id SERIAL PRIMARY KEY,
    ngo_name VARCHAR(255) NOT NULL,
    sector VARCHAR(100) NOT NULL,
    city VARCHAR(100),
    state VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS programs (
    program_id SERIAL PRIMARY KEY,
    ngo_id INT REFERENCES ngos(ngo_id) ON DELETE CASCADE,
    program_name VARCHAR(255) NOT NULL,
    program_type VARCHAR(100) NOT NULL,
    start_date DATE,
    end_date DATE,
    budget_allocated NUMERIC(12,2) DEFAULT 0
);

CREATE TABLE IF NOT EXISTS beneficiaries (
    beneficiary_id SERIAL PRIMARY KEY,
    ngo_id INT REFERENCES ngos(ngo_id) ON DELETE CASCADE,
    program_id INT REFERENCES programs(program_id) ON DELETE SET NULL,
    beneficiary_name VARCHAR(255),
    gender VARCHAR(20),
    age INT,
    district VARCHAR(100),
    village VARCHAR(100),
    enrollment_date DATE,
    is_active BOOLEAN DEFAULT TRUE
);

CREATE TABLE IF NOT EXISTS field_attendance (
    attendance_id SERIAL PRIMARY KEY,
    beneficiary_id INT REFERENCES beneficiaries(beneficiary_id) ON DELETE CASCADE,
    program_id INT REFERENCES programs(program_id) ON DELETE CASCADE,
    visit_date DATE NOT NULL,
    present BOOLEAN NOT NULL,
    session_type VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS assessments (
    assessment_id SERIAL PRIMARY KEY,
    beneficiary_id INT REFERENCES beneficiaries(beneficiary_id) ON DELETE CASCADE,
    program_id INT REFERENCES programs(program_id) ON DELETE CASCADE,
    assessment_date DATE NOT NULL,
    pre_score NUMERIC(5,2),
    post_score NUMERIC(5,2),
    score_type VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS expenses (
    expense_id SERIAL PRIMARY KEY,
    program_id INT REFERENCES programs(program_id) ON DELETE CASCADE,
    expense_date DATE NOT NULL,
    category VARCHAR(100),
    amount NUMERIC(12,2) NOT NULL,
    vendor VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS field_submissions (
    submission_id SERIAL PRIMARY KEY,
    ngo_id INT REFERENCES ngos(ngo_id) ON DELETE CASCADE,
    submitted_by VARCHAR(255),
    submission_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    total_records INT,
    invalid_records INT,
    duplicate_records INT,
    notes TEXT
);