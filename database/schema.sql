-- ============================================================
-- Oracle Fusion AI Agent POC — Database Schema
-- PostgreSQL 15
-- ============================================================

-- Table 1: hcm_employees
CREATE TABLE IF NOT EXISTS hcm_employees (
    employee_id      SERIAL PRIMARY KEY,
    full_name        VARCHAR(100) NOT NULL,
    department       VARCHAR(50) NOT NULL,
    job_title        VARCHAR(100),
    grade_level      VARCHAR(10),
    salary           NUMERIC(12,2),
    hire_date        DATE,
    termination_date DATE,
    employment_status VARCHAR(20) NOT NULL DEFAULT 'ACTIVE',
    location         VARCHAR(50),
    manager_id       INTEGER REFERENCES hcm_employees(employee_id),
    created_at       TIMESTAMP DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_hcm_dept ON hcm_employees(department);
CREATE INDEX IF NOT EXISTS idx_hcm_status ON hcm_employees(employment_status);

-- Table 2: finance_gl_balances
CREATE TABLE IF NOT EXISTS finance_gl_balances (
    balance_id       SERIAL PRIMARY KEY,
    cost_centre      VARCHAR(20) NOT NULL,
    cost_centre_name VARCHAR(100),
    account_code     VARCHAR(20),
    account_name     VARCHAR(100),
    period_name      VARCHAR(20),
    actual_amount    NUMERIC(15,2),
    budget_amount    NUMERIC(15,2),
    currency         VARCHAR(3) DEFAULT 'GBP',
    fiscal_year      INTEGER,
    fiscal_quarter   INTEGER,
    created_at       TIMESTAMP DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_gl_period ON finance_gl_balances(period_name);
CREATE INDEX IF NOT EXISTS idx_gl_cc ON finance_gl_balances(cost_centre);

-- Table 3: finance_ap_invoices
CREATE TABLE IF NOT EXISTS finance_ap_invoices (
    invoice_id       SERIAL PRIMARY KEY,
    invoice_number   VARCHAR(50) UNIQUE,
    supplier_id      INTEGER,
    supplier_name    VARCHAR(100),
    invoice_date     DATE,
    due_date         DATE,
    invoice_amount   NUMERIC(15,2),
    paid_amount      NUMERIC(15,2) DEFAULT 0,
    outstanding_amount NUMERIC(15,2),
    status           VARCHAR(20),
    cost_centre      VARCHAR(20),
    currency         VARCHAR(3) DEFAULT 'GBP',
    created_at       TIMESTAMP DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_ap_status ON finance_ap_invoices(status);
CREATE INDEX IF NOT EXISTS idx_ap_due ON finance_ap_invoices(due_date);

-- Table 4: procurement_quotations
CREATE TABLE IF NOT EXISTS procurement_quotations (
    quotation_id     SERIAL PRIMARY KEY,
    engagement_id    VARCHAR(30) NOT NULL,
    engagement_name  VARCHAR(200),
    supplier_name    VARCHAR(100),
    original_amount  NUMERIC(15,2),
    revised_amount   NUMERIC(15,2),
    quotation_version INTEGER DEFAULT 1,
    status           VARCHAR(20),
    submission_date  DATE,
    category         VARCHAR(50),
    created_at       TIMESTAMP DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_quot_engagement ON procurement_quotations(engagement_id);

-- Table 5: procurement_purchase_orders
CREATE TABLE IF NOT EXISTS procurement_purchase_orders (
    po_id            SERIAL PRIMARY KEY,
    po_number        VARCHAR(50) UNIQUE,
    supplier_name    VARCHAR(100),
    total_amount     NUMERIC(15,2),
    approved_amount  NUMERIC(15,2),
    status           VARCHAR(20),
    created_date     DATE,
    approved_date    DATE,
    cost_centre      VARCHAR(20),
    category         VARCHAR(50),
    created_at       TIMESTAMP DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_po_status ON procurement_purchase_orders(status);

-- Table 6: ai_query_log
CREATE TABLE IF NOT EXISTS ai_query_log (
    log_id           SERIAL PRIMARY KEY,
    user_query       TEXT,
    detected_domain  VARCHAR(30),
    generated_sql    TEXT,
    response_summary TEXT,
    execution_time_ms INTEGER,
    created_at       TIMESTAMP DEFAULT NOW()
);
