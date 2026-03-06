# Database Analysis — Oracle Fusion AI Agent POC

> Generated from live PostgreSQL database on 2026-03-06 (IST)

---

# DATABASE OVERVIEW

| Property | Value |
|---|---|
| Database name | `oracle_fusion_poc` |
| PostgreSQL version | PostgreSQL 15.17, compiled by Visual C++ build 1944, 64-bit |
| Total tables | 64 |
| Total rows (all tables) | 240,185 |
| Domains | HCM (22), Finance (23+), Procurement (17), Supplier (3) |

---

# TABLE INVENTORY

| Table | Rows | Domain | Description |
|---|---|---|---|
| `ai_query_log` | 152 | System | AI agent query audit log |
| `fin_account_codes` | 4,000 | Finance | Account code master |
| `fin_ap_invoice_distributions` | 4,000 | Finance | AP invoice accounting distributions to cost centres |
| `fin_ap_invoice_lines` | 4,000 | Finance | AP invoice line items with po_line_id (3-way match) |
| `fin_ap_invoices` | 4,000 | Finance | AP invoices with invoice_amount, supplier_id, status, due_date |
| `fin_ap_payment_schedules` | 4,000 | Finance | AP payment schedules per invoice |
| `fin_ap_payments` | 4,000 | Finance | AP payment records — payment_amount, supplier_id (NO invoice_id FK) |
| `fin_ar_customers` | 4,000 | Finance | Accounts receivable customer master |
| `fin_ar_invoices` | 4,000 | Finance | AR invoices with invoice_amount, customer_id, outstanding |
| `fin_ar_receipts` | 4,000 | Finance | AR customer payment receipts |
| `fin_budget_headers` | 4,000 | Finance | Budget header per ledger — fiscal_year and total_amount only |
| `fin_budget_lines` | 4,000 | Finance | Budget line amounts at cost centre + account level — PRIMARY budget table |
| `fin_budget_versions` | 4,000 | Finance | Budget version control (original/revised/forecast) |
| `fin_chart_of_accounts` | 4,000 | Finance | Chart of accounts structure |
| `fin_coa_segments` | 4,000 | Finance | COA segment definitions |
| `fin_cost_centres` | 4,000 | Finance | Cost centre master — bridge between HCM and Finance |
| `fin_currency_rates` | 4,000 | Finance | Currency exchange rates |
| `fin_gl_balances` | 4,000 | Finance | GL summary balances: period_debit/credit/net, begin/end_balance, fiscal_year |
| `fin_gl_journal_headers` | 4,000 | Finance | GL journal entry headers |
| `fin_gl_journal_lines` | 4,000 | Finance | GL journal line items with account + cost centre |
| `fin_ledgers` | 4,000 | Finance | General ledger definitions |
| `fin_reporting_periods` | 4,000 | Finance | Fiscal reporting periods with fiscal_year and dates |
| `hcm_assignments` | 4,000 | HCM | ALL org context: dept, grade, salary, job — primary HCM table |
| `hcm_compensation_elements` | 4,000 | HCM | Base/bonus/allowance pay components |
| `hcm_cost_allocations` | 4,000 | HCM | Assignment cost allocation to fin_cost_centres (cross-domain bridge) |
| `hcm_departments` | 4,000 | HCM | Department master — has cost_centre_code VARCHAR (not FK to fin_cost_centres) |
| `hcm_employment_periods` | 4,000 | HCM | Hire to terminate date spans |
| `hcm_grades` | 4,000 | HCM | Grade salary bands (min/mid/max) |
| `hcm_jobs` | 4,000 | HCM | Job catalog and job families |
| `hcm_locations` | 4,000 | HCM | Office and work locations |
| `hcm_organizations` | 4 | HCM | Business units and legal entities |
| `hcm_payroll_results` | 4,000 | HCM | Individual payroll results per assignment |
| `hcm_payroll_runs` | 4,000 | HCM | Payroll batch run headers |
| `hcm_performance_reviews` | 4,000 | HCM | Performance reviews linked to person |
| `hcm_person_emails` | 4,000 | HCM | Employee email addresses |
| `hcm_person_names` | 4,000 | HCM | Legal name change history |
| `hcm_persons` | 4,000 | HCM | Employee master: identity (no salary, no org context) |
| `hcm_positions` | 10 | HCM | Position definitions (slot in org chart) |
| `hcm_promotions` | 4,000 | HCM | Promotion history per assignment |
| `hcm_salary_history` | 4,000 | HCM | Salary change history per assignment |
| `hcm_termination_reasons` | 4,000 | HCM | Termination reason lookup |
| `hcm_training_records` | 4,000 | HCM | Training and certification records |
| `hcm_transfers` | 4,000 | HCM | Transfer history per assignment |
| `hcm_workforce_actions` | 4,000 | HCM | Hire/transfer/promote/terminate lifecycle actions |
| `proc_contract_headers` | 4,000 | Procurement | Blanket purchase contracts with supplier |
| `proc_contract_lines` | 4,000 | Procurement | Contract line items |
| `proc_item_categories` | 4,000 | Procurement | Item category hierarchy (self-referencing) |
| `proc_items` | 4,000 | Procurement | Item/service catalog with unit_price |
| `proc_po_approvals` | 4,000 | Procurement | PO approval workflow |
| `proc_po_distributions` | 4,000 | Procurement | PO accounting distributions: amount, cost_centre_id — PRIMARY spend table |
| `proc_po_headers` | 4,000 | Procurement | PO headers: supplier_id, total_amount, status — NO cost_centre_id |
| `proc_po_lines` | 4,000 | Procurement | PO line items: quantity, unit_price, line_amount |
| `proc_quotation_headers` | 4,000 | Procurement | Supplier quotation (RFQ) headers with engagement_id |
| `proc_quotation_lines` | 4,000 | Procurement | Quotation line items |
| `proc_quote_versions` | 4,000 | Procurement | Quotation version history (audit trail) |
| `proc_receipt_headers` | 4,000 | Procurement | Goods receipt headers linked to PO |
| `proc_receipt_lines` | 4,000 | Procurement | Goods receipt lines matched to PO lines |
| `proc_requisition_distributions` | 4,000 | Procurement | Requisition accounting distributions to cost centres |
| `proc_requisition_headers` | 4,000 | Procurement | Purchase requisition headers with total_amount |
| `proc_requisition_lines` | 4,000 | Procurement | Requisition line items |
| `schema_embeddings` | 19 | System | PGVector embeddings of schema documentation (AI RAG) |
| `sup_supplier_contacts` | 4,000 | Procurement | Supplier contact persons |
| `sup_supplier_sites` | 4,000 | Procurement | Supplier site addresses |
| `sup_suppliers` | 4,000 | Procurement | Unified supplier/vendor master for AP and Procurement |

---

# FULL TABLE STRUCTURE

## `ai_query_log`

**Rows:** 152  |  **Purpose:** AI agent query audit log

| Column | Type | Nullable | Default | Notes |
|---|---|---|---|---|
| `log_id` | integer | NO | nextval('ai_query_log_log_id_s | **PK** |
| `user_query` | text | YES |  |  |
| `detected_domain` | varchar(30) | YES |  |  |
| `generated_sql` | text | YES |  |  |
| `response_summary` | text | YES |  |  |
| `execution_time_ms` | integer | YES |  |  |
| `created_at` | timestamp | YES | now() |  |

## `fin_account_codes`

**Rows:** 4,000  |  **Purpose:** Account code master

| Column | Type | Nullable | Default | Notes |
|---|---|---|---|---|
| `account_code_id` | integer | NO | nextval('fin_account_codes_acc | **PK** |
| `account_code` | varchar(20) | NO |  |  |
| `account_name` | varchar(100) | NO |  |  |
| `account_type` | varchar(30) | NO |  |  |
| `parent_account_code` | varchar(20) | YES |  |  |
| `coa_id` | integer | YES |  |  |
| `status` | varchar(20) | YES | 'ACTIVE'::character varying |  |
| `created_at` | timestamp | YES | now() |  |

## `fin_ap_invoice_distributions`

**Rows:** 4,000  |  **Purpose:** AP invoice accounting distributions to cost centres

| Column | Type | Nullable | Default | Notes |
|---|---|---|---|---|
| `distribution_id` | integer | NO | nextval('fin_ap_invoice_distri | **PK** |
| `invoice_line_id` | integer | YES |  |  |
| `cost_centre_id` | integer | YES |  |  |
| `account_code_id` | integer | YES |  |  |
| `distribution_pct` | numeric(5,2) | YES | 100.00 |  |
| `amount` | numeric(12,2) | YES |  |  |
| `created_at` | timestamp | YES | now() |  |

## `fin_ap_invoice_lines`

**Rows:** 4,000  |  **Purpose:** AP invoice line items with po_line_id (3-way match)

| Column | Type | Nullable | Default | Notes |
|---|---|---|---|---|
| `invoice_line_id` | integer | NO | nextval('fin_ap_invoice_lines_ | **PK** |
| `invoice_id` | integer | YES |  |  |
| `line_number` | integer | NO |  |  |
| `description` | varchar(255) | YES |  |  |
| `quantity` | numeric(10,2) | YES | 1 |  |
| `unit_price` | numeric(12,2) | YES |  |  |
| `line_amount` | numeric(12,2) | YES |  |  |
| `po_line_id` | integer | YES |  |  |
| `created_at` | timestamp | YES | now() |  |

## `fin_ap_invoices`

**Rows:** 4,000  |  **Purpose:** AP invoices with invoice_amount, supplier_id, status, due_date

| Column | Type | Nullable | Default | Notes |
|---|---|---|---|---|
| `invoice_id` | integer | NO | nextval('fin_ap_invoices_invoi | **PK** |
| `invoice_number` | varchar(50) | NO |  |  |
| `supplier_id` | integer | YES |  |  |
| `ledger_id` | integer | YES |  |  |
| `invoice_date` | date | NO |  |  |
| `due_date` | date | YES |  |  |
| `invoice_amount` | numeric(15,2) | NO |  |  |
| `paid_amount` | numeric(15,2) | YES | 0 |  |
| `outstanding_amount` | numeric(15,2) | YES |  |  |
| `currency` | varchar(3) | YES | 'GBP'::character varying |  |
| `status` | varchar(20) | YES | 'PENDING'::character varying |  |
| `created_by` | integer | YES |  |  |
| `approved_by` | integer | YES |  |  |
| `created_at` | timestamp | YES | now() |  |
| `updated_at` | timestamp | YES | now() |  |

## `fin_ap_payment_schedules`

**Rows:** 4,000  |  **Purpose:** AP payment schedules per invoice

| Column | Type | Nullable | Default | Notes |
|---|---|---|---|---|
| `schedule_id` | integer | NO | nextval('fin_ap_payment_schedu | **PK** |
| `invoice_id` | integer | YES |  |  |
| `installment_num` | integer | YES | 1 |  |
| `due_date` | date | NO |  |  |
| `amount_due` | numeric(12,2) | NO |  |  |
| `amount_paid` | numeric(12,2) | YES | 0 |  |
| `status` | varchar(20) | YES | 'OPEN'::character varying |  |
| `created_at` | timestamp | YES | now() |  |

## `fin_ap_payments`

**Rows:** 4,000  |  **Purpose:** AP payment records — payment_amount, supplier_id (NO invoice_id FK)

| Column | Type | Nullable | Default | Notes |
|---|---|---|---|---|
| `payment_id` | integer | NO | nextval('fin_ap_payments_payme | **PK** |
| `payment_number` | varchar(30) | NO |  |  |
| `supplier_id` | integer | YES |  |  |
| `payment_date` | date | NO |  |  |
| `payment_amount` | numeric(15,2) | NO |  |  |
| `payment_method` | varchar(20) | YES | 'BACS'::character varying |  |
| `reference` | varchar(50) | YES |  |  |
| `status` | varchar(20) | YES | 'COMPLETED'::character varying |  |
| `created_at` | timestamp | YES | now() |  |

## `fin_ar_customers`

**Rows:** 4,000  |  **Purpose:** Accounts receivable customer master

| Column | Type | Nullable | Default | Notes |
|---|---|---|---|---|
| `customer_id` | integer | NO | nextval('fin_ar_customers_cust | **PK** |
| `customer_number` | varchar(20) | NO |  |  |
| `customer_name` | varchar(150) | NO |  |  |
| `customer_type` | varchar(30) | YES |  |  |
| `payment_terms` | varchar(30) | YES | 'NET30'::character varying |  |
| `credit_limit` | numeric(15,2) | YES |  |  |
| `contact_name` | varchar(100) | YES |  |  |
| `contact_email` | varchar(150) | YES |  |  |
| `country` | varchar(50) | YES | 'United Kingdom'::character va |  |
| `status` | varchar(20) | YES | 'ACTIVE'::character varying |  |
| `created_at` | timestamp | YES | now() |  |

## `fin_ar_invoices`

**Rows:** 4,000  |  **Purpose:** AR invoices with invoice_amount, customer_id, outstanding

| Column | Type | Nullable | Default | Notes |
|---|---|---|---|---|
| `ar_invoice_id` | integer | NO | nextval('fin_ar_invoices_ar_in | **PK** |
| `invoice_number` | varchar(50) | NO |  |  |
| `customer_id` | integer | YES |  |  |
| `invoice_date` | date | NO |  |  |
| `due_date` | date | NO |  |  |
| `invoice_amount` | numeric(15,2) | NO |  |  |
| `paid_amount` | numeric(15,2) | YES | 0 |  |
| `outstanding` | numeric(15,2) | YES |  |  |
| `currency` | varchar(3) | YES | 'GBP'::character varying |  |
| `status` | varchar(20) | YES | 'OPEN'::character varying |  |
| `created_at` | timestamp | YES | now() |  |

## `fin_ar_receipts`

**Rows:** 4,000  |  **Purpose:** AR customer payment receipts

| Column | Type | Nullable | Default | Notes |
|---|---|---|---|---|
| `receipt_id` | integer | NO | nextval('fin_ar_receipts_recei | **PK** |
| `receipt_number` | varchar(30) | NO |  |  |
| `ar_invoice_id` | integer | YES |  |  |
| `receipt_date` | date | NO |  |  |
| `receipt_amount` | numeric(15,2) | NO |  |  |
| `payment_method` | varchar(20) | YES | 'BACS'::character varying |  |
| `status` | varchar(20) | YES | 'APPLIED'::character varying |  |
| `created_at` | timestamp | YES | now() |  |

## `fin_budget_headers`

**Rows:** 4,000  |  **Purpose:** Budget header per ledger — fiscal_year and total_amount only

| Column | Type | Nullable | Default | Notes |
|---|---|---|---|---|
| `budget_header_id` | integer | NO | nextval('fin_budget_headers_bu | **PK** |
| `budget_name` | varchar(100) | NO |  |  |
| `ledger_id` | integer | YES |  |  |
| `budget_version_id` | integer | YES |  |  |
| `fiscal_year` | integer | NO |  |  |
| `total_amount` | numeric(15,2) | YES |  |  |
| `status` | varchar(20) | YES | 'APPROVED'::character varying |  |
| `created_at` | timestamp | YES | now() |  |

## `fin_budget_lines`

**Rows:** 4,000  |  **Purpose:** Budget line amounts at cost centre + account level — PRIMARY budget table

| Column | Type | Nullable | Default | Notes |
|---|---|---|---|---|
| `budget_line_id` | integer | NO | nextval('fin_budget_lines_budg | **PK** |
| `budget_header_id` | integer | YES |  |  |
| `cost_centre_id` | integer | YES |  |  |
| `account_code_id` | integer | YES |  |  |
| `period_name` | varchar(20) | NO |  |  |
| `amount` | numeric(15,2) | NO |  |  |
| `created_at` | timestamp | YES | now() |  |

## `fin_budget_versions`

**Rows:** 4,000  |  **Purpose:** Budget version control (original/revised/forecast)

| Column | Type | Nullable | Default | Notes |
|---|---|---|---|---|
| `budget_version_id` | integer | NO | nextval('fin_budget_versions_b | **PK** |
| `version_name` | varchar(50) | NO |  |  |
| `version_type` | varchar(20) | YES | 'ORIGINAL'::character varying |  |
| `fiscal_year` | integer | NO |  |  |
| `status` | varchar(20) | YES | 'APPROVED'::character varying |  |
| `created_at` | timestamp | YES | now() |  |

## `fin_chart_of_accounts`

**Rows:** 4,000  |  **Purpose:** Chart of accounts structure

| Column | Type | Nullable | Default | Notes |
|---|---|---|---|---|
| `coa_id` | integer | NO | nextval('fin_chart_of_accounts | **PK** |
| `coa_code` | varchar(20) | NO |  |  |
| `coa_name` | varchar(100) | NO |  |  |
| `ledger_id` | integer | YES |  |  |
| `status` | varchar(20) | YES | 'ACTIVE'::character varying |  |
| `created_at` | timestamp | YES | now() |  |

## `fin_coa_segments`

**Rows:** 4,000  |  **Purpose:** COA segment definitions

| Column | Type | Nullable | Default | Notes |
|---|---|---|---|---|
| `segment_id` | integer | NO | nextval('fin_coa_segments_segm | **PK** |
| `coa_id` | integer | YES |  |  |
| `segment_name` | varchar(50) | NO |  |  |
| `segment_number` | integer | NO |  |  |
| `segment_type` | varchar(30) | YES |  |  |
| `value_set` | varchar(50) | YES |  |  |
| `created_at` | timestamp | YES | now() |  |

## `fin_cost_centres`

**Rows:** 4,000  |  **Purpose:** Cost centre master — bridge between HCM and Finance

| Column | Type | Nullable | Default | Notes |
|---|---|---|---|---|
| `cost_centre_id` | integer | NO | nextval('fin_cost_centres_cost | **PK** |
| `cost_centre_code` | varchar(20) | NO |  |  |
| `cost_centre_name` | varchar(100) | NO |  |  |
| `dept_id` | integer | YES |  |  |
| `manager_person_id` | integer | YES |  |  |
| `status` | varchar(20) | YES | 'ACTIVE'::character varying |  |
| `created_at` | timestamp | YES | now() |  |

## `fin_currency_rates`

**Rows:** 4,000  |  **Purpose:** Currency exchange rates

| Column | Type | Nullable | Default | Notes |
|---|---|---|---|---|
| `rate_id` | integer | NO | nextval('fin_currency_rates_ra | **PK** |
| `from_currency` | varchar(3) | NO |  |  |
| `to_currency` | varchar(3) | NO |  |  |
| `exchange_rate` | numeric(12,6) | NO |  |  |
| `rate_type` | varchar(20) | YES | 'SPOT'::character varying |  |
| `effective_date` | date | NO |  |  |
| `created_at` | timestamp | YES | now() |  |

## `fin_gl_balances`

**Rows:** 4,000  |  **Purpose:** GL summary balances: period_debit/credit/net, begin/end_balance, fiscal_year

| Column | Type | Nullable | Default | Notes |
|---|---|---|---|---|
| `balance_id` | integer | NO | nextval('fin_gl_balances_balan | **PK** |
| `cost_centre_id` | integer | YES |  |  |
| `account_code_id` | integer | YES |  |  |
| `period_name` | varchar(20) | NO |  |  |
| `fiscal_year` | integer | YES |  |  |
| `fiscal_quarter` | integer | YES |  |  |
| `period_debit` | numeric(15,2) | YES |  |  |
| `period_credit` | numeric(15,2) | YES |  |  |
| `period_net` | numeric(15,2) | YES |  |  |
| `begin_balance` | numeric(15,2) | YES |  |  |
| `end_balance` | numeric(15,2) | YES |  |  |
| `currency` | varchar(3) | YES | 'GBP'::character varying |  |
| `created_at` | timestamp | YES | now() |  |
| `actual_amount` | numeric(15,2) | YES |  |  |
| `budget_amount` | numeric(15,2) | YES |  |  |

## `fin_gl_journal_headers`

**Rows:** 4,000  |  **Purpose:** GL journal entry headers

| Column | Type | Nullable | Default | Notes |
|---|---|---|---|---|
| `journal_header_id` | integer | NO | nextval('fin_gl_journal_header | **PK** |
| `journal_number` | varchar(30) | NO |  |  |
| `journal_name` | varchar(150) | YES |  |  |
| `ledger_id` | integer | YES |  |  |
| `period_id` | integer | YES |  |  |
| `journal_date` | date | NO |  |  |
| `journal_source` | varchar(30) | YES |  |  |
| `journal_category` | varchar(30) | YES |  |  |
| `total_debit` | numeric(15,2) | YES |  |  |
| `total_credit` | numeric(15,2) | YES |  |  |
| `status` | varchar(20) | YES | 'POSTED'::character varying |  |
| `created_by` | integer | YES |  |  |
| `approved_by` | integer | YES |  |  |
| `created_at` | timestamp | YES | now() |  |

## `fin_gl_journal_lines`

**Rows:** 4,000  |  **Purpose:** GL journal line items with account + cost centre

| Column | Type | Nullable | Default | Notes |
|---|---|---|---|---|
| `journal_line_id` | integer | NO | nextval('fin_gl_journal_lines_ | **PK** |
| `journal_header_id` | integer | YES |  |  |
| `line_number` | integer | NO |  |  |
| `account_code_id` | integer | YES |  |  |
| `cost_centre_id` | integer | YES |  |  |
| `debit_amount` | numeric(15,2) | YES | 0 |  |
| `credit_amount` | numeric(15,2) | YES | 0 |  |
| `description` | varchar(255) | YES |  |  |
| `created_at` | timestamp | YES | now() |  |

## `fin_ledgers`

**Rows:** 4,000  |  **Purpose:** General ledger definitions

| Column | Type | Nullable | Default | Notes |
|---|---|---|---|---|
| `ledger_id` | integer | NO | nextval('fin_ledgers_ledger_id | **PK** |
| `ledger_code` | varchar(20) | NO |  |  |
| `ledger_name` | varchar(100) | NO |  |  |
| `currency` | varchar(3) | YES | 'GBP'::character varying |  |
| `calendar_type` | varchar(20) | YES | 'FISCAL'::character varying |  |
| `status` | varchar(20) | YES | 'ACTIVE'::character varying |  |
| `created_at` | timestamp | YES | now() |  |

## `fin_reporting_periods`

**Rows:** 4,000  |  **Purpose:** Fiscal reporting periods with fiscal_year and dates

| Column | Type | Nullable | Default | Notes |
|---|---|---|---|---|
| `period_id` | integer | NO | nextval('fin_reporting_periods | **PK** |
| `period_name` | varchar(20) | NO |  |  |
| `fiscal_year` | integer | NO |  |  |
| `fiscal_quarter` | integer | NO |  |  |
| `period_number` | integer | NO |  |  |
| `start_date` | date | NO |  |  |
| `end_date` | date | NO |  |  |
| `status` | varchar(20) | YES | 'OPEN'::character varying |  |
| `created_at` | timestamp | YES | now() |  |

## `hcm_assignments`

**Rows:** 4,000  |  **Purpose:** ALL org context: dept, grade, salary, job — primary HCM table

| Column | Type | Nullable | Default | Notes |
|---|---|---|---|---|
| `assignment_id` | integer | NO | nextval('hcm_assignments_assig | **PK** |
| `assignment_number` | varchar(20) | NO |  |  |
| `person_id` | integer | YES |  |  |
| `position_id` | integer | YES |  |  |
| `dept_id` | integer | YES |  |  |
| `org_id` | integer | YES |  |  |
| `grade_id` | integer | YES |  |  |
| `job_id` | integer | YES |  |  |
| `location_id` | integer | YES |  |  |
| `assignment_type` | varchar(20) | YES | 'PRIMARY'::character varying |  |
| `assignment_status` | varchar(20) | YES | 'ACTIVE'::character varying |  |
| `employment_status` | varchar(20) | YES | 'ACTIVE'::character varying |  |
| `job_title` | varchar(100) | YES |  |  |
| `salary` | numeric(12,2) | YES |  |  |
| `salary_currency` | varchar(3) | YES | 'GBP'::character varying |  |
| `manager_person_id` | integer | YES |  |  |
| `effective_from` | date | NO |  |  |
| `effective_to` | date | YES |  |  |
| `created_at` | timestamp | YES | now() |  |
| `updated_at` | timestamp | YES | now() |  |

## `hcm_compensation_elements`

**Rows:** 4,000  |  **Purpose:** Base/bonus/allowance pay components

| Column | Type | Nullable | Default | Notes |
|---|---|---|---|---|
| `element_id` | integer | NO | nextval('hcm_compensation_elem | **PK** |
| `assignment_id` | integer | YES |  |  |
| `element_type` | varchar(30) | NO |  |  |
| `element_name` | varchar(100) | NO |  |  |
| `amount` | numeric(12,2) | NO |  |  |
| `frequency` | varchar(20) | YES | 'MONTHLY'::character varying |  |
| `currency` | varchar(3) | YES | 'GBP'::character varying |  |
| `effective_from` | date | YES |  |  |
| `effective_to` | date | YES |  |  |
| `created_at` | timestamp | YES | now() |  |

## `hcm_cost_allocations`

**Rows:** 4,000  |  **Purpose:** Assignment cost allocation to fin_cost_centres (cross-domain bridge)

| Column | Type | Nullable | Default | Notes |
|---|---|---|---|---|
| `allocation_id` | integer | NO | nextval('hcm_cost_allocations_ | **PK** |
| `assignment_id` | integer | YES |  |  |
| `cost_centre_id` | integer | YES |  |  |
| `allocation_pct` | numeric(5,2) | YES | 100.00 |  |
| `effective_from` | date | NO |  |  |
| `effective_to` | date | YES |  |  |
| `created_at` | timestamp | YES | now() |  |

## `hcm_departments`

**Rows:** 4,000  |  **Purpose:** Department master — has cost_centre_code VARCHAR (not FK to fin_cost_centres)

| Column | Type | Nullable | Default | Notes |
|---|---|---|---|---|
| `dept_id` | integer | NO | nextval('hcm_departments_dept_ | **PK** |
| `dept_code` | varchar(20) | NO |  |  |
| `dept_name` | varchar(100) | NO |  |  |
| `org_id` | integer | YES |  |  |
| `cost_centre_code` | varchar(20) | YES |  |  |
| `manager_person_id` | integer | YES |  |  |
| `status` | varchar(20) | YES | 'ACTIVE'::character varying |  |
| `created_at` | timestamp | YES | now() |  |

## `hcm_employment_periods`

**Rows:** 4,000  |  **Purpose:** Hire to terminate date spans

| Column | Type | Nullable | Default | Notes |
|---|---|---|---|---|
| `employment_period_id` | integer | NO | nextval('hcm_employment_period | **PK** |
| `person_id` | integer | YES |  |  |
| `period_type` | varchar(20) | YES | 'EMPLOYEE'::character varying |  |
| `start_date` | date | NO |  |  |
| `end_date` | date | YES |  |  |
| `status` | varchar(20) | YES | 'ACTIVE'::character varying |  |
| `created_at` | timestamp | YES | now() |  |

## `hcm_grades`

**Rows:** 4,000  |  **Purpose:** Grade salary bands (min/mid/max)

| Column | Type | Nullable | Default | Notes |
|---|---|---|---|---|
| `grade_id` | integer | NO | nextval('hcm_grades_grade_id_s | **PK** |
| `grade_code` | varchar(10) | NO |  |  |
| `grade_name` | varchar(50) | NO |  |  |
| `min_salary` | numeric(12,2) | YES |  |  |
| `mid_salary` | numeric(12,2) | YES |  |  |
| `max_salary` | numeric(12,2) | YES |  |  |
| `currency` | varchar(3) | YES | 'GBP'::character varying |  |
| `created_at` | timestamp | YES | now() |  |

## `hcm_jobs`

**Rows:** 4,000  |  **Purpose:** Job catalog and job families

| Column | Type | Nullable | Default | Notes |
|---|---|---|---|---|
| `job_id` | integer | NO | nextval('hcm_jobs_job_id_seq': | **PK** |
| `job_code` | varchar(20) | NO |  |  |
| `job_name` | varchar(100) | NO |  |  |
| `job_family` | varchar(50) | YES |  |  |
| `job_level` | varchar(20) | YES |  |  |
| `min_salary` | numeric(12,2) | YES |  |  |
| `max_salary` | numeric(12,2) | YES |  |  |
| `status` | varchar(20) | YES | 'ACTIVE'::character varying |  |
| `created_at` | timestamp | YES | now() |  |

## `hcm_locations`

**Rows:** 4,000  |  **Purpose:** Office and work locations

| Column | Type | Nullable | Default | Notes |
|---|---|---|---|---|
| `location_id` | integer | NO | nextval('hcm_locations_locatio | **PK** |
| `location_code` | varchar(20) | NO |  |  |
| `location_name` | varchar(100) | NO |  |  |
| `address_line1` | varchar(200) | YES |  |  |
| `city` | varchar(50) | YES |  |  |
| `region` | varchar(30) | YES |  |  |
| `postal_code` | varchar(15) | YES |  |  |
| `country` | varchar(50) | YES | 'United Kingdom'::character va |  |
| `status` | varchar(20) | YES | 'ACTIVE'::character varying |  |
| `created_at` | timestamp | YES | now() |  |

## `hcm_organizations`

**Rows:** 4  |  **Purpose:** Business units and legal entities

| Column | Type | Nullable | Default | Notes |
|---|---|---|---|---|
| `org_id` | integer | NO | nextval('hcm_organizations_org | **PK** |
| `org_code` | varchar(20) | NO |  |  |
| `org_name` | varchar(150) | NO |  |  |
| `org_type` | varchar(30) | YES | 'BUSINESS_UNIT'::character var |  |
| `parent_org_id` | integer | YES |  |  |
| `country` | varchar(50) | YES | 'United Kingdom'::character va |  |
| `status` | varchar(20) | YES | 'ACTIVE'::character varying |  |
| `effective_from` | date | YES | CURRENT_DATE |  |
| `created_at` | timestamp | YES | now() |  |

## `hcm_payroll_results`

**Rows:** 4,000  |  **Purpose:** Individual payroll results per assignment

| Column | Type | Nullable | Default | Notes |
|---|---|---|---|---|
| `result_id` | integer | NO | nextval('hcm_payroll_results_r | **PK** |
| `payroll_run_id` | integer | YES |  |  |
| `assignment_id` | integer | YES |  |  |
| `gross_pay` | numeric(12,2) | YES |  |  |
| `tax_deducted` | numeric(12,2) | YES |  |  |
| `ni_deducted` | numeric(12,2) | YES |  |  |
| `pension_deducted` | numeric(12,2) | YES |  |  |
| `other_deductions` | numeric(12,2) | YES | 0 |  |
| `net_pay` | numeric(12,2) | YES |  |  |
| `account_code_id` | integer | YES |  |  |
| `created_at` | timestamp | YES | now() |  |

## `hcm_payroll_runs`

**Rows:** 4,000  |  **Purpose:** Payroll batch run headers

| Column | Type | Nullable | Default | Notes |
|---|---|---|---|---|
| `payroll_run_id` | integer | NO | nextval('hcm_payroll_runs_payr | **PK** |
| `run_name` | varchar(100) | NO |  |  |
| `period_name` | varchar(20) | NO |  |  |
| `run_date` | date | NO |  |  |
| `status` | varchar(20) | YES | 'COMPLETED'::character varying |  |
| `total_gross` | numeric(15,2) | YES |  |  |
| `total_deductions` | numeric(15,2) | YES |  |  |
| `total_net` | numeric(15,2) | YES |  |  |
| `employee_count` | integer | YES |  |  |
| `created_at` | timestamp | YES | now() |  |

## `hcm_performance_reviews`

**Rows:** 4,000  |  **Purpose:** Performance reviews linked to person

| Column | Type | Nullable | Default | Notes |
|---|---|---|---|---|
| `review_id` | integer | NO | nextval('hcm_performance_revie | **PK** |
| `person_id` | integer | YES |  |  |
| `reviewer_person_id` | integer | YES |  |  |
| `review_period` | varchar(20) | NO |  |  |
| `review_type` | varchar(20) | YES | 'ANNUAL'::character varying |  |
| `overall_rating` | varchar(30) | YES |  |  |
| `rating_score` | numeric(3,1) | YES |  |  |
| `goals_met_pct` | numeric(5,2) | YES |  |  |
| `comments` | text | YES |  |  |
| `status` | varchar(20) | YES | 'COMPLETED'::character varying |  |
| `review_date` | date | YES |  |  |
| `created_at` | timestamp | YES | now() |  |

## `hcm_person_emails`

**Rows:** 4,000  |  **Purpose:** Employee email addresses

| Column | Type | Nullable | Default | Notes |
|---|---|---|---|---|
| `email_id` | integer | NO | nextval('hcm_person_emails_ema | **PK** |
| `person_id` | integer | YES |  |  |
| `email_type` | varchar(20) | YES | 'WORK'::character varying |  |
| `email_address` | varchar(150) | NO |  |  |
| `is_primary` | boolean | YES | true |  |
| `created_at` | timestamp | YES | now() |  |

## `hcm_person_names`

**Rows:** 4,000  |  **Purpose:** Legal name change history

| Column | Type | Nullable | Default | Notes |
|---|---|---|---|---|
| `person_name_id` | integer | NO | nextval('hcm_person_names_pers | **PK** |
| `person_id` | integer | YES |  |  |
| `name_type` | varchar(20) | YES | 'GLOBAL'::character varying |  |
| `title` | varchar(10) | YES |  |  |
| `first_name` | varchar(80) | NO |  |  |
| `middle_name` | varchar(80) | YES |  |  |
| `last_name` | varchar(80) | NO |  |  |
| `suffix` | varchar(10) | YES |  |  |
| `effective_from` | date | NO |  |  |
| `effective_to` | date | YES |  |  |
| `created_at` | timestamp | YES | now() |  |

## `hcm_persons`

**Rows:** 4,000  |  **Purpose:** Employee master: identity (no salary, no org context)

| Column | Type | Nullable | Default | Notes |
|---|---|---|---|---|
| `person_id` | integer | NO | nextval('hcm_persons_person_id | **PK** |
| `person_number` | varchar(20) | NO |  |  |
| `first_name` | varchar(80) | NO |  |  |
| `last_name` | varchar(80) | NO |  |  |
| `date_of_birth` | date | YES |  |  |
| `gender` | varchar(10) | YES |  |  |
| `nationality` | varchar(50) | YES |  |  |
| `national_id` | varchar(30) | YES |  |  |
| `marital_status` | varchar(20) | YES |  |  |
| `person_type` | varchar(20) | YES | 'EMPLOYEE'::character varying |  |
| `status` | varchar(20) | YES | 'ACTIVE'::character varying |  |
| `created_at` | timestamp | YES | now() |  |
| `updated_at` | timestamp | YES | now() |  |

## `hcm_positions`

**Rows:** 10  |  **Purpose:** Position definitions (slot in org chart)

| Column | Type | Nullable | Default | Notes |
|---|---|---|---|---|
| `position_id` | integer | NO | nextval('hcm_positions_positio | **PK** |
| `position_code` | varchar(20) | NO |  |  |
| `position_name` | varchar(100) | NO |  |  |
| `dept_id` | integer | YES |  |  |
| `job_id` | integer | YES |  |  |
| `location_id` | integer | YES |  |  |
| `grade_id` | integer | YES |  |  |
| `headcount_target` | integer | YES | 1 |  |
| `status` | varchar(20) | YES | 'ACTIVE'::character varying |  |
| `created_at` | timestamp | YES | now() |  |

## `hcm_promotions`

**Rows:** 4,000  |  **Purpose:** Promotion history per assignment

| Column | Type | Nullable | Default | Notes |
|---|---|---|---|---|
| `promotion_id` | integer | NO | nextval('hcm_promotions_promot | **PK** |
| `assignment_id` | integer | YES |  |  |
| `effective_date` | date | NO |  |  |
| `old_grade` | varchar(10) | YES |  |  |
| `new_grade` | varchar(10) | YES |  |  |
| `old_job_title` | varchar(100) | YES |  |  |
| `new_job_title` | varchar(100) | YES |  |  |
| `old_salary` | numeric(12,2) | YES |  |  |
| `new_salary` | numeric(12,2) | YES |  |  |
| `approved_by` | integer | YES |  |  |
| `status` | varchar(20) | YES | 'APPROVED'::character varying |  |
| `created_at` | timestamp | YES | now() |  |

## `hcm_salary_history`

**Rows:** 4,000  |  **Purpose:** Salary change history per assignment

| Column | Type | Nullable | Default | Notes |
|---|---|---|---|---|
| `salary_history_id` | integer | NO | nextval('hcm_salary_history_sa | **PK** |
| `assignment_id` | integer | YES |  |  |
| `old_salary` | numeric(12,2) | YES |  |  |
| `new_salary` | numeric(12,2) | NO |  |  |
| `change_reason` | varchar(50) | YES |  |  |
| `effective_date` | date | NO |  |  |
| `currency` | varchar(3) | YES | 'GBP'::character varying |  |
| `approved_by` | integer | YES |  |  |
| `created_at` | timestamp | YES | now() |  |

## `hcm_termination_reasons`

**Rows:** 4,000  |  **Purpose:** Termination reason lookup

| Column | Type | Nullable | Default | Notes |
|---|---|---|---|---|
| `reason_id` | integer | NO | nextval('hcm_termination_reaso | **PK** |
| `reason_code` | varchar(20) | NO |  |  |
| `reason_name` | varchar(100) | NO |  |  |
| `reason_category` | varchar(30) | YES |  |  |
| `is_voluntary` | boolean | YES | true |  |
| `created_at` | timestamp | YES | now() |  |

## `hcm_training_records`

**Rows:** 4,000  |  **Purpose:** Training and certification records

| Column | Type | Nullable | Default | Notes |
|---|---|---|---|---|
| `training_id` | integer | NO | nextval('hcm_training_records_ | **PK** |
| `person_id` | integer | YES |  |  |
| `course_name` | varchar(150) | NO |  |  |
| `course_category` | varchar(50) | YES |  |  |
| `provider` | varchar(100) | YES |  |  |
| `completion_date` | date | YES |  |  |
| `score` | numeric(5,2) | YES |  |  |
| `status` | varchar(20) | YES | 'COMPLETED'::character varying |  |
| `certificate_id` | varchar(50) | YES |  |  |
| `created_at` | timestamp | YES | now() |  |

## `hcm_transfers`

**Rows:** 4,000  |  **Purpose:** Transfer history per assignment

| Column | Type | Nullable | Default | Notes |
|---|---|---|---|---|
| `transfer_id` | integer | NO | nextval('hcm_transfers_transfe | **PK** |
| `assignment_id` | integer | YES |  |  |
| `effective_date` | date | NO |  |  |
| `from_dept_id` | integer | YES |  |  |
| `to_dept_id` | integer | YES |  |  |
| `from_location_id` | integer | YES |  |  |
| `to_location_id` | integer | YES |  |  |
| `transfer_reason` | varchar(100) | YES |  |  |
| `approved_by` | integer | YES |  |  |
| `status` | varchar(20) | YES | 'APPROVED'::character varying |  |
| `created_at` | timestamp | YES | now() |  |

## `hcm_workforce_actions`

**Rows:** 4,000  |  **Purpose:** Hire/transfer/promote/terminate lifecycle actions

| Column | Type | Nullable | Default | Notes |
|---|---|---|---|---|
| `action_id` | integer | NO | nextval('hcm_workforce_actions | **PK** |
| `person_id` | integer | YES |  |  |
| `assignment_id` | integer | YES |  |  |
| `action_type` | varchar(30) | NO |  |  |
| `action_reason` | varchar(100) | YES |  |  |
| `effective_date` | date | NO |  |  |
| `reason_id` | integer | YES |  |  |
| `old_value` | varchar(200) | YES |  |  |
| `new_value` | varchar(200) | YES |  |  |
| `processed_by` | integer | YES |  |  |
| `status` | varchar(20) | YES | 'COMPLETED'::character varying |  |
| `created_at` | timestamp | YES | now() |  |

## `proc_contract_headers`

**Rows:** 4,000  |  **Purpose:** Blanket purchase contracts with supplier

| Column | Type | Nullable | Default | Notes |
|---|---|---|---|---|
| `contract_header_id` | integer | NO | nextval('proc_contract_headers | **PK** |
| `contract_number` | varchar(30) | NO |  |  |
| `contract_name` | varchar(200) | YES |  |  |
| `supplier_id` | integer | YES |  |  |
| `contract_type` | varchar(30) | YES | 'BLANKET'::character varying |  |
| `start_date` | date | YES |  |  |
| `end_date` | date | YES |  |  |
| `total_value` | numeric(15,2) | YES |  |  |
| `released_amount` | numeric(15,2) | YES | 0 |  |
| `status` | varchar(20) | YES | 'ACTIVE'::character varying |  |
| `owner_id` | integer | YES |  |  |
| `created_at` | timestamp | YES | now() |  |

## `proc_contract_lines`

**Rows:** 4,000  |  **Purpose:** Contract line items

| Column | Type | Nullable | Default | Notes |
|---|---|---|---|---|
| `contract_line_id` | integer | NO | nextval('proc_contract_lines_c | **PK** |
| `contract_header_id` | integer | YES |  |  |
| `line_number` | integer | NO |  |  |
| `item_id` | integer | YES |  |  |
| `description` | varchar(255) | YES |  |  |
| `quantity` | numeric(10,2) | YES |  |  |
| `unit_price` | numeric(12,2) | YES |  |  |
| `line_amount` | numeric(12,2) | YES |  |  |
| `released_amount` | numeric(12,2) | YES | 0 |  |
| `created_at` | timestamp | YES | now() |  |

## `proc_item_categories`

**Rows:** 4,000  |  **Purpose:** Item category hierarchy (self-referencing)

| Column | Type | Nullable | Default | Notes |
|---|---|---|---|---|
| `category_id` | integer | NO | nextval('proc_item_categories_ | **PK** |
| `category_code` | varchar(20) | NO |  |  |
| `category_name` | varchar(100) | NO |  |  |
| `parent_category_id` | integer | YES |  |  |
| `status` | varchar(20) | YES | 'ACTIVE'::character varying |  |
| `created_at` | timestamp | YES | now() |  |

## `proc_items`

**Rows:** 4,000  |  **Purpose:** Item/service catalog with unit_price

| Column | Type | Nullable | Default | Notes |
|---|---|---|---|---|
| `item_id` | integer | NO | nextval('proc_items_item_id_se | **PK** |
| `item_code` | varchar(20) | NO |  |  |
| `item_name` | varchar(150) | NO |  |  |
| `description` | varchar(255) | YES |  |  |
| `category_id` | integer | YES |  |  |
| `unit_of_measure` | varchar(20) | YES | 'EACH'::character varying |  |
| `unit_price` | numeric(12,2) | YES |  |  |
| `item_type` | varchar(20) | YES | 'SERVICE'::character varying |  |
| `status` | varchar(20) | YES | 'ACTIVE'::character varying |  |
| `created_at` | timestamp | YES | now() |  |

## `proc_po_approvals`

**Rows:** 4,000  |  **Purpose:** PO approval workflow

| Column | Type | Nullable | Default | Notes |
|---|---|---|---|---|
| `approval_id` | integer | NO | nextval('proc_po_approvals_app | **PK** |
| `po_header_id` | integer | YES |  |  |
| `approver_id` | integer | YES |  |  |
| `approval_level` | integer | YES | 1 |  |
| `action` | varchar(20) | NO |  |  |
| `comments` | text | YES |  |  |
| `action_date` | date | NO |  |  |
| `status` | varchar(20) | YES | 'APPROVED'::character varying |  |
| `created_at` | timestamp | YES | now() |  |

## `proc_po_distributions`

**Rows:** 4,000  |  **Purpose:** PO accounting distributions: amount, cost_centre_id — PRIMARY spend table

| Column | Type | Nullable | Default | Notes |
|---|---|---|---|---|
| `po_dist_id` | integer | NO | nextval('proc_po_distributions | **PK** |
| `po_line_id` | integer | YES |  |  |
| `cost_centre_id` | integer | YES |  |  |
| `account_code_id` | integer | YES |  |  |
| `distribution_pct` | numeric(5,2) | YES | 100.00 |  |
| `amount` | numeric(12,2) | YES |  |  |
| `created_at` | timestamp | YES | now() |  |

## `proc_po_headers`

**Rows:** 4,000  |  **Purpose:** PO headers: supplier_id, total_amount, status — NO cost_centre_id

| Column | Type | Nullable | Default | Notes |
|---|---|---|---|---|
| `po_header_id` | integer | NO | nextval('proc_po_headers_po_he | **PK** |
| `po_number` | varchar(50) | NO |  |  |
| `supplier_id` | integer | YES |  |  |
| `requisition_id` | integer | YES |  |  |
| `buyer_id` | integer | YES |  |  |
| `total_amount` | numeric(15,2) | YES |  |  |
| `approved_amount` | numeric(15,2) | YES |  |  |
| `status` | varchar(20) | YES | 'PENDING'::character varying |  |
| `created_date` | date | YES |  |  |
| `approved_date` | date | YES |  |  |
| `approved_by` | integer | YES |  |  |
| `category` | varchar(50) | YES |  |  |
| `created_at` | timestamp | YES | now() |  |
| `updated_at` | timestamp | YES | now() |  |

## `proc_po_lines`

**Rows:** 4,000  |  **Purpose:** PO line items: quantity, unit_price, line_amount

| Column | Type | Nullable | Default | Notes |
|---|---|---|---|---|
| `po_line_id` | integer | NO | nextval('proc_po_lines_po_line | **PK** |
| `po_header_id` | integer | YES |  |  |
| `line_number` | integer | NO |  |  |
| `item_id` | integer | YES |  |  |
| `description` | varchar(255) | YES |  |  |
| `quantity` | numeric(10,2) | YES | 1 |  |
| `unit_price` | numeric(12,2) | YES |  |  |
| `line_amount` | numeric(12,2) | YES |  |  |
| `status` | varchar(20) | YES | 'OPEN'::character varying |  |
| `created_at` | timestamp | YES | now() |  |

## `proc_quotation_headers`

**Rows:** 4,000  |  **Purpose:** Supplier quotation (RFQ) headers with engagement_id

| Column | Type | Nullable | Default | Notes |
|---|---|---|---|---|
| `quotation_header_id` | integer | NO | nextval('proc_quotation_header | **PK** |
| `quotation_number` | varchar(30) | NO |  |  |
| `engagement_id` | varchar(30) | NO |  |  |
| `engagement_name` | varchar(200) | YES |  |  |
| `supplier_id` | integer | YES |  |  |
| `original_amount` | numeric(15,2) | YES |  |  |
| `revised_amount` | numeric(15,2) | YES |  |  |
| `status` | varchar(20) | YES |  |  |
| `submission_date` | date | YES |  |  |
| `category` | varchar(50) | YES |  |  |
| `created_at` | timestamp | YES | now() |  |
| `updated_at` | timestamp | YES | now() |  |

## `proc_quotation_lines`

**Rows:** 4,000  |  **Purpose:** Quotation line items

| Column | Type | Nullable | Default | Notes |
|---|---|---|---|---|
| `quot_line_id` | integer | NO | nextval('proc_quotation_lines_ | **PK** |
| `quotation_header_id` | integer | YES |  |  |
| `line_number` | integer | NO |  |  |
| `item_id` | integer | YES |  |  |
| `description` | varchar(255) | YES |  |  |
| `quantity` | numeric(10,2) | YES | 1 |  |
| `unit_price` | numeric(12,2) | YES |  |  |
| `line_amount` | numeric(12,2) | YES |  |  |
| `created_at` | timestamp | YES | now() |  |

## `proc_quote_versions`

**Rows:** 4,000  |  **Purpose:** Quotation version history (audit trail)

| Column | Type | Nullable | Default | Notes |
|---|---|---|---|---|
| `version_id` | integer | NO | nextval('proc_quote_versions_v | **PK** |
| `quotation_header_id` | integer | YES |  |  |
| `version_number` | integer | NO |  |  |
| `version_amount` | numeric(15,2) | YES |  |  |
| `submitted_date` | date | YES |  |  |
| `status` | varchar(20) | YES |  |  |
| `change_notes` | text | YES |  |  |
| `created_at` | timestamp | YES | now() |  |

## `proc_receipt_headers`

**Rows:** 4,000  |  **Purpose:** Goods receipt headers linked to PO

| Column | Type | Nullable | Default | Notes |
|---|---|---|---|---|
| `receipt_header_id` | integer | NO | nextval('proc_receipt_headers_ | **PK** |
| `receipt_number` | varchar(30) | NO |  |  |
| `po_header_id` | integer | YES |  |  |
| `received_by` | integer | YES |  |  |
| `receipt_date` | date | NO |  |  |
| `status` | varchar(20) | YES | 'RECEIVED'::character varying |  |
| `comments` | text | YES |  |  |
| `created_at` | timestamp | YES | now() |  |

## `proc_receipt_lines`

**Rows:** 4,000  |  **Purpose:** Goods receipt lines matched to PO lines

| Column | Type | Nullable | Default | Notes |
|---|---|---|---|---|
| `receipt_line_id` | integer | NO | nextval('proc_receipt_lines_re | **PK** |
| `receipt_header_id` | integer | YES |  |  |
| `po_line_id` | integer | YES |  |  |
| `quantity_received` | numeric(10,2) | YES |  |  |
| `quantity_accepted` | numeric(10,2) | YES |  |  |
| `quantity_rejected` | numeric(10,2) | YES | 0 |  |
| `inspection_status` | varchar(20) | YES | 'ACCEPTED'::character varying |  |
| `created_at` | timestamp | YES | now() |  |

## `proc_requisition_distributions`

**Rows:** 4,000  |  **Purpose:** Requisition accounting distributions to cost centres

| Column | Type | Nullable | Default | Notes |
|---|---|---|---|---|
| `req_dist_id` | integer | NO | nextval('proc_requisition_dist | **PK** |
| `req_line_id` | integer | YES |  |  |
| `cost_centre_id` | integer | YES |  |  |
| `account_code_id` | integer | YES |  |  |
| `distribution_pct` | numeric(5,2) | YES | 100.00 |  |
| `amount` | numeric(12,2) | YES |  |  |
| `created_at` | timestamp | YES | now() |  |

## `proc_requisition_headers`

**Rows:** 4,000  |  **Purpose:** Purchase requisition headers with total_amount

| Column | Type | Nullable | Default | Notes |
|---|---|---|---|---|
| `requisition_id` | integer | NO | nextval('proc_requisition_head | **PK** |
| `requisition_number` | varchar(30) | NO |  |  |
| `requester_id` | integer | YES |  |  |
| `dept_id` | integer | YES |  |  |
| `description` | varchar(255) | YES |  |  |
| `justification` | text | YES |  |  |
| `total_amount` | numeric(15,2) | YES |  |  |
| `status` | varchar(20) | YES | 'APPROVED'::character varying |  |
| `submitted_date` | date | YES |  |  |
| `approved_date` | date | YES |  |  |
| `approved_by` | integer | YES |  |  |
| `created_at` | timestamp | YES | now() |  |
| `updated_at` | timestamp | YES | now() |  |

## `proc_requisition_lines`

**Rows:** 4,000  |  **Purpose:** Requisition line items

| Column | Type | Nullable | Default | Notes |
|---|---|---|---|---|
| `req_line_id` | integer | NO | nextval('proc_requisition_line | **PK** |
| `requisition_id` | integer | YES |  |  |
| `line_number` | integer | NO |  |  |
| `item_id` | integer | YES |  |  |
| `description` | varchar(255) | YES |  |  |
| `quantity` | numeric(10,2) | YES | 1 |  |
| `unit_price` | numeric(12,2) | YES |  |  |
| `line_amount` | numeric(12,2) | YES |  |  |
| `need_by_date` | date | YES |  |  |
| `created_at` | timestamp | YES | now() |  |

## `schema_embeddings`

**Rows:** 19  |  **Purpose:** PGVector embeddings of schema documentation (AI RAG)

| Column | Type | Nullable | Default | Notes |
|---|---|---|---|---|
| `id` | integer | NO | nextval('schema_embeddings_id_ | **PK** |
| `doc_id` | varchar(100) | NO |  |  |
| `domain` | varchar(30) | NO |  |  |
| `title` | varchar(200) | YES |  |  |
| `content` | text | NO |  |  |
| `embedding` | vector | YES |  |  |
| `created_at` | timestamp | YES | now() |  |

## `sup_supplier_contacts`

**Rows:** 4,000  |  **Purpose:** Supplier contact persons

| Column | Type | Nullable | Default | Notes |
|---|---|---|---|---|
| `contact_id` | integer | NO | nextval('sup_supplier_contacts | **PK** |
| `supplier_id` | integer | YES |  |  |
| `contact_name` | varchar(100) | NO |  |  |
| `job_title` | varchar(100) | YES |  |  |
| `email` | varchar(150) | YES |  |  |
| `phone` | varchar(30) | YES |  |  |
| `is_primary` | boolean | YES | false |  |
| `created_at` | timestamp | YES | now() |  |

## `sup_supplier_sites`

**Rows:** 4,000  |  **Purpose:** Supplier site addresses

| Column | Type | Nullable | Default | Notes |
|---|---|---|---|---|
| `site_id` | integer | NO | nextval('sup_supplier_sites_si | **PK** |
| `supplier_id` | integer | YES |  |  |
| `site_code` | varchar(20) | NO |  |  |
| `site_name` | varchar(100) | YES |  |  |
| `address_line1` | varchar(200) | YES |  |  |
| `city` | varchar(50) | YES |  |  |
| `postal_code` | varchar(15) | YES |  |  |
| `country` | varchar(50) | YES | 'United Kingdom'::character va |  |
| `is_primary` | boolean | YES | false |  |
| `status` | varchar(20) | YES | 'ACTIVE'::character varying |  |
| `created_at` | timestamp | YES | now() |  |

## `sup_suppliers`

**Rows:** 4,000  |  **Purpose:** Unified supplier/vendor master for AP and Procurement

| Column | Type | Nullable | Default | Notes |
|---|---|---|---|---|
| `supplier_id` | integer | NO | nextval('sup_suppliers_supplie | **PK** |
| `supplier_number` | varchar(20) | NO |  |  |
| `supplier_name` | varchar(150) | NO |  |  |
| `tax_registration` | varchar(30) | YES |  |  |
| `payment_terms` | varchar(30) | YES | 'NET30'::character varying |  |
| `supplier_type` | varchar(30) | YES |  |  |
| `risk_rating` | varchar(10) | YES |  |  |
| `qualification_status` | varchar(20) | YES | 'QUALIFIED'::character varying |  |
| `status` | varchar(20) | YES | 'ACTIVE'::character varying |  |
| `country` | varchar(50) | YES | 'United Kingdom'::character va |  |
| `created_at` | timestamp | YES | now() |  |
| `updated_at` | timestamp | YES | now() |  |

---

# PRIMARY KEYS

| Table | Primary Key |
|---|---|
| `ai_query_log` | `log_id` |
| `fin_account_codes` | `account_code_id` |
| `fin_ap_invoice_distributions` | `distribution_id` |
| `fin_ap_invoice_lines` | `invoice_line_id` |
| `fin_ap_invoices` | `invoice_id` |
| `fin_ap_payment_schedules` | `schedule_id` |
| `fin_ap_payments` | `payment_id` |
| `fin_ar_customers` | `customer_id` |
| `fin_ar_invoices` | `ar_invoice_id` |
| `fin_ar_receipts` | `receipt_id` |
| `fin_budget_headers` | `budget_header_id` |
| `fin_budget_lines` | `budget_line_id` |
| `fin_budget_versions` | `budget_version_id` |
| `fin_chart_of_accounts` | `coa_id` |
| `fin_coa_segments` | `segment_id` |
| `fin_cost_centres` | `cost_centre_id` |
| `fin_currency_rates` | `rate_id` |
| `fin_gl_balances` | `balance_id` |
| `fin_gl_journal_headers` | `journal_header_id` |
| `fin_gl_journal_lines` | `journal_line_id` |
| `fin_ledgers` | `ledger_id` |
| `fin_reporting_periods` | `period_id` |
| `hcm_assignments` | `assignment_id` |
| `hcm_compensation_elements` | `element_id` |
| `hcm_cost_allocations` | `allocation_id` |
| `hcm_departments` | `dept_id` |
| `hcm_employment_periods` | `employment_period_id` |
| `hcm_grades` | `grade_id` |
| `hcm_jobs` | `job_id` |
| `hcm_locations` | `location_id` |
| `hcm_organizations` | `org_id` |
| `hcm_payroll_results` | `result_id` |
| `hcm_payroll_runs` | `payroll_run_id` |
| `hcm_performance_reviews` | `review_id` |
| `hcm_person_emails` | `email_id` |
| `hcm_person_names` | `person_name_id` |
| `hcm_persons` | `person_id` |
| `hcm_positions` | `position_id` |
| `hcm_promotions` | `promotion_id` |
| `hcm_salary_history` | `salary_history_id` |
| `hcm_termination_reasons` | `reason_id` |
| `hcm_training_records` | `training_id` |
| `hcm_transfers` | `transfer_id` |
| `hcm_workforce_actions` | `action_id` |
| `proc_contract_headers` | `contract_header_id` |
| `proc_contract_lines` | `contract_line_id` |
| `proc_item_categories` | `category_id` |
| `proc_items` | `item_id` |
| `proc_po_approvals` | `approval_id` |
| `proc_po_distributions` | `po_dist_id` |
| `proc_po_headers` | `po_header_id` |
| `proc_po_lines` | `po_line_id` |
| `proc_quotation_headers` | `quotation_header_id` |
| `proc_quotation_lines` | `quot_line_id` |
| `proc_quote_versions` | `version_id` |
| `proc_receipt_headers` | `receipt_header_id` |
| `proc_receipt_lines` | `receipt_line_id` |
| `proc_requisition_distributions` | `req_dist_id` |
| `proc_requisition_headers` | `requisition_id` |
| `proc_requisition_lines` | `req_line_id` |
| `schema_embeddings` | `id` |
| `sup_supplier_contacts` | `contact_id` |
| `sup_supplier_sites` | `site_id` |
| `sup_suppliers` | `supplier_id` |

---

# FOREIGN KEY RELATIONSHIPS

| Child Table | Child Column | Referenced Table | Referenced Column |
|---|---|---|---|

---

# DOMAIN GROUPING

## HCM

| Table | Rows | Purpose |
|---|---|---|
| `hcm_assignments` | 4,000 | ALL org context: dept, grade, salary, job — primary HCM table |
| `hcm_compensation_elements` | 4,000 | Base/bonus/allowance pay components |
| `hcm_cost_allocations` | 4,000 | Assignment cost allocation to fin_cost_centres (cross-domain bridge) |
| `hcm_departments` | 4,000 | Department master — has cost_centre_code VARCHAR (not FK to fin_cost_centres) |
| `hcm_employment_periods` | 4,000 | Hire to terminate date spans |
| `hcm_grades` | 4,000 | Grade salary bands (min/mid/max) |
| `hcm_jobs` | 4,000 | Job catalog and job families |
| `hcm_locations` | 4,000 | Office and work locations |
| `hcm_organizations` | 4 | Business units and legal entities |
| `hcm_payroll_results` | 4,000 | Individual payroll results per assignment |
| `hcm_payroll_runs` | 4,000 | Payroll batch run headers |
| `hcm_performance_reviews` | 4,000 | Performance reviews linked to person |
| `hcm_person_emails` | 4,000 | Employee email addresses |
| `hcm_person_names` | 4,000 | Legal name change history |
| `hcm_persons` | 4,000 | Employee master: identity (no salary, no org context) |
| `hcm_positions` | 10 | Position definitions (slot in org chart) |
| `hcm_promotions` | 4,000 | Promotion history per assignment |
| `hcm_salary_history` | 4,000 | Salary change history per assignment |
| `hcm_termination_reasons` | 4,000 | Termination reason lookup |
| `hcm_training_records` | 4,000 | Training and certification records |
| `hcm_transfers` | 4,000 | Transfer history per assignment |
| `hcm_workforce_actions` | 4,000 | Hire/transfer/promote/terminate lifecycle actions |

## Finance

| Table | Rows | Purpose |
|---|---|---|
| `fin_account_codes` | 4,000 | Account code master |
| `fin_ap_invoice_distributions` | 4,000 | AP invoice accounting distributions to cost centres |
| `fin_ap_invoice_lines` | 4,000 | AP invoice line items with po_line_id (3-way match) |
| `fin_ap_invoices` | 4,000 | AP invoices with invoice_amount, supplier_id, status, due_date |
| `fin_ap_payment_schedules` | 4,000 | AP payment schedules per invoice |
| `fin_ap_payments` | 4,000 | AP payment records — payment_amount, supplier_id (NO invoice_id FK) |
| `fin_ar_customers` | 4,000 | Accounts receivable customer master |
| `fin_ar_invoices` | 4,000 | AR invoices with invoice_amount, customer_id, outstanding |
| `fin_ar_receipts` | 4,000 | AR customer payment receipts |
| `fin_budget_headers` | 4,000 | Budget header per ledger — fiscal_year and total_amount only |
| `fin_budget_lines` | 4,000 | Budget line amounts at cost centre + account level — PRIMARY budget table |
| `fin_budget_versions` | 4,000 | Budget version control (original/revised/forecast) |
| `fin_chart_of_accounts` | 4,000 | Chart of accounts structure |
| `fin_coa_segments` | 4,000 | COA segment definitions |
| `fin_cost_centres` | 4,000 | Cost centre master — bridge between HCM and Finance |
| `fin_currency_rates` | 4,000 | Currency exchange rates |
| `fin_gl_balances` | 4,000 | GL summary balances: period_debit/credit/net, begin/end_balance, fiscal_year |
| `fin_gl_journal_headers` | 4,000 | GL journal entry headers |
| `fin_gl_journal_lines` | 4,000 | GL journal line items with account + cost centre |
| `fin_ledgers` | 4,000 | General ledger definitions |
| `fin_reporting_periods` | 4,000 | Fiscal reporting periods with fiscal_year and dates |

## Procurement

| Table | Rows | Purpose |
|---|---|---|
| `proc_contract_headers` | 4,000 | Blanket purchase contracts with supplier |
| `proc_contract_lines` | 4,000 | Contract line items |
| `proc_item_categories` | 4,000 | Item category hierarchy (self-referencing) |
| `proc_items` | 4,000 | Item/service catalog with unit_price |
| `proc_po_approvals` | 4,000 | PO approval workflow |
| `proc_po_distributions` | 4,000 | PO accounting distributions: amount, cost_centre_id — PRIMARY spend table |
| `proc_po_headers` | 4,000 | PO headers: supplier_id, total_amount, status — NO cost_centre_id |
| `proc_po_lines` | 4,000 | PO line items: quantity, unit_price, line_amount |
| `proc_quotation_headers` | 4,000 | Supplier quotation (RFQ) headers with engagement_id |
| `proc_quotation_lines` | 4,000 | Quotation line items |
| `proc_quote_versions` | 4,000 | Quotation version history (audit trail) |
| `proc_receipt_headers` | 4,000 | Goods receipt headers linked to PO |
| `proc_receipt_lines` | 4,000 | Goods receipt lines matched to PO lines |
| `proc_requisition_distributions` | 4,000 | Requisition accounting distributions to cost centres |
| `proc_requisition_headers` | 4,000 | Purchase requisition headers with total_amount |
| `proc_requisition_lines` | 4,000 | Requisition line items |
| `sup_supplier_contacts` | 4,000 | Supplier contact persons |
| `sup_supplier_sites` | 4,000 | Supplier site addresses |
| `sup_suppliers` | 4,000 | Unified supplier/vendor master for AP and Procurement |

## System

| Table | Rows | Purpose |
|---|---|---|
| `ai_query_log` | 152 | AI agent query audit log |
| `schema_embeddings` | 19 | PGVector embeddings of schema documentation (AI RAG) |

---

# DATA COVERAGE ANALYSIS

## Fiscal Years Available

| Source Table | Fiscal Years |
|---|---|
| `fin_budget_headers.fiscal_year` | 2023, 2024, 2025, 2026 |
| `fin_gl_balances.fiscal_year` | 2023, 2024, 2025, 2026 |

## Accounting Periods Available

**fin_budget_headers.period_name:**

(none)

**fin_budget_lines.period_name:**

APR-2023, APR-2024, APR-2025, APR-2026, AUG-2023, AUG-2024, AUG-2025, AUG-2026, DEC-2023, DEC-2024, DEC-2025, DEC-2026, FEB-2023, FEB-2024, FEB-2025, FEB-2026, JAN-2023, JAN-2024, JAN-2025, JAN-2026

**fin_gl_balances.period_name:**

APR-2023, APR-2024, APR-2025, APR-2026, AUG-2023, AUG-2024, AUG-2025, AUG-2026, DEC-2023, DEC-2024, DEC-2025, DEC-2026, FEB-2023, FEB-2024, FEB-2025, FEB-2026, JAN-2023, JAN-2024, JAN-2025, JAN-2026

## Departments (first 20 from hcm_departments)

| dept_id | dept_name |
|---|---|
| 1 | Engineering |
| 2 | Finance |
| 3 | HR |
| 4 | Procurement |
| 5 | Marketing |
| 6 | Sales |
| 7 | Operations |
| 8 | IT |
| 9 | Legal |
| 10 | Executive |
| 11 | Operations 11 |
| 12 | Treasury 12 |
| 13 | Audit 13 |
| 14 | Customer Support 14 |
| 15 | Procurement 15 |
| 16 | Sales 16 |
| 17 | Customer Support 17 |
| 18 | R&D 18 |
| 19 | Executive 19 |
| 20 | Treasury 20 |

## Cost Centres (fin_cost_centres — all rows)

| cost_centre_id | code | name | dept_id |
|---|---|---|---|
| 1 | CC001 | Engineering | 1 |
| 2 | CC002 | Finance | 2 |
| 3 | CC004 | HR | 3 |
| 4 | CC005 | Procurement | 4 |
| 5 | CC003 | Marketing | 5 |
| 6 | CC006 | Sales | 6 |
| 7 | CC007 | Operations | 7 |
| 8 | CC008 | IT | 8 |
| 9 | CC009 | Legal | 9 |
| 10 | CC010 | Executive | 10 |
| 11 | CC0011 | Support CC11 | 846 |
| 12 | CC0012 | Strategy CC12 | 741 |
| 13 | CC0013 | Procurement CC13 | 2825 |
| 14 | CC0014 | Logistics CC14 | 918 |
| 15 | CC0015 | Analytics CC15 | 3325 |
| 16 | CC0016 | Analytics CC16 | 445 |
| 17 | CC0017 | Logistics CC17 | 2968 |
| 18 | CC0018 | Support CC18 | 2269 |
| 19 | CC0019 | Quality CC19 | 1270 |
| 20 | CC0020 | IT CC20 | 3676 |
| 21 | CC0021 | Treasury CC21 | 3769 |
| 22 | CC0022 | Analytics CC22 | 2361 |
| 23 | CC0023 | Treasury CC23 | 2213 |
| 24 | CC0024 | Audit CC24 | 3571 |
| 25 | CC0025 | Treasury CC25 | 821 |
| 26 | CC0026 | Sales CC26 | 1322 |
| 27 | CC0027 | Audit CC27 | 2141 |
| 28 | CC0028 | Procurement CC28 | 726 |
| 29 | CC0029 | Marketing CC29 | 136 |
| 30 | CC0030 | HR CC30 | 3936 |
| 31 | CC0031 | Sales CC31 | 3474 |
| 32 | CC0032 | Analytics CC32 | 845 |
| 33 | CC0033 | Marketing CC33 | 608 |
| 34 | CC0034 | Engineering CC34 | 1059 |
| 35 | CC0035 | Compliance CC35 | 1780 |
| 36 | CC0036 | Logistics CC36 | 2428 |
| 37 | CC0037 | Operations CC37 | 3947 |
| 38 | CC0038 | Quality CC38 | 3766 |
| 39 | CC0039 | IT CC39 | 1766 |
| 40 | CC0040 | Strategy CC40 | 3703 |
| 41 | CC0041 | Executive CC41 | 1981 |
| 42 | CC0042 | Risk CC42 | 904 |
| 43 | CC0043 | Compliance CC43 | 1272 |
| 44 | CC0044 | Analytics CC44 | 1831 |
| 45 | CC0045 | Risk CC45 | 276 |
| 46 | CC0046 | Compliance CC46 | 2959 |
| 47 | CC0047 | Compliance CC47 | 543 |
| 48 | CC0048 | Finance CC48 | 484 |
| 49 | CC0049 | Analytics CC49 | 3276 |
| 50 | CC0050 | Support CC50 | 1812 |
| 51 | CC0051 | Engineering CC51 | 869 |
| 52 | CC0052 | Audit CC52 | 2016 |
| 53 | CC0053 | Audit CC53 | 175 |
| 54 | CC0054 | Compliance CC54 | 1819 |
| 55 | CC0055 | Operations CC55 | 3031 |
| 56 | CC0056 | Executive CC56 | 1633 |
| 57 | CC0057 | Finance CC57 | 2433 |
| 58 | CC0058 | Support CC58 | 2292 |
| 59 | CC0059 | Strategy CC59 | 3456 |
| 60 | CC0060 | Executive CC60 | 1458 |
| 61 | CC0061 | Sales CC61 | 1777 |
| 62 | CC0062 | Treasury CC62 | 1147 |
| 63 | CC0063 | Legal CC63 | 3834 |
| 64 | CC0064 | R&D CC64 | 844 |
| 65 | CC0065 | Sales CC65 | 2558 |
| 66 | CC0066 | Treasury CC66 | 1049 |
| 67 | CC0067 | Marketing CC67 | 1654 |
| 68 | CC0068 | HR CC68 | 198 |
| 69 | CC0069 | HR CC69 | 1790 |
| 70 | CC0070 | Operations CC70 | 2799 |
| 71 | CC0071 | IT CC71 | 3271 |
| 72 | CC0072 | Quality CC72 | 1448 |
| 73 | CC0073 | Operations CC73 | 1764 |
| 74 | CC0074 | Audit CC74 | 1960 |
| 75 | CC0075 | Risk CC75 | 1669 |
| 76 | CC0076 | Finance CC76 | 2503 |
| 77 | CC0077 | Marketing CC77 | 1057 |
| 78 | CC0078 | Treasury CC78 | 2776 |
| 79 | CC0079 | Strategy CC79 | 1385 |
| 80 | CC0080 | IT CC80 | 3483 |
| 81 | CC0081 | Risk CC81 | 2309 |
| 82 | CC0082 | R&D CC82 | 3629 |
| 83 | CC0083 | Operations CC83 | 2345 |
| 84 | CC0084 | Legal CC84 | 1141 |
| 85 | CC0085 | Compliance CC85 | 2330 |
| 86 | CC0086 | IT CC86 | 1127 |
| 87 | CC0087 | Marketing CC87 | 2470 |
| 88 | CC0088 | Analytics CC88 | 887 |
| 89 | CC0089 | Analytics CC89 | 2169 |
| 90 | CC0090 | Quality CC90 | 3221 |
| 91 | CC0091 | Finance CC91 | 3740 |
| 92 | CC0092 | Finance CC92 | 3496 |
| 93 | CC0093 | Quality CC93 | 1883 |
| 94 | CC0094 | Risk CC94 | 459 |
| 95 | CC0095 | HR CC95 | 2773 |
| 96 | CC0096 | Strategy CC96 | 1413 |
| 97 | CC0097 | Audit CC97 | 3709 |
| 98 | CC0098 | Procurement CC98 | 3114 |
| 99 | CC0099 | R&D CC99 | 137 |
| 100 | CC0100 | Procurement CC100 | 645 |
| 101 | CC0101 | Support CC101 | 1174 |
| 102 | CC0102 | Compliance CC102 | 3361 |
| 103 | CC0103 | R&D CC103 | 2027 |
| 104 | CC0104 | Logistics CC104 | 1970 |
| 105 | CC0105 | R&D CC105 | 3218 |
| 106 | CC0106 | Risk CC106 | 3373 |
| 107 | CC0107 | Compliance CC107 | 3412 |
| 108 | CC0108 | Engineering CC108 | 2737 |
| 109 | CC0109 | Executive CC109 | 2234 |
| 110 | CC0110 | Quality CC110 | 555 |
| 111 | CC0111 | Compliance CC111 | 897 |
| 112 | CC0112 | Compliance CC112 | 283 |
| 113 | CC0113 | HR CC113 | 1797 |
| 114 | CC0114 | IT CC114 | 2202 |
| 115 | CC0115 | Compliance CC115 | 2283 |
| 116 | CC0116 | Procurement CC116 | 1506 |
| 117 | CC0117 | IT CC117 | 160 |
| 118 | CC0118 | Support CC118 | 1105 |
| 119 | CC0119 | Logistics CC119 | 1372 |
| 120 | CC0120 | Risk CC120 | 2387 |
| 121 | CC0121 | Finance CC121 | 1537 |
| 122 | CC0122 | Risk CC122 | 3426 |
| 123 | CC0123 | R&D CC123 | 1067 |
| 124 | CC0124 | Support CC124 | 3156 |
| 125 | CC0125 | HR CC125 | 1079 |
| 126 | CC0126 | Sales CC126 | 694 |
| 127 | CC0127 | Treasury CC127 | 2185 |
| 128 | CC0128 | R&D CC128 | 2203 |
| 129 | CC0129 | Support CC129 | 2794 |
| 130 | CC0130 | Marketing CC130 | 1753 |
| 131 | CC0131 | Support CC131 | 3412 |
| 132 | CC0132 | Analytics CC132 | 3105 |
| 133 | CC0133 | Analytics CC133 | 491 |
| 134 | CC0134 | Strategy CC134 | 2493 |
| 135 | CC0135 | Analytics CC135 | 1169 |
| 136 | CC0136 | Support CC136 | 1277 |
| 137 | CC0137 | Operations CC137 | 121 |
| 138 | CC0138 | Marketing CC138 | 1232 |
| 139 | CC0139 | Analytics CC139 | 186 |
| 140 | CC0140 | Executive CC140 | 2010 |
| 141 | CC0141 | Logistics CC141 | 2246 |
| 142 | CC0142 | Strategy CC142 | 248 |
| 143 | CC0143 | Finance CC143 | 3614 |
| 144 | CC0144 | Quality CC144 | 3220 |
| 145 | CC0145 | Audit CC145 | 1594 |
| 146 | CC0146 | Risk CC146 | 1580 |
| 147 | CC0147 | IT CC147 | 1602 |
| 148 | CC0148 | Analytics CC148 | 2920 |
| 149 | CC0149 | Treasury CC149 | 2461 |
| 150 | CC0150 | HR CC150 | 2031 |
| 151 | CC0151 | Strategy CC151 | 3669 |
| 152 | CC0152 | Executive CC152 | 1130 |
| 153 | CC0153 | Marketing CC153 | 2553 |
| 154 | CC0154 | Logistics CC154 | 2928 |
| 155 | CC0155 | Marketing CC155 | 950 |
| 156 | CC0156 | Engineering CC156 | 1071 |
| 157 | CC0157 | Quality CC157 | 3852 |
| 158 | CC0158 | Legal CC158 | 5 |
| 159 | CC0159 | Analytics CC159 | 599 |
| 160 | CC0160 | Support CC160 | 809 |
| 161 | CC0161 | Sales CC161 | 1866 |
| 162 | CC0162 | Engineering CC162 | 3240 |
| 163 | CC0163 | Sales CC163 | 3198 |
| 164 | CC0164 | Operations CC164 | 3762 |
| 165 | CC0165 | Operations CC165 | 2413 |
| 166 | CC0166 | Executive CC166 | 1410 |
| 167 | CC0167 | Analytics CC167 | 2634 |
| 168 | CC0168 | Legal CC168 | 3089 |
| 169 | CC0169 | Strategy CC169 | 612 |
| 170 | CC0170 | HR CC170 | 138 |
| 171 | CC0171 | Treasury CC171 | 3460 |
| 172 | CC0172 | Audit CC172 | 3200 |
| 173 | CC0173 | Quality CC173 | 1718 |
| 174 | CC0174 | Operations CC174 | 2453 |
| 175 | CC0175 | R&D CC175 | 1869 |
| 176 | CC0176 | Marketing CC176 | 2229 |
| 177 | CC0177 | Strategy CC177 | 3972 |
| 178 | CC0178 | Procurement CC178 | 3450 |
| 179 | CC0179 | Executive CC179 | 1970 |
| 180 | CC0180 | Procurement CC180 | 187 |
| 181 | CC0181 | Sales CC181 | 1382 |
| 182 | CC0182 | R&D CC182 | 1661 |
| 183 | CC0183 | Risk CC183 | 3557 |
| 184 | CC0184 | HR CC184 | 214 |
| 185 | CC0185 | IT CC185 | 3279 |
| 186 | CC0186 | Audit CC186 | 2398 |
| 187 | CC0187 | Operations CC187 | 2888 |
| 188 | CC0188 | Compliance CC188 | 1075 |
| 189 | CC0189 | Engineering CC189 | 2485 |
| 190 | CC0190 | Procurement CC190 | 2545 |
| 191 | CC0191 | Logistics CC191 | 2230 |
| 192 | CC0192 | IT CC192 | 1729 |
| 193 | CC0193 | Treasury CC193 | 2443 |
| 194 | CC0194 | R&D CC194 | 265 |
| 195 | CC0195 | HR CC195 | 3549 |
| 196 | CC0196 | Finance CC196 | 428 |
| 197 | CC0197 | Engineering CC197 | 3493 |
| 198 | CC0198 | Logistics CC198 | 2298 |
| 199 | CC0199 | Compliance CC199 | 2836 |
| 200 | CC0200 | Treasury CC200 | 180 |
| 201 | CC0201 | Engineering CC201 | 1996 |
| 202 | CC0202 | Quality CC202 | 1678 |
| 203 | CC0203 | Analytics CC203 | 2911 |
| 204 | CC0204 | Logistics CC204 | 2770 |
| 205 | CC0205 | Executive CC205 | 216 |
| 206 | CC0206 | Marketing CC206 | 711 |
| 207 | CC0207 | Sales CC207 | 2940 |
| 208 | CC0208 | Analytics CC208 | 2436 |
| 209 | CC0209 | R&D CC209 | 546 |
| 210 | CC0210 | R&D CC210 | 1133 |
| 211 | CC0211 | Strategy CC211 | 1406 |
| 212 | CC0212 | Marketing CC212 | 3093 |
| 213 | CC0213 | Executive CC213 | 1037 |
| 214 | CC0214 | Quality CC214 | 1353 |
| 215 | CC0215 | Treasury CC215 | 1710 |
| 216 | CC0216 | Executive CC216 | 528 |
| 217 | CC0217 | Support CC217 | 2725 |
| 218 | CC0218 | Quality CC218 | 2656 |
| 219 | CC0219 | Executive CC219 | 815 |
| 220 | CC0220 | Treasury CC220 | 3972 |
| 221 | CC0221 | Analytics CC221 | 2049 |
| 222 | CC0222 | HR CC222 | 1632 |
| 223 | CC0223 | HR CC223 | 250 |
| 224 | CC0224 | Audit CC224 | 920 |
| 225 | CC0225 | HR CC225 | 1269 |
| 226 | CC0226 | Operations CC226 | 3678 |
| 227 | CC0227 | Engineering CC227 | 1230 |
| 228 | CC0228 | Executive CC228 | 1006 |
| 229 | CC0229 | Quality CC229 | 523 |
| 230 | CC0230 | Strategy CC230 | 3402 |
| 231 | CC0231 | Marketing CC231 | 896 |
| 232 | CC0232 | Procurement CC232 | 1306 |
| 233 | CC0233 | Quality CC233 | 1217 |
| 234 | CC0234 | Legal CC234 | 3792 |
| 235 | CC0235 | Logistics CC235 | 803 |
| 236 | CC0236 | HR CC236 | 2510 |
| 237 | CC0237 | Treasury CC237 | 2969 |
| 238 | CC0238 | Executive CC238 | 3246 |
| 239 | CC0239 | HR CC239 | 1588 |
| 240 | CC0240 | Strategy CC240 | 234 |
| 241 | CC0241 | Executive CC241 | 1485 |
| 242 | CC0242 | Audit CC242 | 303 |
| 243 | CC0243 | Treasury CC243 | 3707 |
| 244 | CC0244 | Quality CC244 | 3110 |
| 245 | CC0245 | Sales CC245 | 3237 |
| 246 | CC0246 | Logistics CC246 | 340 |
| 247 | CC0247 | Marketing CC247 | 2207 |
| 248 | CC0248 | IT CC248 | 2170 |
| 249 | CC0249 | Quality CC249 | 1801 |
| 250 | CC0250 | Procurement CC250 | 38 |
| 251 | CC0251 | Risk CC251 | 3499 |
| 252 | CC0252 | Procurement CC252 | 224 |
| 253 | CC0253 | Engineering CC253 | 1007 |
| 254 | CC0254 | Operations CC254 | 1245 |
| 255 | CC0255 | Operations CC255 | 3377 |
| 256 | CC0256 | Engineering CC256 | 551 |
| 257 | CC0257 | Executive CC257 | 2448 |
| 258 | CC0258 | Procurement CC258 | 235 |
| 259 | CC0259 | Marketing CC259 | 3955 |
| 260 | CC0260 | Treasury CC260 | 3945 |
| 261 | CC0261 | Quality CC261 | 2626 |
| 262 | CC0262 | R&D CC262 | 1875 |
| 263 | CC0263 | R&D CC263 | 3566 |
| 264 | CC0264 | Engineering CC264 | 2072 |
| 265 | CC0265 | Sales CC265 | 3075 |
| 266 | CC0266 | Compliance CC266 | 51 |
| 267 | CC0267 | Procurement CC267 | 2457 |
| 268 | CC0268 | R&D CC268 | 328 |
| 269 | CC0269 | Logistics CC269 | 1142 |
| 270 | CC0270 | Procurement CC270 | 217 |
| 271 | CC0271 | R&D CC271 | 2301 |
| 272 | CC0272 | Engineering CC272 | 887 |
| 273 | CC0273 | Engineering CC273 | 3901 |
| 274 | CC0274 | Support CC274 | 3704 |
| 275 | CC0275 | Support CC275 | 854 |
| 276 | CC0276 | Strategy CC276 | 3297 |
| 277 | CC0277 | Logistics CC277 | 2360 |
| 278 | CC0278 | HR CC278 | 3547 |
| 279 | CC0279 | R&D CC279 | 3350 |
| 280 | CC0280 | Treasury CC280 | 903 |
| 281 | CC0281 | Support CC281 | 3702 |
| 282 | CC0282 | IT CC282 | 1703 |
| 283 | CC0283 | Executive CC283 | 3088 |
| 284 | CC0284 | Marketing CC284 | 1760 |
| 285 | CC0285 | Operations CC285 | 2473 |
| 286 | CC0286 | Finance CC286 | 609 |
| 287 | CC0287 | Legal CC287 | 487 |
| 288 | CC0288 | Analytics CC288 | 3824 |
| 289 | CC0289 | Logistics CC289 | 1900 |
| 290 | CC0290 | IT CC290 | 1767 |
| 291 | CC0291 | Marketing CC291 | 678 |
| 292 | CC0292 | Analytics CC292 | 250 |
| 293 | CC0293 | Operations CC293 | 329 |
| 294 | CC0294 | R&D CC294 | 1270 |
| 295 | CC0295 | Compliance CC295 | 778 |
| 296 | CC0296 | IT CC296 | 1235 |
| 297 | CC0297 | R&D CC297 | 493 |
| 298 | CC0298 | Operations CC298 | 3685 |
| 299 | CC0299 | R&D CC299 | 1896 |
| 300 | CC0300 | Strategy CC300 | 2645 |
| 301 | CC0301 | Engineering CC301 | 2134 |
| 302 | CC0302 | Executive CC302 | 154 |
| 303 | CC0303 | Quality CC303 | 847 |
| 304 | CC0304 | Analytics CC304 | 285 |
| 305 | CC0305 | Strategy CC305 | 1993 |
| 306 | CC0306 | R&D CC306 | 1578 |
| 307 | CC0307 | Marketing CC307 | 3608 |
| 308 | CC0308 | Support CC308 | 1128 |
| 309 | CC0309 | HR CC309 | 3908 |
| 310 | CC0310 | Legal CC310 | 2981 |
| 311 | CC0311 | Operations CC311 | 1793 |
| 312 | CC0312 | Support CC312 | 3938 |
| 313 | CC0313 | Finance CC313 | 857 |
| 314 | CC0314 | Finance CC314 | 3713 |
| 315 | CC0315 | Operations CC315 | 1090 |
| 316 | CC0316 | Executive CC316 | 3651 |
| 317 | CC0317 | Compliance CC317 | 3797 |
| 318 | CC0318 | IT CC318 | 2956 |
| 319 | CC0319 | Treasury CC319 | 1932 |
| 320 | CC0320 | HR CC320 | 2019 |
| 321 | CC0321 | Sales CC321 | 1234 |
| 322 | CC0322 | Finance CC322 | 2871 |
| 323 | CC0323 | Legal CC323 | 3963 |
| 324 | CC0324 | Logistics CC324 | 477 |
| 325 | CC0325 | Quality CC325 | 3083 |
| 326 | CC0326 | Support CC326 | 184 |
| 327 | CC0327 | R&D CC327 | 1125 |
| 328 | CC0328 | Analytics CC328 | 440 |
| 329 | CC0329 | Risk CC329 | 1893 |
| 330 | CC0330 | Procurement CC330 | 883 |
| 331 | CC0331 | Procurement CC331 | 3960 |
| 332 | CC0332 | Logistics CC332 | 187 |
| 333 | CC0333 | Sales CC333 | 3007 |
| 334 | CC0334 | R&D CC334 | 1026 |
| 335 | CC0335 | R&D CC335 | 2058 |
| 336 | CC0336 | Marketing CC336 | 2074 |
| 337 | CC0337 | Audit CC337 | 2973 |
| 338 | CC0338 | Support CC338 | 20 |
| 339 | CC0339 | Logistics CC339 | 590 |
| 340 | CC0340 | Legal CC340 | 2196 |
| 341 | CC0341 | HR CC341 | 11 |
| 342 | CC0342 | Legal CC342 | 1537 |
| 343 | CC0343 | Treasury CC343 | 3256 |
| 344 | CC0344 | Quality CC344 | 2139 |
| 345 | CC0345 | Procurement CC345 | 3387 |
| 346 | CC0346 | Support CC346 | 1614 |
| 347 | CC0347 | Legal CC347 | 935 |
| 348 | CC0348 | Compliance CC348 | 401 |
| 349 | CC0349 | Support CC349 | 926 |
| 350 | CC0350 | Audit CC350 | 2708 |
| 351 | CC0351 | Strategy CC351 | 1401 |
| 352 | CC0352 | Support CC352 | 574 |
| 353 | CC0353 | Strategy CC353 | 2011 |
| 354 | CC0354 | IT CC354 | 3588 |
| 355 | CC0355 | Engineering CC355 | 3286 |
| 356 | CC0356 | Sales CC356 | 563 |
| 357 | CC0357 | Marketing CC357 | 2493 |
| 358 | CC0358 | Risk CC358 | 492 |
| 359 | CC0359 | Legal CC359 | 1674 |
| 360 | CC0360 | Procurement CC360 | 909 |
| 361 | CC0361 | Executive CC361 | 2282 |
| 362 | CC0362 | Legal CC362 | 795 |
| 363 | CC0363 | Treasury CC363 | 870 |
| 364 | CC0364 | Operations CC364 | 3407 |
| 365 | CC0365 | IT CC365 | 664 |
| 366 | CC0366 | Support CC366 | 1955 |
| 367 | CC0367 | Sales CC367 | 3617 |
| 368 | CC0368 | Compliance CC368 | 2256 |
| 369 | CC0369 | Strategy CC369 | 3286 |
| 370 | CC0370 | IT CC370 | 394 |
| 371 | CC0371 | Logistics CC371 | 2914 |
| 372 | CC0372 | Finance CC372 | 2969 |
| 373 | CC0373 | Marketing CC373 | 3036 |
| 374 | CC0374 | Operations CC374 | 2460 |
| 375 | CC0375 | Risk CC375 | 2224 |
| 376 | CC0376 | IT CC376 | 2712 |
| 377 | CC0377 | Treasury CC377 | 1029 |
| 378 | CC0378 | Quality CC378 | 2857 |
| 379 | CC0379 | Quality CC379 | 3398 |
| 380 | CC0380 | Operations CC380 | 3472 |
| 381 | CC0381 | Sales CC381 | 1190 |
| 382 | CC0382 | Marketing CC382 | 1217 |
| 383 | CC0383 | HR CC383 | 89 |
| 384 | CC0384 | Executive CC384 | 134 |
| 385 | CC0385 | Treasury CC385 | 1103 |
| 386 | CC0386 | Operations CC386 | 1635 |
| 387 | CC0387 | Treasury CC387 | 3080 |
| 388 | CC0388 | Logistics CC388 | 1770 |
| 389 | CC0389 | Logistics CC389 | 3491 |
| 390 | CC0390 | Support CC390 | 498 |
| 391 | CC0391 | Legal CC391 | 3274 |
| 392 | CC0392 | HR CC392 | 2105 |
| 393 | CC0393 | HR CC393 | 2823 |
| 394 | CC0394 | Engineering CC394 | 2800 |
| 395 | CC0395 | Audit CC395 | 3928 |
| 396 | CC0396 | Procurement CC396 | 1283 |
| 397 | CC0397 | Compliance CC397 | 1341 |
| 398 | CC0398 | Sales CC398 | 2803 |
| 399 | CC0399 | IT CC399 | 2048 |
| 400 | CC0400 | Strategy CC400 | 3524 |
| 401 | CC0401 | Strategy CC401 | 3960 |
| 402 | CC0402 | Legal CC402 | 478 |
| 403 | CC0403 | Executive CC403 | 1841 |
| 404 | CC0404 | Risk CC404 | 708 |
| 405 | CC0405 | Operations CC405 | 2673 |
| 406 | CC0406 | Risk CC406 | 3959 |
| 407 | CC0407 | Logistics CC407 | 3218 |
| 408 | CC0408 | Treasury CC408 | 3821 |
| 409 | CC0409 | Logistics CC409 | 2136 |
| 410 | CC0410 | Analytics CC410 | 2675 |
| 411 | CC0411 | IT CC411 | 3398 |
| 412 | CC0412 | Strategy CC412 | 3136 |
| 413 | CC0413 | Logistics CC413 | 2728 |
| 414 | CC0414 | Audit CC414 | 1463 |
| 415 | CC0415 | R&D CC415 | 2963 |
| 416 | CC0416 | Support CC416 | 3359 |
| 417 | CC0417 | Treasury CC417 | 2775 |
| 418 | CC0418 | Executive CC418 | 3645 |
| 419 | CC0419 | Audit CC419 | 2100 |
| 420 | CC0420 | Operations CC420 | 3614 |
| 421 | CC0421 | Support CC421 | 1830 |
| 422 | CC0422 | Finance CC422 | 2454 |
| 423 | CC0423 | Finance CC423 | 2384 |
| 424 | CC0424 | Strategy CC424 | 2128 |
| 425 | CC0425 | HR CC425 | 2201 |
| 426 | CC0426 | Quality CC426 | 2993 |
| 427 | CC0427 | Support CC427 | 3307 |
| 428 | CC0428 | Finance CC428 | 2076 |
| 429 | CC0429 | Support CC429 | 2602 |
| 430 | CC0430 | Strategy CC430 | 438 |
| 431 | CC0431 | Compliance CC431 | 488 |
| 432 | CC0432 | Marketing CC432 | 293 |
| 433 | CC0433 | Sales CC433 | 2612 |
| 434 | CC0434 | Support CC434 | 2807 |
| 435 | CC0435 | Procurement CC435 | 1264 |
| 436 | CC0436 | Engineering CC436 | 1412 |
| 437 | CC0437 | Quality CC437 | 114 |
| 438 | CC0438 | Treasury CC438 | 491 |
| 439 | CC0439 | Operations CC439 | 2974 |
| 440 | CC0440 | Compliance CC440 | 2235 |
| 441 | CC0441 | Engineering CC441 | 3258 |
| 442 | CC0442 | Analytics CC442 | 1702 |
| 443 | CC0443 | Logistics CC443 | 2108 |
| 444 | CC0444 | IT CC444 | 497 |
| 445 | CC0445 | Quality CC445 | 2192 |
| 446 | CC0446 | IT CC446 | 3155 |
| 447 | CC0447 | Executive CC447 | 1199 |
| 448 | CC0448 | Risk CC448 | 2413 |
| 449 | CC0449 | Compliance CC449 | 724 |
| 450 | CC0450 | Logistics CC450 | 3130 |
| 451 | CC0451 | Strategy CC451 | 1154 |
| 452 | CC0452 | Support CC452 | 3141 |
| 453 | CC0453 | HR CC453 | 1945 |
| 454 | CC0454 | Strategy CC454 | 1865 |
| 455 | CC0455 | Strategy CC455 | 1923 |
| 456 | CC0456 | Compliance CC456 | 479 |
| 457 | CC0457 | Compliance CC457 | 3779 |
| 458 | CC0458 | Finance CC458 | 1429 |
| 459 | CC0459 | Quality CC459 | 2240 |
| 460 | CC0460 | Treasury CC460 | 738 |
| 461 | CC0461 | Audit CC461 | 985 |
| 462 | CC0462 | R&D CC462 | 3516 |
| 463 | CC0463 | Analytics CC463 | 547 |
| 464 | CC0464 | Marketing CC464 | 659 |
| 465 | CC0465 | Audit CC465 | 1889 |
| 466 | CC0466 | Procurement CC466 | 277 |
| 467 | CC0467 | Marketing CC467 | 471 |
| 468 | CC0468 | Treasury CC468 | 2534 |
| 469 | CC0469 | Procurement CC469 | 2199 |
| 470 | CC0470 | Strategy CC470 | 2067 |
| 471 | CC0471 | Analytics CC471 | 2869 |
| 472 | CC0472 | R&D CC472 | 1088 |
| 473 | CC0473 | HR CC473 | 2319 |
| 474 | CC0474 | Executive CC474 | 1871 |
| 475 | CC0475 | Logistics CC475 | 1100 |
| 476 | CC0476 | Sales CC476 | 3195 |
| 477 | CC0477 | Strategy CC477 | 1704 |
| 478 | CC0478 | Logistics CC478 | 2870 |
| 479 | CC0479 | Executive CC479 | 1543 |
| 480 | CC0480 | R&D CC480 | 2585 |
| 481 | CC0481 | Operations CC481 | 1887 |
| 482 | CC0482 | Compliance CC482 | 1373 |
| 483 | CC0483 | Marketing CC483 | 1601 |
| 484 | CC0484 | Support CC484 | 988 |
| 485 | CC0485 | Procurement CC485 | 1192 |
| 486 | CC0486 | Engineering CC486 | 948 |
| 487 | CC0487 | Logistics CC487 | 2292 |
| 488 | CC0488 | IT CC488 | 1519 |
| 489 | CC0489 | Support CC489 | 2112 |
| 490 | CC0490 | Audit CC490 | 343 |
| 491 | CC0491 | Logistics CC491 | 367 |
| 492 | CC0492 | Quality CC492 | 2768 |
| 493 | CC0493 | Marketing CC493 | 565 |
| 494 | CC0494 | Analytics CC494 | 1309 |
| 495 | CC0495 | HR CC495 | 1045 |
| 496 | CC0496 | Sales CC496 | 67 |
| 497 | CC0497 | Risk CC497 | 990 |
| 498 | CC0498 | IT CC498 | 2888 |
| 499 | CC0499 | HR CC499 | 3644 |
| 500 | CC0500 | Compliance CC500 | 143 |
| 501 | CC0501 | HR CC501 | 59 |
| 502 | CC0502 | Executive CC502 | 1572 |
| 503 | CC0503 | Executive CC503 | 2177 |
| 504 | CC0504 | Support CC504 | 541 |
| 505 | CC0505 | Strategy CC505 | 3953 |
| 506 | CC0506 | Support CC506 | 1039 |
| 507 | CC0507 | Logistics CC507 | 963 |
| 508 | CC0508 | IT CC508 | 2766 |
| 509 | CC0509 | Risk CC509 | 2200 |
| 510 | CC0510 | Quality CC510 | 201 |
| 511 | CC0511 | Analytics CC511 | 1189 |
| 512 | CC0512 | Treasury CC512 | 1158 |
| 513 | CC0513 | Audit CC513 | 1218 |
| 514 | CC0514 | Procurement CC514 | 2233 |
| 515 | CC0515 | Logistics CC515 | 3117 |
| 516 | CC0516 | Analytics CC516 | 282 |
| 517 | CC0517 | Engineering CC517 | 823 |
| 518 | CC0518 | Sales CC518 | 2684 |
| 519 | CC0519 | Operations CC519 | 2845 |
| 520 | CC0520 | Risk CC520 | 2193 |
| 521 | CC0521 | Compliance CC521 | 2790 |
| 522 | CC0522 | Audit CC522 | 3880 |
| 523 | CC0523 | Treasury CC523 | 729 |
| 524 | CC0524 | Analytics CC524 | 2792 |
| 525 | CC0525 | Operations CC525 | 3203 |
| 526 | CC0526 | IT CC526 | 3708 |
| 527 | CC0527 | R&D CC527 | 586 |
| 528 | CC0528 | Treasury CC528 | 613 |
| 529 | CC0529 | Analytics CC529 | 3641 |
| 530 | CC0530 | R&D CC530 | 577 |
| 531 | CC0531 | Marketing CC531 | 6 |
| 532 | CC0532 | Compliance CC532 | 202 |
| 533 | CC0533 | IT CC533 | 2498 |
| 534 | CC0534 | Treasury CC534 | 213 |
| 535 | CC0535 | Procurement CC535 | 450 |
| 536 | CC0536 | HR CC536 | 1817 |
| 537 | CC0537 | HR CC537 | 3661 |
| 538 | CC0538 | Treasury CC538 | 161 |
| 539 | CC0539 | Treasury CC539 | 943 |
| 540 | CC0540 | Strategy CC540 | 3663 |
| 541 | CC0541 | Operations CC541 | 2656 |
| 542 | CC0542 | Audit CC542 | 2272 |
| 543 | CC0543 | Logistics CC543 | 1409 |
| 544 | CC0544 | Analytics CC544 | 1320 |
| 545 | CC0545 | Finance CC545 | 1007 |
| 546 | CC0546 | Support CC546 | 701 |
| 547 | CC0547 | Support CC547 | 3900 |
| 548 | CC0548 | Strategy CC548 | 2435 |
| 549 | CC0549 | HR CC549 | 1590 |
| 550 | CC0550 | Operations CC550 | 1329 |
| 551 | CC0551 | Support CC551 | 1443 |
| 552 | CC0552 | Audit CC552 | 3528 |
| 553 | CC0553 | Executive CC553 | 347 |
| 554 | CC0554 | Finance CC554 | 1898 |
| 555 | CC0555 | Finance CC555 | 3535 |
| 556 | CC0556 | Logistics CC556 | 3058 |
| 557 | CC0557 | Analytics CC557 | 3358 |
| 558 | CC0558 | Legal CC558 | 3851 |
| 559 | CC0559 | Analytics CC559 | 2751 |
| 560 | CC0560 | Executive CC560 | 2727 |
| 561 | CC0561 | IT CC561 | 271 |
| 562 | CC0562 | Analytics CC562 | 2805 |
| 563 | CC0563 | Support CC563 | 3490 |
| 564 | CC0564 | Treasury CC564 | 2939 |
| 565 | CC0565 | Executive CC565 | 2624 |
| 566 | CC0566 | Procurement CC566 | 2226 |
| 567 | CC0567 | Procurement CC567 | 517 |
| 568 | CC0568 | Compliance CC568 | 3241 |
| 569 | CC0569 | Operations CC569 | 826 |
| 570 | CC0570 | Quality CC570 | 3980 |
| 571 | CC0571 | Treasury CC571 | 2789 |
| 572 | CC0572 | Analytics CC572 | 671 |
| 573 | CC0573 | Analytics CC573 | 664 |
| 574 | CC0574 | Engineering CC574 | 3185 |
| 575 | CC0575 | R&D CC575 | 2168 |
| 576 | CC0576 | Sales CC576 | 1744 |
| 577 | CC0577 | Strategy CC577 | 1453 |
| 578 | CC0578 | Finance CC578 | 3012 |
| 579 | CC0579 | Marketing CC579 | 1985 |
| 580 | CC0580 | Executive CC580 | 2881 |
| 581 | CC0581 | Operations CC581 | 980 |
| 582 | CC0582 | IT CC582 | 140 |
| 583 | CC0583 | Strategy CC583 | 3396 |
| 584 | CC0584 | Support CC584 | 2328 |
| 585 | CC0585 | Logistics CC585 | 711 |
| 586 | CC0586 | Executive CC586 | 2148 |
| 587 | CC0587 | Strategy CC587 | 328 |
| 588 | CC0588 | Risk CC588 | 1152 |
| 589 | CC0589 | Engineering CC589 | 3186 |
| 590 | CC0590 | Marketing CC590 | 3243 |
| 591 | CC0591 | Finance CC591 | 1730 |
| 592 | CC0592 | Audit CC592 | 326 |
| 593 | CC0593 | Operations CC593 | 669 |
| 594 | CC0594 | Treasury CC594 | 1795 |
| 595 | CC0595 | Risk CC595 | 2995 |
| 596 | CC0596 | Operations CC596 | 1484 |
| 597 | CC0597 | Support CC597 | 3608 |
| 598 | CC0598 | Strategy CC598 | 195 |
| 599 | CC0599 | Audit CC599 | 357 |
| 600 | CC0600 | Operations CC600 | 3457 |
| 601 | CC0601 | Support CC601 | 2411 |
| 602 | CC0602 | Audit CC602 | 3488 |
| 603 | CC0603 | Engineering CC603 | 2910 |
| 604 | CC0604 | R&D CC604 | 2417 |
| 605 | CC0605 | Executive CC605 | 115 |
| 606 | CC0606 | Logistics CC606 | 2090 |
| 607 | CC0607 | Operations CC607 | 3923 |
| 608 | CC0608 | HR CC608 | 3512 |
| 609 | CC0609 | Compliance CC609 | 3363 |
| 610 | CC0610 | Treasury CC610 | 164 |
| 611 | CC0611 | Operations CC611 | 3595 |
| 612 | CC0612 | IT CC612 | 794 |
| 613 | CC0613 | Quality CC613 | 1658 |
| 614 | CC0614 | Analytics CC614 | 2484 |
| 615 | CC0615 | Risk CC615 | 2892 |
| 616 | CC0616 | Logistics CC616 | 1077 |
| 617 | CC0617 | Quality CC617 | 1221 |
| 618 | CC0618 | Operations CC618 | 1812 |
| 619 | CC0619 | HR CC619 | 1099 |
| 620 | CC0620 | R&D CC620 | 1593 |
| 621 | CC0621 | Audit CC621 | 2552 |
| 622 | CC0622 | HR CC622 | 1096 |
| 623 | CC0623 | Audit CC623 | 1918 |
| 624 | CC0624 | Legal CC624 | 2474 |
| 625 | CC0625 | IT CC625 | 23 |
| 626 | CC0626 | Marketing CC626 | 555 |
| 627 | CC0627 | Operations CC627 | 2264 |
| 628 | CC0628 | Operations CC628 | 2209 |
| 629 | CC0629 | HR CC629 | 600 |
| 630 | CC0630 | Risk CC630 | 336 |
| 631 | CC0631 | IT CC631 | 947 |
| 632 | CC0632 | Marketing CC632 | 2055 |
| 633 | CC0633 | Audit CC633 | 3297 |
| 634 | CC0634 | Support CC634 | 1728 |
| 635 | CC0635 | Treasury CC635 | 2970 |
| 636 | CC0636 | HR CC636 | 112 |
| 637 | CC0637 | R&D CC637 | 1381 |
| 638 | CC0638 | HR CC638 | 708 |
| 639 | CC0639 | Procurement CC639 | 3078 |
| 640 | CC0640 | Marketing CC640 | 1055 |
| 641 | CC0641 | HR CC641 | 2666 |
| 642 | CC0642 | Sales CC642 | 578 |
| 643 | CC0643 | Support CC643 | 2391 |
| 644 | CC0644 | Support CC644 | 3016 |
| 645 | CC0645 | Executive CC645 | 3621 |
| 646 | CC0646 | Treasury CC646 | 3835 |
| 647 | CC0647 | Finance CC647 | 2993 |
| 648 | CC0648 | R&D CC648 | 3564 |
| 649 | CC0649 | R&D CC649 | 2538 |
| 650 | CC0650 | Support CC650 | 2228 |
| 651 | CC0651 | Engineering CC651 | 225 |
| 652 | CC0652 | Executive CC652 | 3571 |
| 653 | CC0653 | Procurement CC653 | 2046 |
| 654 | CC0654 | Risk CC654 | 508 |
| 655 | CC0655 | HR CC655 | 1731 |
| 656 | CC0656 | Support CC656 | 3779 |
| 657 | CC0657 | Compliance CC657 | 3357 |
| 658 | CC0658 | Finance CC658 | 1803 |
| 659 | CC0659 | Audit CC659 | 1919 |
| 660 | CC0660 | Audit CC660 | 868 |
| 661 | CC0661 | Logistics CC661 | 3146 |
| 662 | CC0662 | HR CC662 | 1819 |
| 663 | CC0663 | Quality CC663 | 538 |
| 664 | CC0664 | HR CC664 | 2132 |
| 665 | CC0665 | Logistics CC665 | 136 |
| 666 | CC0666 | Executive CC666 | 1791 |
| 667 | CC0667 | Treasury CC667 | 1962 |
| 668 | CC0668 | Marketing CC668 | 3263 |
| 669 | CC0669 | IT CC669 | 2839 |
| 670 | CC0670 | Audit CC670 | 1316 |
| 671 | CC0671 | Marketing CC671 | 2604 |
| 672 | CC0672 | Procurement CC672 | 3171 |
| 673 | CC0673 | Procurement CC673 | 2479 |
| 674 | CC0674 | Quality CC674 | 2004 |
| 675 | CC0675 | Strategy CC675 | 1905 |
| 676 | CC0676 | Logistics CC676 | 308 |
| 677 | CC0677 | IT CC677 | 2722 |
| 678 | CC0678 | Sales CC678 | 2275 |
| 679 | CC0679 | HR CC679 | 1274 |
| 680 | CC0680 | Legal CC680 | 2570 |
| 681 | CC0681 | HR CC681 | 2734 |
| 682 | CC0682 | IT CC682 | 1908 |
| 683 | CC0683 | Support CC683 | 3303 |
| 684 | CC0684 | Procurement CC684 | 47 |
| 685 | CC0685 | Logistics CC685 | 3760 |
| 686 | CC0686 | Procurement CC686 | 2658 |
| 687 | CC0687 | Audit CC687 | 3981 |
| 688 | CC0688 | Support CC688 | 364 |
| 689 | CC0689 | Analytics CC689 | 3768 |
| 690 | CC0690 | Analytics CC690 | 2552 |
| 691 | CC0691 | Operations CC691 | 1949 |
| 692 | CC0692 | Risk CC692 | 1797 |
| 693 | CC0693 | Sales CC693 | 3340 |
| 694 | CC0694 | Quality CC694 | 354 |
| 695 | CC0695 | Audit CC695 | 2838 |
| 696 | CC0696 | HR CC696 | 610 |
| 697 | CC0697 | Support CC697 | 2894 |
| 698 | CC0698 | Engineering CC698 | 2772 |
| 699 | CC0699 | Finance CC699 | 3767 |
| 700 | CC0700 | Risk CC700 | 3344 |
| 701 | CC0701 | HR CC701 | 3694 |
| 702 | CC0702 | Operations CC702 | 1015 |
| 703 | CC0703 | Treasury CC703 | 25 |
| 704 | CC0704 | Strategy CC704 | 329 |
| 705 | CC0705 | Legal CC705 | 641 |
| 706 | CC0706 | Logistics CC706 | 791 |
| 707 | CC0707 | Executive CC707 | 3620 |
| 708 | CC0708 | Operations CC708 | 2033 |
| 709 | CC0709 | Audit CC709 | 3809 |
| 710 | CC0710 | Operations CC710 | 1517 |
| 711 | CC0711 | Compliance CC711 | 1602 |
| 712 | CC0712 | Engineering CC712 | 307 |
| 713 | CC0713 | Audit CC713 | 1339 |
| 714 | CC0714 | Operations CC714 | 2431 |
| 715 | CC0715 | R&D CC715 | 1828 |
| 716 | CC0716 | Finance CC716 | 1649 |
| 717 | CC0717 | Finance CC717 | 3786 |
| 718 | CC0718 | Quality CC718 | 3408 |
| 719 | CC0719 | Audit CC719 | 559 |
| 720 | CC0720 | Executive CC720 | 3308 |
| 721 | CC0721 | Executive CC721 | 3001 |
| 722 | CC0722 | Procurement CC722 | 2839 |
| 723 | CC0723 | Marketing CC723 | 334 |
| 724 | CC0724 | Marketing CC724 | 2770 |
| 725 | CC0725 | Support CC725 | 2002 |
| 726 | CC0726 | Legal CC726 | 1782 |
| 727 | CC0727 | Logistics CC727 | 2948 |
| 728 | CC0728 | Audit CC728 | 2771 |
| 729 | CC0729 | Marketing CC729 | 1987 |
| 730 | CC0730 | IT CC730 | 2236 |
| 731 | CC0731 | Sales CC731 | 279 |
| 732 | CC0732 | Audit CC732 | 247 |
| 733 | CC0733 | Quality CC733 | 1697 |
| 734 | CC0734 | HR CC734 | 1208 |
| 735 | CC0735 | Sales CC735 | 434 |
| 736 | CC0736 | Engineering CC736 | 3316 |
| 737 | CC0737 | Risk CC737 | 1695 |
| 738 | CC0738 | Executive CC738 | 2591 |
| 739 | CC0739 | HR CC739 | 3940 |
| 740 | CC0740 | Finance CC740 | 1742 |
| 741 | CC0741 | R&D CC741 | 278 |
| 742 | CC0742 | Procurement CC742 | 3604 |
| 743 | CC0743 | Compliance CC743 | 3353 |
| 744 | CC0744 | Operations CC744 | 362 |
| 745 | CC0745 | R&D CC745 | 2963 |
| 746 | CC0746 | Compliance CC746 | 782 |
| 747 | CC0747 | Support CC747 | 1691 |
| 748 | CC0748 | Support CC748 | 3053 |
| 749 | CC0749 | Executive CC749 | 2448 |
| 750 | CC0750 | Marketing CC750 | 3056 |
| 751 | CC0751 | Sales CC751 | 1020 |
| 752 | CC0752 | IT CC752 | 1154 |
| 753 | CC0753 | Audit CC753 | 3890 |
| 754 | CC0754 | Treasury CC754 | 2320 |
| 755 | CC0755 | Strategy CC755 | 3079 |
| 756 | CC0756 | HR CC756 | 2677 |
| 757 | CC0757 | Logistics CC757 | 3518 |
| 758 | CC0758 | Strategy CC758 | 3143 |
| 759 | CC0759 | Risk CC759 | 3023 |
| 760 | CC0760 | Sales CC760 | 648 |
| 761 | CC0761 | Audit CC761 | 1699 |
| 762 | CC0762 | Risk CC762 | 410 |
| 763 | CC0763 | HR CC763 | 2557 |
| 764 | CC0764 | Strategy CC764 | 897 |
| 765 | CC0765 | Logistics CC765 | 2846 |
| 766 | CC0766 | Risk CC766 | 1944 |
| 767 | CC0767 | Support CC767 | 2376 |
| 768 | CC0768 | Legal CC768 | 1546 |
| 769 | CC0769 | Operations CC769 | 2970 |
| 770 | CC0770 | Audit CC770 | 1431 |
| 771 | CC0771 | Sales CC771 | 623 |
| 772 | CC0772 | Finance CC772 | 1482 |
| 773 | CC0773 | Marketing CC773 | 2460 |
| 774 | CC0774 | Logistics CC774 | 2707 |
| 775 | CC0775 | Logistics CC775 | 2 |
| 776 | CC0776 | HR CC776 | 3568 |
| 777 | CC0777 | Sales CC777 | 3004 |
| 778 | CC0778 | Risk CC778 | 1203 |
| 779 | CC0779 | IT CC779 | 1935 |
| 780 | CC0780 | Support CC780 | 281 |
| 781 | CC0781 | Executive CC781 | 2067 |
| 782 | CC0782 | Procurement CC782 | 3499 |
| 783 | CC0783 | Treasury CC783 | 1570 |
| 784 | CC0784 | Risk CC784 | 2194 |
| 785 | CC0785 | Treasury CC785 | 38 |
| 786 | CC0786 | Logistics CC786 | 3784 |
| 787 | CC0787 | Logistics CC787 | 1738 |
| 788 | CC0788 | R&D CC788 | 3290 |
| 789 | CC0789 | Marketing CC789 | 3638 |
| 790 | CC0790 | Audit CC790 | 3446 |
| 791 | CC0791 | Marketing CC791 | 2437 |
| 792 | CC0792 | Engineering CC792 | 1224 |
| 793 | CC0793 | Compliance CC793 | 3140 |
| 794 | CC0794 | R&D CC794 | 3485 |
| 795 | CC0795 | Compliance CC795 | 2161 |
| 796 | CC0796 | Treasury CC796 | 2962 |
| 797 | CC0797 | Compliance CC797 | 3311 |
| 798 | CC0798 | Risk CC798 | 1224 |
| 799 | CC0799 | Compliance CC799 | 727 |
| 800 | CC0800 | Sales CC800 | 2051 |
| 801 | CC0801 | R&D CC801 | 1271 |
| 802 | CC0802 | HR CC802 | 3152 |
| 803 | CC0803 | Treasury CC803 | 1984 |
| 804 | CC0804 | Finance CC804 | 1564 |
| 805 | CC0805 | Audit CC805 | 2722 |
| 806 | CC0806 | Procurement CC806 | 328 |
| 807 | CC0807 | Treasury CC807 | 2569 |
| 808 | CC0808 | Marketing CC808 | 12 |
| 809 | CC0809 | Sales CC809 | 2797 |
| 810 | CC0810 | Strategy CC810 | 3532 |
| 811 | CC0811 | Quality CC811 | 3198 |
| 812 | CC0812 | Procurement CC812 | 2873 |
| 813 | CC0813 | Procurement CC813 | 1464 |
| 814 | CC0814 | IT CC814 | 1260 |
| 815 | CC0815 | Procurement CC815 | 417 |
| 816 | CC0816 | Operations CC816 | 2528 |
| 817 | CC0817 | HR CC817 | 3755 |
| 818 | CC0818 | Executive CC818 | 1956 |
| 819 | CC0819 | Marketing CC819 | 67 |
| 820 | CC0820 | HR CC820 | 1151 |
| 821 | CC0821 | Sales CC821 | 620 |
| 822 | CC0822 | R&D CC822 | 1649 |
| 823 | CC0823 | Legal CC823 | 3056 |
| 824 | CC0824 | Risk CC824 | 3017 |
| 825 | CC0825 | Risk CC825 | 986 |
| 826 | CC0826 | R&D CC826 | 3460 |
| 827 | CC0827 | Quality CC827 | 1743 |
| 828 | CC0828 | Engineering CC828 | 2414 |
| 829 | CC0829 | R&D CC829 | 709 |
| 830 | CC0830 | IT CC830 | 859 |
| 831 | CC0831 | HR CC831 | 1536 |
| 832 | CC0832 | IT CC832 | 2532 |
| 833 | CC0833 | Logistics CC833 | 3370 |
| 834 | CC0834 | Marketing CC834 | 1166 |
| 835 | CC0835 | Engineering CC835 | 3777 |
| 836 | CC0836 | Procurement CC836 | 2896 |
| 837 | CC0837 | IT CC837 | 1785 |
| 838 | CC0838 | Executive CC838 | 2048 |
| 839 | CC0839 | Legal CC839 | 3914 |
| 840 | CC0840 | Engineering CC840 | 1104 |
| 841 | CC0841 | Engineering CC841 | 3900 |
| 842 | CC0842 | Engineering CC842 | 41 |
| 843 | CC0843 | Strategy CC843 | 2154 |
| 844 | CC0844 | Risk CC844 | 188 |
| 845 | CC0845 | Legal CC845 | 999 |
| 846 | CC0846 | Quality CC846 | 1815 |
| 847 | CC0847 | Treasury CC847 | 1178 |
| 848 | CC0848 | R&D CC848 | 3973 |
| 849 | CC0849 | Support CC849 | 2431 |
| 850 | CC0850 | Audit CC850 | 651 |
| 851 | CC0851 | Analytics CC851 | 1804 |
| 852 | CC0852 | Executive CC852 | 3327 |
| 853 | CC0853 | Treasury CC853 | 2835 |
| 854 | CC0854 | Audit CC854 | 429 |
| 855 | CC0855 | Sales CC855 | 1823 |
| 856 | CC0856 | Marketing CC856 | 3605 |
| 857 | CC0857 | Risk CC857 | 2899 |
| 858 | CC0858 | Support CC858 | 3127 |
| 859 | CC0859 | Sales CC859 | 3997 |
| 860 | CC0860 | Strategy CC860 | 2385 |
| 861 | CC0861 | HR CC861 | 168 |
| 862 | CC0862 | Strategy CC862 | 301 |
| 863 | CC0863 | Procurement CC863 | 1451 |
| 864 | CC0864 | Support CC864 | 1490 |
| 865 | CC0865 | HR CC865 | 2576 |
| 866 | CC0866 | Marketing CC866 | 3093 |
| 867 | CC0867 | Engineering CC867 | 2880 |
| 868 | CC0868 | Risk CC868 | 1674 |
| 869 | CC0869 | Audit CC869 | 1746 |
| 870 | CC0870 | IT CC870 | 3763 |
| 871 | CC0871 | Marketing CC871 | 2428 |
| 872 | CC0872 | Analytics CC872 | 3214 |
| 873 | CC0873 | Procurement CC873 | 843 |
| 874 | CC0874 | Risk CC874 | 631 |
| 875 | CC0875 | Legal CC875 | 2737 |
| 876 | CC0876 | IT CC876 | 2025 |
| 877 | CC0877 | R&D CC877 | 2780 |
| 878 | CC0878 | Marketing CC878 | 2639 |
| 879 | CC0879 | Compliance CC879 | 1629 |
| 880 | CC0880 | IT CC880 | 3387 |
| 881 | CC0881 | Procurement CC881 | 1084 |
| 882 | CC0882 | Engineering CC882 | 1064 |
| 883 | CC0883 | Executive CC883 | 1387 |
| 884 | CC0884 | IT CC884 | 3974 |
| 885 | CC0885 | Operations CC885 | 1909 |
| 886 | CC0886 | HR CC886 | 2814 |
| 887 | CC0887 | Legal CC887 | 2271 |
| 888 | CC0888 | Finance CC888 | 552 |
| 889 | CC0889 | Sales CC889 | 800 |
| 890 | CC0890 | Executive CC890 | 52 |
| 891 | CC0891 | Support CC891 | 377 |
| 892 | CC0892 | Logistics CC892 | 1811 |
| 893 | CC0893 | Risk CC893 | 2589 |
| 894 | CC0894 | Support CC894 | 2697 |
| 895 | CC0895 | Procurement CC895 | 3854 |
| 896 | CC0896 | Executive CC896 | 2361 |
| 897 | CC0897 | Finance CC897 | 3069 |
| 898 | CC0898 | Procurement CC898 | 433 |
| 899 | CC0899 | Compliance CC899 | 1906 |
| 900 | CC0900 | HR CC900 | 1216 |
| 901 | CC0901 | Audit CC901 | 1672 |
| 902 | CC0902 | Treasury CC902 | 526 |
| 903 | CC0903 | Sales CC903 | 554 |
| 904 | CC0904 | Treasury CC904 | 413 |
| 905 | CC0905 | Analytics CC905 | 3996 |
| 906 | CC0906 | Strategy CC906 | 3777 |
| 907 | CC0907 | Analytics CC907 | 2845 |
| 908 | CC0908 | Legal CC908 | 2250 |
| 909 | CC0909 | Audit CC909 | 3433 |
| 910 | CC0910 | Strategy CC910 | 2409 |
| 911 | CC0911 | Treasury CC911 | 2873 |
| 912 | CC0912 | HR CC912 | 1120 |
| 913 | CC0913 | IT CC913 | 2007 |
| 914 | CC0914 | Support CC914 | 999 |
| 915 | CC0915 | Logistics CC915 | 1047 |
| 916 | CC0916 | Risk CC916 | 2014 |
| 917 | CC0917 | Marketing CC917 | 2024 |
| 918 | CC0918 | Sales CC918 | 1474 |
| 919 | CC0919 | Logistics CC919 | 369 |
| 920 | CC0920 | Operations CC920 | 1247 |
| 921 | CC0921 | Engineering CC921 | 698 |
| 922 | CC0922 | Finance CC922 | 3585 |
| 923 | CC0923 | Procurement CC923 | 466 |
| 924 | CC0924 | Compliance CC924 | 1295 |
| 925 | CC0925 | Audit CC925 | 1161 |
| 926 | CC0926 | Risk CC926 | 1454 |
| 927 | CC0927 | Quality CC927 | 2687 |
| 928 | CC0928 | Strategy CC928 | 1546 |
| 929 | CC0929 | Sales CC929 | 2189 |
| 930 | CC0930 | Treasury CC930 | 1519 |
| 931 | CC0931 | IT CC931 | 2625 |
| 932 | CC0932 | Executive CC932 | 92 |
| 933 | CC0933 | Executive CC933 | 71 |
| 934 | CC0934 | Quality CC934 | 2800 |
| 935 | CC0935 | Risk CC935 | 1064 |
| 936 | CC0936 | Compliance CC936 | 1992 |
| 937 | CC0937 | Strategy CC937 | 1282 |
| 938 | CC0938 | Logistics CC938 | 3643 |
| 939 | CC0939 | Treasury CC939 | 3982 |
| 940 | CC0940 | Engineering CC940 | 2870 |
| 941 | CC0941 | Finance CC941 | 266 |
| 942 | CC0942 | Finance CC942 | 3705 |
| 943 | CC0943 | Procurement CC943 | 1714 |
| 944 | CC0944 | HR CC944 | 2702 |
| 945 | CC0945 | Support CC945 | 2858 |
| 946 | CC0946 | Operations CC946 | 3587 |
| 947 | CC0947 | Executive CC947 | 647 |
| 948 | CC0948 | Legal CC948 | 3807 |
| 949 | CC0949 | Treasury CC949 | 1411 |
| 950 | CC0950 | Quality CC950 | 1106 |
| 951 | CC0951 | Compliance CC951 | 114 |
| 952 | CC0952 | Audit CC952 | 3797 |
| 953 | CC0953 | Analytics CC953 | 3964 |
| 954 | CC0954 | Sales CC954 | 965 |
| 955 | CC0955 | R&D CC955 | 2775 |
| 956 | CC0956 | HR CC956 | 3459 |
| 957 | CC0957 | Treasury CC957 | 2896 |
| 958 | CC0958 | Logistics CC958 | 2660 |
| 959 | CC0959 | Legal CC959 | 3588 |
| 960 | CC0960 | Finance CC960 | 168 |
| 961 | CC0961 | Logistics CC961 | 1267 |
| 962 | CC0962 | Support CC962 | 443 |
| 963 | CC0963 | Marketing CC963 | 3100 |
| 964 | CC0964 | Compliance CC964 | 1153 |
| 965 | CC0965 | Strategy CC965 | 3668 |
| 966 | CC0966 | IT CC966 | 2183 |
| 967 | CC0967 | Sales CC967 | 3701 |
| 968 | CC0968 | Analytics CC968 | 444 |
| 969 | CC0969 | Finance CC969 | 3013 |
| 970 | CC0970 | Treasury CC970 | 1608 |
| 971 | CC0971 | Legal CC971 | 2559 |
| 972 | CC0972 | Strategy CC972 | 2046 |
| 973 | CC0973 | Analytics CC973 | 3299 |
| 974 | CC0974 | Legal CC974 | 2111 |
| 975 | CC0975 | Legal CC975 | 2097 |
| 976 | CC0976 | Strategy CC976 | 3041 |
| 977 | CC0977 | Sales CC977 | 815 |
| 978 | CC0978 | HR CC978 | 1080 |
| 979 | CC0979 | Executive CC979 | 891 |
| 980 | CC0980 | Quality CC980 | 449 |
| 981 | CC0981 | Procurement CC981 | 2600 |
| 982 | CC0982 | Procurement CC982 | 807 |
| 983 | CC0983 | HR CC983 | 3904 |
| 984 | CC0984 | Executive CC984 | 2158 |
| 985 | CC0985 | HR CC985 | 1968 |
| 986 | CC0986 | Legal CC986 | 1111 |
| 987 | CC0987 | R&D CC987 | 3393 |
| 988 | CC0988 | Marketing CC988 | 3417 |
| 989 | CC0989 | Compliance CC989 | 750 |
| 990 | CC0990 | Finance CC990 | 1239 |
| 991 | CC0991 | Quality CC991 | 3519 |
| 992 | CC0992 | Finance CC992 | 387 |
| 993 | CC0993 | Audit CC993 | 861 |
| 994 | CC0994 | Finance CC994 | 3080 |
| 995 | CC0995 | Procurement CC995 | 2869 |
| 996 | CC0996 | Quality CC996 | 950 |
| 997 | CC0997 | Marketing CC997 | 3618 |
| 998 | CC0998 | Sales CC998 | 1437 |
| 999 | CC0999 | Legal CC999 | 2400 |
| 1000 | CC1000 | IT CC1000 | 1082 |
| 1001 | CC1001 | Audit CC1001 | 3461 |
| 1002 | CC1002 | Treasury CC1002 | 2583 |
| 1003 | CC1003 | Procurement CC1003 | 3265 |
| 1004 | CC1004 | Finance CC1004 | 1521 |
| 1005 | CC1005 | IT CC1005 | 130 |
| 1006 | CC1006 | Compliance CC1006 | 3323 |
| 1007 | CC1007 | Logistics CC1007 | 3666 |
| 1008 | CC1008 | Engineering CC1008 | 3116 |
| 1009 | CC1009 | Operations CC1009 | 3958 |
| 1010 | CC1010 | Finance CC1010 | 3488 |
| 1011 | CC1011 | R&D CC1011 | 1583 |
| 1012 | CC1012 | Engineering CC1012 | 3857 |
| 1013 | CC1013 | Marketing CC1013 | 3542 |
| 1014 | CC1014 | Procurement CC1014 | 2803 |
| 1015 | CC1015 | Executive CC1015 | 719 |
| 1016 | CC1016 | IT CC1016 | 1375 |
| 1017 | CC1017 | Logistics CC1017 | 2055 |
| 1018 | CC1018 | Strategy CC1018 | 2457 |
| 1019 | CC1019 | HR CC1019 | 917 |
| 1020 | CC1020 | Procurement CC1020 | 2863 |
| 1021 | CC1021 | Legal CC1021 | 454 |
| 1022 | CC1022 | Strategy CC1022 | 2191 |
| 1023 | CC1023 | Marketing CC1023 | 983 |
| 1024 | CC1024 | Finance CC1024 | 1048 |
| 1025 | CC1025 | Procurement CC1025 | 2006 |
| 1026 | CC1026 | Treasury CC1026 | 240 |
| 1027 | CC1027 | Quality CC1027 | 1356 |
| 1028 | CC1028 | HR CC1028 | 2558 |
| 1029 | CC1029 | Treasury CC1029 | 1574 |
| 1030 | CC1030 | Support CC1030 | 2557 |
| 1031 | CC1031 | Risk CC1031 | 2421 |
| 1032 | CC1032 | Finance CC1032 | 1341 |
| 1033 | CC1033 | Logistics CC1033 | 1342 |
| 1034 | CC1034 | Support CC1034 | 3674 |
| 1035 | CC1035 | Engineering CC1035 | 3720 |
| 1036 | CC1036 | Strategy CC1036 | 1220 |
| 1037 | CC1037 | Marketing CC1037 | 229 |
| 1038 | CC1038 | Analytics CC1038 | 931 |
| 1039 | CC1039 | Treasury CC1039 | 510 |
| 1040 | CC1040 | IT CC1040 | 1001 |
| 1041 | CC1041 | HR CC1041 | 1401 |
| 1042 | CC1042 | Quality CC1042 | 2964 |
| 1043 | CC1043 | Engineering CC1043 | 830 |
| 1044 | CC1044 | Operations CC1044 | 1661 |
| 1045 | CC1045 | IT CC1045 | 2176 |
| 1046 | CC1046 | Audit CC1046 | 2284 |
| 1047 | CC1047 | Analytics CC1047 | 2757 |
| 1048 | CC1048 | R&D CC1048 | 181 |
| 1049 | CC1049 | Risk CC1049 | 1271 |
| 1050 | CC1050 | Executive CC1050 | 1549 |
| 1051 | CC1051 | HR CC1051 | 834 |
| 1052 | CC1052 | Audit CC1052 | 1907 |
| 1053 | CC1053 | Quality CC1053 | 3844 |
| 1054 | CC1054 | Sales CC1054 | 3730 |
| 1055 | CC1055 | R&D CC1055 | 1691 |
| 1056 | CC1056 | Strategy CC1056 | 225 |
| 1057 | CC1057 | Support CC1057 | 2841 |
| 1058 | CC1058 | Marketing CC1058 | 80 |
| 1059 | CC1059 | Compliance CC1059 | 3083 |
| 1060 | CC1060 | R&D CC1060 | 3954 |
| 1061 | CC1061 | IT CC1061 | 4000 |
| 1062 | CC1062 | Engineering CC1062 | 3463 |
| 1063 | CC1063 | Strategy CC1063 | 3918 |
| 1064 | CC1064 | Marketing CC1064 | 2989 |
| 1065 | CC1065 | IT CC1065 | 2933 |
| 1066 | CC1066 | R&D CC1066 | 2032 |
| 1067 | CC1067 | Executive CC1067 | 3174 |
| 1068 | CC1068 | Logistics CC1068 | 1605 |
| 1069 | CC1069 | Executive CC1069 | 3155 |
| 1070 | CC1070 | Compliance CC1070 | 3773 |
| 1071 | CC1071 | Executive CC1071 | 3599 |
| 1072 | CC1072 | Sales CC1072 | 2553 |
| 1073 | CC1073 | R&D CC1073 | 1807 |
| 1074 | CC1074 | Strategy CC1074 | 2955 |
| 1075 | CC1075 | Logistics CC1075 | 1097 |
| 1076 | CC1076 | Marketing CC1076 | 3828 |
| 1077 | CC1077 | Analytics CC1077 | 2755 |
| 1078 | CC1078 | Analytics CC1078 | 2260 |
| 1079 | CC1079 | Analytics CC1079 | 3028 |
| 1080 | CC1080 | Logistics CC1080 | 2373 |
| 1081 | CC1081 | HR CC1081 | 1453 |
| 1082 | CC1082 | R&D CC1082 | 1207 |
| 1083 | CC1083 | Procurement CC1083 | 890 |
| 1084 | CC1084 | Executive CC1084 | 3597 |
| 1085 | CC1085 | Audit CC1085 | 3918 |
| 1086 | CC1086 | Engineering CC1086 | 1529 |
| 1087 | CC1087 | Engineering CC1087 | 1333 |
| 1088 | CC1088 | Finance CC1088 | 2061 |
| 1089 | CC1089 | Executive CC1089 | 332 |
| 1090 | CC1090 | R&D CC1090 | 2606 |
| 1091 | CC1091 | Quality CC1091 | 231 |
| 1092 | CC1092 | Logistics CC1092 | 2127 |
| 1093 | CC1093 | Strategy CC1093 | 1662 |
| 1094 | CC1094 | Executive CC1094 | 579 |
| 1095 | CC1095 | Procurement CC1095 | 1229 |
| 1096 | CC1096 | HR CC1096 | 3482 |
| 1097 | CC1097 | Compliance CC1097 | 3599 |
| 1098 | CC1098 | Support CC1098 | 3975 |
| 1099 | CC1099 | Analytics CC1099 | 1379 |
| 1100 | CC1100 | Quality CC1100 | 293 |
| 1101 | CC1101 | Support CC1101 | 965 |
| 1102 | CC1102 | IT CC1102 | 2373 |
| 1103 | CC1103 | Quality CC1103 | 3274 |
| 1104 | CC1104 | Quality CC1104 | 915 |
| 1105 | CC1105 | Legal CC1105 | 3255 |
| 1106 | CC1106 | Support CC1106 | 1412 |
| 1107 | CC1107 | Legal CC1107 | 2204 |
| 1108 | CC1108 | Legal CC1108 | 565 |
| 1109 | CC1109 | Logistics CC1109 | 2217 |
| 1110 | CC1110 | Support CC1110 | 2440 |
| 1111 | CC1111 | Compliance CC1111 | 898 |
| 1112 | CC1112 | Analytics CC1112 | 2681 |
| 1113 | CC1113 | Compliance CC1113 | 1419 |
| 1114 | CC1114 | Legal CC1114 | 708 |
| 1115 | CC1115 | Treasury CC1115 | 744 |
| 1116 | CC1116 | R&D CC1116 | 3359 |
| 1117 | CC1117 | Treasury CC1117 | 1841 |
| 1118 | CC1118 | HR CC1118 | 2146 |
| 1119 | CC1119 | Audit CC1119 | 1939 |
| 1120 | CC1120 | Risk CC1120 | 1642 |
| 1121 | CC1121 | R&D CC1121 | 177 |
| 1122 | CC1122 | IT CC1122 | 3642 |
| 1123 | CC1123 | Treasury CC1123 | 1254 |
| 1124 | CC1124 | Audit CC1124 | 840 |
| 1125 | CC1125 | Strategy CC1125 | 2036 |
| 1126 | CC1126 | Finance CC1126 | 1353 |
| 1127 | CC1127 | Logistics CC1127 | 2665 |
| 1128 | CC1128 | Treasury CC1128 | 3022 |
| 1129 | CC1129 | Support CC1129 | 2160 |
| 1130 | CC1130 | Strategy CC1130 | 507 |
| 1131 | CC1131 | Risk CC1131 | 3491 |
| 1132 | CC1132 | Quality CC1132 | 2295 |
| 1133 | CC1133 | Strategy CC1133 | 1281 |
| 1134 | CC1134 | Sales CC1134 | 3079 |
| 1135 | CC1135 | Executive CC1135 | 2546 |
| 1136 | CC1136 | IT CC1136 | 3189 |
| 1137 | CC1137 | Sales CC1137 | 626 |
| 1138 | CC1138 | Strategy CC1138 | 85 |
| 1139 | CC1139 | Risk CC1139 | 1294 |
| 1140 | CC1140 | Engineering CC1140 | 2754 |
| 1141 | CC1141 | Treasury CC1141 | 237 |
| 1142 | CC1142 | Strategy CC1142 | 1774 |
| 1143 | CC1143 | Executive CC1143 | 1540 |
| 1144 | CC1144 | Treasury CC1144 | 470 |
| 1145 | CC1145 | Treasury CC1145 | 931 |
| 1146 | CC1146 | Procurement CC1146 | 2408 |
| 1147 | CC1147 | Sales CC1147 | 3090 |
| 1148 | CC1148 | Finance CC1148 | 2544 |
| 1149 | CC1149 | IT CC1149 | 1665 |
| 1150 | CC1150 | Risk CC1150 | 2977 |
| 1151 | CC1151 | HR CC1151 | 2014 |
| 1152 | CC1152 | Engineering CC1152 | 783 |
| 1153 | CC1153 | Finance CC1153 | 3580 |
| 1154 | CC1154 | Operations CC1154 | 1547 |
| 1155 | CC1155 | Risk CC1155 | 1834 |
| 1156 | CC1156 | Analytics CC1156 | 199 |
| 1157 | CC1157 | Marketing CC1157 | 2129 |
| 1158 | CC1158 | R&D CC1158 | 2814 |
| 1159 | CC1159 | HR CC1159 | 1037 |
| 1160 | CC1160 | Risk CC1160 | 2626 |
| 1161 | CC1161 | IT CC1161 | 1230 |
| 1162 | CC1162 | Treasury CC1162 | 2748 |
| 1163 | CC1163 | Strategy CC1163 | 1465 |
| 1164 | CC1164 | Audit CC1164 | 1607 |
| 1165 | CC1165 | Executive CC1165 | 2414 |
| 1166 | CC1166 | Logistics CC1166 | 1418 |
| 1167 | CC1167 | Executive CC1167 | 184 |
| 1168 | CC1168 | Risk CC1168 | 509 |
| 1169 | CC1169 | Quality CC1169 | 3928 |
| 1170 | CC1170 | Analytics CC1170 | 3761 |
| 1171 | CC1171 | Strategy CC1171 | 3330 |
| 1172 | CC1172 | Procurement CC1172 | 1092 |
| 1173 | CC1173 | Audit CC1173 | 224 |
| 1174 | CC1174 | Sales CC1174 | 2778 |
| 1175 | CC1175 | Legal CC1175 | 420 |
| 1176 | CC1176 | Support CC1176 | 1850 |
| 1177 | CC1177 | IT CC1177 | 661 |
| 1178 | CC1178 | Executive CC1178 | 1163 |
| 1179 | CC1179 | Procurement CC1179 | 2672 |
| 1180 | CC1180 | Procurement CC1180 | 245 |
| 1181 | CC1181 | Legal CC1181 | 2843 |
| 1182 | CC1182 | Quality CC1182 | 2297 |
| 1183 | CC1183 | Sales CC1183 | 2502 |
| 1184 | CC1184 | Support CC1184 | 2917 |
| 1185 | CC1185 | R&D CC1185 | 830 |
| 1186 | CC1186 | Treasury CC1186 | 2350 |
| 1187 | CC1187 | Finance CC1187 | 1845 |
| 1188 | CC1188 | Quality CC1188 | 1785 |
| 1189 | CC1189 | Marketing CC1189 | 1066 |
| 1190 | CC1190 | Risk CC1190 | 2716 |
| 1191 | CC1191 | IT CC1191 | 608 |
| 1192 | CC1192 | Strategy CC1192 | 716 |
| 1193 | CC1193 | Legal CC1193 | 1370 |
| 1194 | CC1194 | Strategy CC1194 | 394 |
| 1195 | CC1195 | Procurement CC1195 | 599 |
| 1196 | CC1196 | Treasury CC1196 | 1055 |
| 1197 | CC1197 | HR CC1197 | 11 |
| 1198 | CC1198 | Treasury CC1198 | 3808 |
| 1199 | CC1199 | Engineering CC1199 | 1030 |
| 1200 | CC1200 | HR CC1200 | 534 |
| 1201 | CC1201 | HR CC1201 | 1417 |
| 1202 | CC1202 | HR CC1202 | 59 |
| 1203 | CC1203 | IT CC1203 | 2651 |
| 1204 | CC1204 | Strategy CC1204 | 2707 |
| 1205 | CC1205 | Engineering CC1205 | 1819 |
| 1206 | CC1206 | IT CC1206 | 3803 |
| 1207 | CC1207 | Operations CC1207 | 2365 |
| 1208 | CC1208 | Marketing CC1208 | 3946 |
| 1209 | CC1209 | Sales CC1209 | 3210 |
| 1210 | CC1210 | Finance CC1210 | 3622 |
| 1211 | CC1211 | Analytics CC1211 | 1575 |
| 1212 | CC1212 | HR CC1212 | 3298 |
| 1213 | CC1213 | Risk CC1213 | 3410 |
| 1214 | CC1214 | Engineering CC1214 | 2136 |
| 1215 | CC1215 | Marketing CC1215 | 29 |
| 1216 | CC1216 | Risk CC1216 | 2139 |
| 1217 | CC1217 | Analytics CC1217 | 194 |
| 1218 | CC1218 | Sales CC1218 | 1185 |
| 1219 | CC1219 | HR CC1219 | 2787 |
| 1220 | CC1220 | Marketing CC1220 | 8 |
| 1221 | CC1221 | Support CC1221 | 2274 |
| 1222 | CC1222 | Procurement CC1222 | 2681 |
| 1223 | CC1223 | Logistics CC1223 | 1059 |
| 1224 | CC1224 | HR CC1224 | 1493 |
| 1225 | CC1225 | Compliance CC1225 | 729 |
| 1226 | CC1226 | Procurement CC1226 | 718 |
| 1227 | CC1227 | Analytics CC1227 | 3831 |
| 1228 | CC1228 | Procurement CC1228 | 443 |
| 1229 | CC1229 | Support CC1229 | 1820 |
| 1230 | CC1230 | HR CC1230 | 721 |
| 1231 | CC1231 | Logistics CC1231 | 2111 |
| 1232 | CC1232 | Finance CC1232 | 3216 |
| 1233 | CC1233 | Finance CC1233 | 402 |
| 1234 | CC1234 | Engineering CC1234 | 3932 |
| 1235 | CC1235 | Operations CC1235 | 57 |
| 1236 | CC1236 | Executive CC1236 | 2482 |
| 1237 | CC1237 | Legal CC1237 | 3254 |
| 1238 | CC1238 | Legal CC1238 | 3879 |
| 1239 | CC1239 | Logistics CC1239 | 1525 |
| 1240 | CC1240 | Operations CC1240 | 2529 |
| 1241 | CC1241 | Analytics CC1241 | 3304 |
| 1242 | CC1242 | Engineering CC1242 | 2321 |
| 1243 | CC1243 | Analytics CC1243 | 2255 |
| 1244 | CC1244 | Support CC1244 | 1658 |
| 1245 | CC1245 | Support CC1245 | 3840 |
| 1246 | CC1246 | Strategy CC1246 | 1356 |
| 1247 | CC1247 | Legal CC1247 | 1742 |
| 1248 | CC1248 | Strategy CC1248 | 1800 |
| 1249 | CC1249 | Quality CC1249 | 3851 |
| 1250 | CC1250 | Risk CC1250 | 1756 |
| 1251 | CC1251 | Quality CC1251 | 1361 |
| 1252 | CC1252 | Analytics CC1252 | 1974 |
| 1253 | CC1253 | Legal CC1253 | 1953 |
| 1254 | CC1254 | Legal CC1254 | 689 |
| 1255 | CC1255 | Finance CC1255 | 151 |
| 1256 | CC1256 | Strategy CC1256 | 3884 |
| 1257 | CC1257 | Engineering CC1257 | 3888 |
| 1258 | CC1258 | Procurement CC1258 | 1927 |
| 1259 | CC1259 | Operations CC1259 | 2767 |
| 1260 | CC1260 | Logistics CC1260 | 467 |
| 1261 | CC1261 | Analytics CC1261 | 748 |
| 1262 | CC1262 | Treasury CC1262 | 304 |
| 1263 | CC1263 | Compliance CC1263 | 1185 |
| 1264 | CC1264 | Treasury CC1264 | 727 |
| 1265 | CC1265 | Executive CC1265 | 2650 |
| 1266 | CC1266 | R&D CC1266 | 303 |
| 1267 | CC1267 | Finance CC1267 | 981 |
| 1268 | CC1268 | Compliance CC1268 | 3355 |
| 1269 | CC1269 | Analytics CC1269 | 137 |
| 1270 | CC1270 | Executive CC1270 | 2506 |
| 1271 | CC1271 | Marketing CC1271 | 2282 |
| 1272 | CC1272 | Audit CC1272 | 702 |
| 1273 | CC1273 | Risk CC1273 | 2785 |
| 1274 | CC1274 | Logistics CC1274 | 483 |
| 1275 | CC1275 | Legal CC1275 | 632 |
| 1276 | CC1276 | Audit CC1276 | 1442 |
| 1277 | CC1277 | HR CC1277 | 2366 |
| 1278 | CC1278 | Logistics CC1278 | 662 |
| 1279 | CC1279 | Quality CC1279 | 999 |
| 1280 | CC1280 | IT CC1280 | 1482 |
| 1281 | CC1281 | Sales CC1281 | 878 |
| 1282 | CC1282 | HR CC1282 | 364 |
| 1283 | CC1283 | Strategy CC1283 | 2731 |
| 1284 | CC1284 | Operations CC1284 | 2925 |
| 1285 | CC1285 | Treasury CC1285 | 1473 |
| 1286 | CC1286 | Compliance CC1286 | 981 |
| 1287 | CC1287 | Audit CC1287 | 2969 |
| 1288 | CC1288 | Risk CC1288 | 251 |
| 1289 | CC1289 | Support CC1289 | 1683 |
| 1290 | CC1290 | Procurement CC1290 | 673 |
| 1291 | CC1291 | Executive CC1291 | 2331 |
| 1292 | CC1292 | Marketing CC1292 | 3669 |
| 1293 | CC1293 | Finance CC1293 | 153 |
| 1294 | CC1294 | IT CC1294 | 840 |
| 1295 | CC1295 | Support CC1295 | 376 |
| 1296 | CC1296 | Marketing CC1296 | 3639 |
| 1297 | CC1297 | Risk CC1297 | 653 |
| 1298 | CC1298 | Risk CC1298 | 1256 |
| 1299 | CC1299 | Procurement CC1299 | 3668 |
| 1300 | CC1300 | Legal CC1300 | 862 |
| 1301 | CC1301 | Operations CC1301 | 3262 |
| 1302 | CC1302 | Marketing CC1302 | 2274 |
| 1303 | CC1303 | Support CC1303 | 2539 |
| 1304 | CC1304 | Engineering CC1304 | 1122 |
| 1305 | CC1305 | Quality CC1305 | 1896 |
| 1306 | CC1306 | Risk CC1306 | 169 |
| 1307 | CC1307 | HR CC1307 | 886 |
| 1308 | CC1308 | Audit CC1308 | 3476 |
| 1309 | CC1309 | Risk CC1309 | 421 |
| 1310 | CC1310 | Executive CC1310 | 89 |
| 1311 | CC1311 | Finance CC1311 | 1050 |
| 1312 | CC1312 | Procurement CC1312 | 1842 |
| 1313 | CC1313 | Analytics CC1313 | 125 |
| 1314 | CC1314 | Audit CC1314 | 327 |
| 1315 | CC1315 | R&D CC1315 | 289 |
| 1316 | CC1316 | Engineering CC1316 | 3654 |
| 1317 | CC1317 | Audit CC1317 | 3667 |
| 1318 | CC1318 | R&D CC1318 | 3706 |
| 1319 | CC1319 | R&D CC1319 | 1957 |
| 1320 | CC1320 | Sales CC1320 | 777 |
| 1321 | CC1321 | Treasury CC1321 | 345 |
| 1322 | CC1322 | Risk CC1322 | 447 |
| 1323 | CC1323 | Engineering CC1323 | 1165 |
| 1324 | CC1324 | Sales CC1324 | 154 |
| 1325 | CC1325 | R&D CC1325 | 2653 |
| 1326 | CC1326 | HR CC1326 | 3850 |
| 1327 | CC1327 | Risk CC1327 | 2713 |
| 1328 | CC1328 | Audit CC1328 | 3472 |
| 1329 | CC1329 | HR CC1329 | 3097 |
| 1330 | CC1330 | Sales CC1330 | 2111 |
| 1331 | CC1331 | Quality CC1331 | 2376 |
| 1332 | CC1332 | Logistics CC1332 | 773 |
| 1333 | CC1333 | Analytics CC1333 | 1645 |
| 1334 | CC1334 | Procurement CC1334 | 3131 |
| 1335 | CC1335 | R&D CC1335 | 3209 |
| 1336 | CC1336 | Analytics CC1336 | 981 |
| 1337 | CC1337 | Support CC1337 | 1380 |
| 1338 | CC1338 | Analytics CC1338 | 3257 |
| 1339 | CC1339 | Compliance CC1339 | 2833 |
| 1340 | CC1340 | Analytics CC1340 | 1423 |
| 1341 | CC1341 | Logistics CC1341 | 1870 |
| 1342 | CC1342 | Engineering CC1342 | 829 |
| 1343 | CC1343 | HR CC1343 | 2594 |
| 1344 | CC1344 | Executive CC1344 | 705 |
| 1345 | CC1345 | Treasury CC1345 | 68 |
| 1346 | CC1346 | Logistics CC1346 | 2642 |
| 1347 | CC1347 | Operations CC1347 | 952 |
| 1348 | CC1348 | R&D CC1348 | 453 |
| 1349 | CC1349 | Strategy CC1349 | 311 |
| 1350 | CC1350 | Marketing CC1350 | 822 |
| 1351 | CC1351 | Analytics CC1351 | 3333 |
| 1352 | CC1352 | Executive CC1352 | 2080 |
| 1353 | CC1353 | Procurement CC1353 | 943 |
| 1354 | CC1354 | Analytics CC1354 | 1356 |
| 1355 | CC1355 | Marketing CC1355 | 1999 |
| 1356 | CC1356 | Treasury CC1356 | 2761 |
| 1357 | CC1357 | Logistics CC1357 | 2056 |
| 1358 | CC1358 | Sales CC1358 | 1997 |
| 1359 | CC1359 | Legal CC1359 | 3192 |
| 1360 | CC1360 | Support CC1360 | 2835 |
| 1361 | CC1361 | Marketing CC1361 | 2190 |
| 1362 | CC1362 | Logistics CC1362 | 1692 |
| 1363 | CC1363 | Compliance CC1363 | 3620 |
| 1364 | CC1364 | HR CC1364 | 913 |
| 1365 | CC1365 | Quality CC1365 | 115 |
| 1366 | CC1366 | Logistics CC1366 | 339 |
| 1367 | CC1367 | R&D CC1367 | 2824 |
| 1368 | CC1368 | IT CC1368 | 3000 |
| 1369 | CC1369 | Executive CC1369 | 153 |
| 1370 | CC1370 | Executive CC1370 | 79 |
| 1371 | CC1371 | Treasury CC1371 | 2874 |
| 1372 | CC1372 | Operations CC1372 | 3623 |
| 1373 | CC1373 | Engineering CC1373 | 1926 |
| 1374 | CC1374 | Logistics CC1374 | 2633 |
| 1375 | CC1375 | Engineering CC1375 | 341 |
| 1376 | CC1376 | IT CC1376 | 2345 |
| 1377 | CC1377 | Compliance CC1377 | 536 |
| 1378 | CC1378 | Executive CC1378 | 552 |
| 1379 | CC1379 | R&D CC1379 | 3816 |
| 1380 | CC1380 | Compliance CC1380 | 1391 |
| 1381 | CC1381 | IT CC1381 | 2862 |
| 1382 | CC1382 | Marketing CC1382 | 3436 |
| 1383 | CC1383 | Engineering CC1383 | 1804 |
| 1384 | CC1384 | Legal CC1384 | 1689 |
| 1385 | CC1385 | Engineering CC1385 | 958 |
| 1386 | CC1386 | Finance CC1386 | 2935 |
| 1387 | CC1387 | Sales CC1387 | 3116 |
| 1388 | CC1388 | Sales CC1388 | 2635 |
| 1389 | CC1389 | Support CC1389 | 3161 |
| 1390 | CC1390 | Strategy CC1390 | 606 |
| 1391 | CC1391 | Marketing CC1391 | 1543 |
| 1392 | CC1392 | Audit CC1392 | 1902 |
| 1393 | CC1393 | Treasury CC1393 | 1438 |
| 1394 | CC1394 | Executive CC1394 | 1947 |
| 1395 | CC1395 | Analytics CC1395 | 3150 |
| 1396 | CC1396 | Support CC1396 | 1084 |
| 1397 | CC1397 | Operations CC1397 | 42 |
| 1398 | CC1398 | R&D CC1398 | 3245 |
| 1399 | CC1399 | Compliance CC1399 | 2870 |
| 1400 | CC1400 | Strategy CC1400 | 2895 |
| 1401 | CC1401 | Procurement CC1401 | 342 |
| 1402 | CC1402 | Sales CC1402 | 3864 |
| 1403 | CC1403 | Support CC1403 | 3218 |
| 1404 | CC1404 | Risk CC1404 | 2094 |
| 1405 | CC1405 | Finance CC1405 | 576 |
| 1406 | CC1406 | Logistics CC1406 | 1600 |
| 1407 | CC1407 | Engineering CC1407 | 2303 |
| 1408 | CC1408 | Support CC1408 | 503 |
| 1409 | CC1409 | Support CC1409 | 3938 |
| 1410 | CC1410 | R&D CC1410 | 3747 |
| 1411 | CC1411 | Sales CC1411 | 3354 |
| 1412 | CC1412 | Sales CC1412 | 3734 |
| 1413 | CC1413 | Quality CC1413 | 3127 |
| 1414 | CC1414 | R&D CC1414 | 1995 |
| 1415 | CC1415 | Strategy CC1415 | 1658 |
| 1416 | CC1416 | Treasury CC1416 | 3573 |
| 1417 | CC1417 | Marketing CC1417 | 3824 |
| 1418 | CC1418 | R&D CC1418 | 2275 |
| 1419 | CC1419 | Treasury CC1419 | 2155 |
| 1420 | CC1420 | Quality CC1420 | 2022 |
| 1421 | CC1421 | Marketing CC1421 | 3035 |
| 1422 | CC1422 | Quality CC1422 | 1337 |
| 1423 | CC1423 | IT CC1423 | 3684 |
| 1424 | CC1424 | Treasury CC1424 | 1146 |
| 1425 | CC1425 | Treasury CC1425 | 475 |
| 1426 | CC1426 | Legal CC1426 | 658 |
| 1427 | CC1427 | Strategy CC1427 | 995 |
| 1428 | CC1428 | Engineering CC1428 | 1793 |
| 1429 | CC1429 | Operations CC1429 | 930 |
| 1430 | CC1430 | Compliance CC1430 | 931 |
| 1431 | CC1431 | Finance CC1431 | 3637 |
| 1432 | CC1432 | Engineering CC1432 | 1782 |
| 1433 | CC1433 | HR CC1433 | 3150 |
| 1434 | CC1434 | Strategy CC1434 | 392 |
| 1435 | CC1435 | Marketing CC1435 | 1290 |
| 1436 | CC1436 | Quality CC1436 | 2082 |
| 1437 | CC1437 | Audit CC1437 | 2746 |
| 1438 | CC1438 | Procurement CC1438 | 777 |
| 1439 | CC1439 | Analytics CC1439 | 676 |
| 1440 | CC1440 | Logistics CC1440 | 3088 |
| 1441 | CC1441 | Treasury CC1441 | 930 |
| 1442 | CC1442 | Audit CC1442 | 3145 |
| 1443 | CC1443 | Operations CC1443 | 968 |
| 1444 | CC1444 | Legal CC1444 | 1833 |
| 1445 | CC1445 | Risk CC1445 | 3929 |
| 1446 | CC1446 | Compliance CC1446 | 3019 |
| 1447 | CC1447 | Executive CC1447 | 3459 |
| 1448 | CC1448 | Treasury CC1448 | 1454 |
| 1449 | CC1449 | R&D CC1449 | 3643 |
| 1450 | CC1450 | Compliance CC1450 | 1317 |
| 1451 | CC1451 | Audit CC1451 | 2371 |
| 1452 | CC1452 | Procurement CC1452 | 2192 |
| 1453 | CC1453 | Finance CC1453 | 1880 |
| 1454 | CC1454 | IT CC1454 | 3610 |
| 1455 | CC1455 | Risk CC1455 | 2392 |
| 1456 | CC1456 | Risk CC1456 | 879 |
| 1457 | CC1457 | Legal CC1457 | 2819 |
| 1458 | CC1458 | Finance CC1458 | 223 |
| 1459 | CC1459 | Engineering CC1459 | 2123 |
| 1460 | CC1460 | Logistics CC1460 | 547 |
| 1461 | CC1461 | Quality CC1461 | 3012 |
| 1462 | CC1462 | Audit CC1462 | 3006 |
| 1463 | CC1463 | Logistics CC1463 | 2338 |
| 1464 | CC1464 | R&D CC1464 | 2200 |
| 1465 | CC1465 | Logistics CC1465 | 478 |
| 1466 | CC1466 | Legal CC1466 | 2573 |
| 1467 | CC1467 | Quality CC1467 | 186 |
| 1468 | CC1468 | Treasury CC1468 | 278 |
| 1469 | CC1469 | Quality CC1469 | 1058 |
| 1470 | CC1470 | R&D CC1470 | 2224 |
| 1471 | CC1471 | Strategy CC1471 | 547 |
| 1472 | CC1472 | IT CC1472 | 2638 |
| 1473 | CC1473 | Legal CC1473 | 370 |
| 1474 | CC1474 | Analytics CC1474 | 2778 |
| 1475 | CC1475 | Sales CC1475 | 959 |
| 1476 | CC1476 | R&D CC1476 | 1859 |
| 1477 | CC1477 | HR CC1477 | 2692 |
| 1478 | CC1478 | Analytics CC1478 | 2135 |
| 1479 | CC1479 | IT CC1479 | 594 |
| 1480 | CC1480 | Engineering CC1480 | 2645 |
| 1481 | CC1481 | Procurement CC1481 | 3286 |
| 1482 | CC1482 | R&D CC1482 | 1600 |
| 1483 | CC1483 | Quality CC1483 | 737 |
| 1484 | CC1484 | Engineering CC1484 | 2543 |
| 1485 | CC1485 | Analytics CC1485 | 2711 |
| 1486 | CC1486 | Analytics CC1486 | 3845 |
| 1487 | CC1487 | R&D CC1487 | 516 |
| 1488 | CC1488 | IT CC1488 | 360 |
| 1489 | CC1489 | Analytics CC1489 | 1972 |
| 1490 | CC1490 | Marketing CC1490 | 263 |
| 1491 | CC1491 | Logistics CC1491 | 2308 |
| 1492 | CC1492 | Operations CC1492 | 280 |
| 1493 | CC1493 | HR CC1493 | 2549 |
| 1494 | CC1494 | Procurement CC1494 | 1879 |
| 1495 | CC1495 | Compliance CC1495 | 518 |
| 1496 | CC1496 | Analytics CC1496 | 3679 |
| 1497 | CC1497 | Compliance CC1497 | 2169 |
| 1498 | CC1498 | IT CC1498 | 221 |
| 1499 | CC1499 | Support CC1499 | 3962 |
| 1500 | CC1500 | Audit CC1500 | 2947 |
| 1501 | CC1501 | Finance CC1501 | 2061 |
| 1502 | CC1502 | Strategy CC1502 | 296 |
| 1503 | CC1503 | Analytics CC1503 | 2122 |
| 1504 | CC1504 | Procurement CC1504 | 1314 |
| 1505 | CC1505 | Compliance CC1505 | 3991 |
| 1506 | CC1506 | Support CC1506 | 457 |
| 1507 | CC1507 | IT CC1507 | 1889 |
| 1508 | CC1508 | Treasury CC1508 | 3247 |
| 1509 | CC1509 | R&D CC1509 | 576 |
| 1510 | CC1510 | Operations CC1510 | 1555 |
| 1511 | CC1511 | Sales CC1511 | 75 |
| 1512 | CC1512 | Support CC1512 | 3879 |
| 1513 | CC1513 | Procurement CC1513 | 3787 |
| 1514 | CC1514 | Audit CC1514 | 1136 |
| 1515 | CC1515 | Marketing CC1515 | 1125 |
| 1516 | CC1516 | Engineering CC1516 | 1177 |
| 1517 | CC1517 | Legal CC1517 | 998 |
| 1518 | CC1518 | Treasury CC1518 | 1423 |
| 1519 | CC1519 | Marketing CC1519 | 753 |
| 1520 | CC1520 | Operations CC1520 | 61 |
| 1521 | CC1521 | Operations CC1521 | 2961 |
| 1522 | CC1522 | Executive CC1522 | 3266 |
| 1523 | CC1523 | Sales CC1523 | 3385 |
| 1524 | CC1524 | Analytics CC1524 | 1138 |
| 1525 | CC1525 | Risk CC1525 | 1275 |
| 1526 | CC1526 | HR CC1526 | 1463 |
| 1527 | CC1527 | Audit CC1527 | 3315 |
| 1528 | CC1528 | Operations CC1528 | 3273 |
| 1529 | CC1529 | R&D CC1529 | 3382 |
| 1530 | CC1530 | Legal CC1530 | 2932 |
| 1531 | CC1531 | Compliance CC1531 | 3363 |
| 1532 | CC1532 | Finance CC1532 | 2644 |
| 1533 | CC1533 | Quality CC1533 | 3509 |
| 1534 | CC1534 | Risk CC1534 | 3020 |
| 1535 | CC1535 | Finance CC1535 | 204 |
| 1536 | CC1536 | Logistics CC1536 | 1314 |
| 1537 | CC1537 | IT CC1537 | 3573 |
| 1538 | CC1538 | Finance CC1538 | 1048 |
| 1539 | CC1539 | IT CC1539 | 3051 |
| 1540 | CC1540 | Sales CC1540 | 1471 |
| 1541 | CC1541 | Risk CC1541 | 3446 |
| 1542 | CC1542 | Marketing CC1542 | 529 |
| 1543 | CC1543 | Sales CC1543 | 579 |
| 1544 | CC1544 | Finance CC1544 | 3743 |
| 1545 | CC1545 | Treasury CC1545 | 683 |
| 1546 | CC1546 | Legal CC1546 | 3884 |
| 1547 | CC1547 | Risk CC1547 | 2340 |
| 1548 | CC1548 | Procurement CC1548 | 2680 |
| 1549 | CC1549 | Finance CC1549 | 1286 |
| 1550 | CC1550 | Operations CC1550 | 2484 |
| 1551 | CC1551 | Compliance CC1551 | 2441 |
| 1552 | CC1552 | Compliance CC1552 | 3837 |
| 1553 | CC1553 | Strategy CC1553 | 2188 |
| 1554 | CC1554 | Logistics CC1554 | 3197 |
| 1555 | CC1555 | Risk CC1555 | 3976 |
| 1556 | CC1556 | Finance CC1556 | 3602 |
| 1557 | CC1557 | HR CC1557 | 336 |
| 1558 | CC1558 | Finance CC1558 | 2929 |
| 1559 | CC1559 | HR CC1559 | 3142 |
| 1560 | CC1560 | Legal CC1560 | 3309 |
| 1561 | CC1561 | HR CC1561 | 2528 |
| 1562 | CC1562 | Engineering CC1562 | 3402 |
| 1563 | CC1563 | Analytics CC1563 | 1903 |
| 1564 | CC1564 | Executive CC1564 | 1899 |
| 1565 | CC1565 | Treasury CC1565 | 3825 |
| 1566 | CC1566 | Risk CC1566 | 234 |
| 1567 | CC1567 | Engineering CC1567 | 393 |
| 1568 | CC1568 | Legal CC1568 | 1741 |
| 1569 | CC1569 | Compliance CC1569 | 2548 |
| 1570 | CC1570 | Sales CC1570 | 1217 |
| 1571 | CC1571 | HR CC1571 | 391 |
| 1572 | CC1572 | Treasury CC1572 | 395 |
| 1573 | CC1573 | Engineering CC1573 | 511 |
| 1574 | CC1574 | Operations CC1574 | 3798 |
| 1575 | CC1575 | Executive CC1575 | 2809 |
| 1576 | CC1576 | Support CC1576 | 3515 |
| 1577 | CC1577 | Operations CC1577 | 3384 |
| 1578 | CC1578 | Sales CC1578 | 2424 |
| 1579 | CC1579 | Risk CC1579 | 3089 |
| 1580 | CC1580 | Engineering CC1580 | 3106 |
| 1581 | CC1581 | Logistics CC1581 | 385 |
| 1582 | CC1582 | Logistics CC1582 | 1633 |
| 1583 | CC1583 | Treasury CC1583 | 2111 |
| 1584 | CC1584 | Sales CC1584 | 3263 |
| 1585 | CC1585 | HR CC1585 | 45 |
| 1586 | CC1586 | Quality CC1586 | 1295 |
| 1587 | CC1587 | Strategy CC1587 | 1483 |
| 1588 | CC1588 | Quality CC1588 | 3012 |
| 1589 | CC1589 | Treasury CC1589 | 3935 |
| 1590 | CC1590 | Quality CC1590 | 3177 |
| 1591 | CC1591 | Analytics CC1591 | 3823 |
| 1592 | CC1592 | Quality CC1592 | 3814 |
| 1593 | CC1593 | HR CC1593 | 1483 |
| 1594 | CC1594 | Finance CC1594 | 2506 |
| 1595 | CC1595 | Treasury CC1595 | 2550 |
| 1596 | CC1596 | Quality CC1596 | 1692 |
| 1597 | CC1597 | Legal CC1597 | 3160 |
| 1598 | CC1598 | IT CC1598 | 1217 |
| 1599 | CC1599 | Support CC1599 | 3109 |
| 1600 | CC1600 | Operations CC1600 | 3227 |
| 1601 | CC1601 | Audit CC1601 | 3697 |
| 1602 | CC1602 | Quality CC1602 | 192 |
| 1603 | CC1603 | Strategy CC1603 | 973 |
| 1604 | CC1604 | Procurement CC1604 | 448 |
| 1605 | CC1605 | Audit CC1605 | 2856 |
| 1606 | CC1606 | Executive CC1606 | 1484 |
| 1607 | CC1607 | R&D CC1607 | 870 |
| 1608 | CC1608 | Executive CC1608 | 2178 |
| 1609 | CC1609 | Support CC1609 | 2497 |
| 1610 | CC1610 | Audit CC1610 | 1467 |
| 1611 | CC1611 | Sales CC1611 | 2063 |
| 1612 | CC1612 | Operations CC1612 | 1997 |
| 1613 | CC1613 | Engineering CC1613 | 2004 |
| 1614 | CC1614 | Logistics CC1614 | 1976 |
| 1615 | CC1615 | Quality CC1615 | 699 |
| 1616 | CC1616 | Procurement CC1616 | 1793 |
| 1617 | CC1617 | Support CC1617 | 2201 |
| 1618 | CC1618 | Analytics CC1618 | 1876 |
| 1619 | CC1619 | Logistics CC1619 | 241 |
| 1620 | CC1620 | Logistics CC1620 | 2518 |
| 1621 | CC1621 | Logistics CC1621 | 1977 |
| 1622 | CC1622 | Legal CC1622 | 2476 |
| 1623 | CC1623 | Compliance CC1623 | 3393 |
| 1624 | CC1624 | Engineering CC1624 | 1251 |
| 1625 | CC1625 | Executive CC1625 | 1824 |
| 1626 | CC1626 | Engineering CC1626 | 2933 |
| 1627 | CC1627 | Compliance CC1627 | 504 |
| 1628 | CC1628 | Executive CC1628 | 3196 |
| 1629 | CC1629 | Risk CC1629 | 3906 |
| 1630 | CC1630 | IT CC1630 | 2983 |
| 1631 | CC1631 | Risk CC1631 | 306 |
| 1632 | CC1632 | Support CC1632 | 926 |
| 1633 | CC1633 | Support CC1633 | 1950 |
| 1634 | CC1634 | Legal CC1634 | 2173 |
| 1635 | CC1635 | Audit CC1635 | 733 |
| 1636 | CC1636 | Legal CC1636 | 151 |
| 1637 | CC1637 | HR CC1637 | 2370 |
| 1638 | CC1638 | HR CC1638 | 934 |
| 1639 | CC1639 | HR CC1639 | 2652 |
| 1640 | CC1640 | Strategy CC1640 | 471 |
| 1641 | CC1641 | Operations CC1641 | 1790 |
| 1642 | CC1642 | Sales CC1642 | 3526 |
| 1643 | CC1643 | Executive CC1643 | 32 |
| 1644 | CC1644 | Finance CC1644 | 849 |
| 1645 | CC1645 | Sales CC1645 | 3129 |
| 1646 | CC1646 | Compliance CC1646 | 1684 |
| 1647 | CC1647 | Logistics CC1647 | 768 |
| 1648 | CC1648 | Compliance CC1648 | 1778 |
| 1649 | CC1649 | Audit CC1649 | 1441 |
| 1650 | CC1650 | Audit CC1650 | 982 |
| 1651 | CC1651 | Quality CC1651 | 1719 |
| 1652 | CC1652 | Treasury CC1652 | 3740 |
| 1653 | CC1653 | Treasury CC1653 | 1536 |
| 1654 | CC1654 | Audit CC1654 | 859 |
| 1655 | CC1655 | Compliance CC1655 | 2011 |
| 1656 | CC1656 | Quality CC1656 | 1217 |
| 1657 | CC1657 | Audit CC1657 | 339 |
| 1658 | CC1658 | Analytics CC1658 | 1376 |
| 1659 | CC1659 | IT CC1659 | 2884 |
| 1660 | CC1660 | Engineering CC1660 | 3361 |
| 1661 | CC1661 | IT CC1661 | 3356 |
| 1662 | CC1662 | Support CC1662 | 1846 |
| 1663 | CC1663 | Analytics CC1663 | 1822 |
| 1664 | CC1664 | R&D CC1664 | 871 |
| 1665 | CC1665 | Analytics CC1665 | 2074 |
| 1666 | CC1666 | IT CC1666 | 883 |
| 1667 | CC1667 | Operations CC1667 | 450 |
| 1668 | CC1668 | Finance CC1668 | 619 |
| 1669 | CC1669 | Executive CC1669 | 626 |
| 1670 | CC1670 | Quality CC1670 | 2972 |
| 1671 | CC1671 | HR CC1671 | 3724 |
| 1672 | CC1672 | Support CC1672 | 208 |
| 1673 | CC1673 | Risk CC1673 | 853 |
| 1674 | CC1674 | Executive CC1674 | 722 |
| 1675 | CC1675 | Sales CC1675 | 170 |
| 1676 | CC1676 | Analytics CC1676 | 368 |
| 1677 | CC1677 | Audit CC1677 | 3093 |
| 1678 | CC1678 | Compliance CC1678 | 2111 |
| 1679 | CC1679 | IT CC1679 | 2512 |
| 1680 | CC1680 | Sales CC1680 | 2730 |
| 1681 | CC1681 | Legal CC1681 | 603 |
| 1682 | CC1682 | Strategy CC1682 | 441 |
| 1683 | CC1683 | Executive CC1683 | 3320 |
| 1684 | CC1684 | Sales CC1684 | 3277 |
| 1685 | CC1685 | IT CC1685 | 3631 |
| 1686 | CC1686 | Engineering CC1686 | 990 |
| 1687 | CC1687 | HR CC1687 | 2451 |
| 1688 | CC1688 | Risk CC1688 | 3567 |
| 1689 | CC1689 | Procurement CC1689 | 627 |
| 1690 | CC1690 | HR CC1690 | 2660 |
| 1691 | CC1691 | Finance CC1691 | 3022 |
| 1692 | CC1692 | IT CC1692 | 2002 |
| 1693 | CC1693 | Finance CC1693 | 52 |
| 1694 | CC1694 | Finance CC1694 | 2069 |
| 1695 | CC1695 | R&D CC1695 | 1130 |
| 1696 | CC1696 | Analytics CC1696 | 1834 |
| 1697 | CC1697 | Logistics CC1697 | 2383 |
| 1698 | CC1698 | Logistics CC1698 | 2842 |
| 1699 | CC1699 | Engineering CC1699 | 2546 |
| 1700 | CC1700 | Sales CC1700 | 3358 |
| 1701 | CC1701 | Strategy CC1701 | 1649 |
| 1702 | CC1702 | Sales CC1702 | 1946 |
| 1703 | CC1703 | Analytics CC1703 | 1048 |
| 1704 | CC1704 | IT CC1704 | 3367 |
| 1705 | CC1705 | Procurement CC1705 | 1404 |
| 1706 | CC1706 | Risk CC1706 | 3009 |
| 1707 | CC1707 | Quality CC1707 | 2722 |
| 1708 | CC1708 | Executive CC1708 | 930 |
| 1709 | CC1709 | Legal CC1709 | 3583 |
| 1710 | CC1710 | Treasury CC1710 | 1938 |
| 1711 | CC1711 | Operations CC1711 | 1711 |
| 1712 | CC1712 | IT CC1712 | 2298 |
| 1713 | CC1713 | Marketing CC1713 | 591 |
| 1714 | CC1714 | Audit CC1714 | 3466 |
| 1715 | CC1715 | Audit CC1715 | 1504 |
| 1716 | CC1716 | Quality CC1716 | 3971 |
| 1717 | CC1717 | Legal CC1717 | 3597 |
| 1718 | CC1718 | Operations CC1718 | 1363 |
| 1719 | CC1719 | Risk CC1719 | 688 |
| 1720 | CC1720 | Executive CC1720 | 2821 |
| 1721 | CC1721 | Treasury CC1721 | 2299 |
| 1722 | CC1722 | Marketing CC1722 | 3104 |
| 1723 | CC1723 | Executive CC1723 | 520 |
| 1724 | CC1724 | HR CC1724 | 3074 |
| 1725 | CC1725 | HR CC1725 | 1178 |
| 1726 | CC1726 | Strategy CC1726 | 1137 |
| 1727 | CC1727 | Logistics CC1727 | 2042 |
| 1728 | CC1728 | Strategy CC1728 | 1764 |
| 1729 | CC1729 | Quality CC1729 | 22 |
| 1730 | CC1730 | Marketing CC1730 | 2709 |
| 1731 | CC1731 | Engineering CC1731 | 3657 |
| 1732 | CC1732 | Procurement CC1732 | 664 |
| 1733 | CC1733 | IT CC1733 | 3922 |
| 1734 | CC1734 | Sales CC1734 | 3774 |
| 1735 | CC1735 | Quality CC1735 | 2261 |
| 1736 | CC1736 | Audit CC1736 | 548 |
| 1737 | CC1737 | Compliance CC1737 | 3715 |
| 1738 | CC1738 | Legal CC1738 | 2107 |
| 1739 | CC1739 | Audit CC1739 | 89 |
| 1740 | CC1740 | R&D CC1740 | 2930 |
| 1741 | CC1741 | Compliance CC1741 | 1952 |
| 1742 | CC1742 | Treasury CC1742 | 887 |
| 1743 | CC1743 | Risk CC1743 | 1219 |
| 1744 | CC1744 | Procurement CC1744 | 2643 |
| 1745 | CC1745 | Engineering CC1745 | 3036 |
| 1746 | CC1746 | Strategy CC1746 | 1738 |
| 1747 | CC1747 | Audit CC1747 | 1241 |
| 1748 | CC1748 | Analytics CC1748 | 530 |
| 1749 | CC1749 | Strategy CC1749 | 3091 |
| 1750 | CC1750 | Support CC1750 | 2220 |
| 1751 | CC1751 | Procurement CC1751 | 3689 |
| 1752 | CC1752 | Marketing CC1752 | 3178 |
| 1753 | CC1753 | Sales CC1753 | 1192 |
| 1754 | CC1754 | Executive CC1754 | 649 |
| 1755 | CC1755 | Engineering CC1755 | 250 |
| 1756 | CC1756 | Support CC1756 | 1144 |
| 1757 | CC1757 | R&D CC1757 | 1711 |
| 1758 | CC1758 | Procurement CC1758 | 32 |
| 1759 | CC1759 | Logistics CC1759 | 821 |
| 1760 | CC1760 | Risk CC1760 | 1966 |
| 1761 | CC1761 | Quality CC1761 | 3371 |
| 1762 | CC1762 | Procurement CC1762 | 3784 |
| 1763 | CC1763 | HR CC1763 | 1923 |
| 1764 | CC1764 | R&D CC1764 | 1698 |
| 1765 | CC1765 | Audit CC1765 | 2840 |
| 1766 | CC1766 | Analytics CC1766 | 1376 |
| 1767 | CC1767 | Quality CC1767 | 3332 |
| 1768 | CC1768 | Compliance CC1768 | 257 |
| 1769 | CC1769 | Support CC1769 | 2584 |
| 1770 | CC1770 | IT CC1770 | 3034 |
| 1771 | CC1771 | Sales CC1771 | 1083 |
| 1772 | CC1772 | Procurement CC1772 | 245 |
| 1773 | CC1773 | Analytics CC1773 | 3365 |
| 1774 | CC1774 | Sales CC1774 | 904 |
| 1775 | CC1775 | Support CC1775 | 3580 |
| 1776 | CC1776 | Treasury CC1776 | 1670 |
| 1777 | CC1777 | Support CC1777 | 3029 |
| 1778 | CC1778 | Operations CC1778 | 629 |
| 1779 | CC1779 | Support CC1779 | 80 |
| 1780 | CC1780 | Sales CC1780 | 1973 |
| 1781 | CC1781 | Audit CC1781 | 3078 |
| 1782 | CC1782 | Engineering CC1782 | 2201 |
| 1783 | CC1783 | Compliance CC1783 | 3541 |
| 1784 | CC1784 | HR CC1784 | 460 |
| 1785 | CC1785 | Operations CC1785 | 332 |
| 1786 | CC1786 | Executive CC1786 | 612 |
| 1787 | CC1787 | Engineering CC1787 | 2602 |
| 1788 | CC1788 | Risk CC1788 | 1604 |
| 1789 | CC1789 | Legal CC1789 | 3630 |
| 1790 | CC1790 | Finance CC1790 | 1514 |
| 1791 | CC1791 | Procurement CC1791 | 522 |
| 1792 | CC1792 | Logistics CC1792 | 1340 |
| 1793 | CC1793 | Operations CC1793 | 3331 |
| 1794 | CC1794 | HR CC1794 | 3990 |
| 1795 | CC1795 | IT CC1795 | 3122 |
| 1796 | CC1796 | Marketing CC1796 | 1449 |
| 1797 | CC1797 | Operations CC1797 | 2248 |
| 1798 | CC1798 | IT CC1798 | 3571 |
| 1799 | CC1799 | Support CC1799 | 1990 |
| 1800 | CC1800 | Procurement CC1800 | 2653 |
| 1801 | CC1801 | Risk CC1801 | 259 |
| 1802 | CC1802 | R&D CC1802 | 1644 |
| 1803 | CC1803 | Marketing CC1803 | 1518 |
| 1804 | CC1804 | Sales CC1804 | 864 |
| 1805 | CC1805 | Analytics CC1805 | 2140 |
| 1806 | CC1806 | Executive CC1806 | 1608 |
| 1807 | CC1807 | R&D CC1807 | 2549 |
| 1808 | CC1808 | Compliance CC1808 | 1340 |
| 1809 | CC1809 | HR CC1809 | 3514 |
| 1810 | CC1810 | Sales CC1810 | 3622 |
| 1811 | CC1811 | R&D CC1811 | 3245 |
| 1812 | CC1812 | Operations CC1812 | 711 |
| 1813 | CC1813 | Quality CC1813 | 2953 |
| 1814 | CC1814 | Sales CC1814 | 3758 |
| 1815 | CC1815 | HR CC1815 | 449 |
| 1816 | CC1816 | Risk CC1816 | 1561 |
| 1817 | CC1817 | Quality CC1817 | 3550 |
| 1818 | CC1818 | R&D CC1818 | 3126 |
| 1819 | CC1819 | Executive CC1819 | 3595 |
| 1820 | CC1820 | Audit CC1820 | 3634 |
| 1821 | CC1821 | Analytics CC1821 | 3097 |
| 1822 | CC1822 | Support CC1822 | 299 |
| 1823 | CC1823 | HR CC1823 | 802 |
| 1824 | CC1824 | Finance CC1824 | 1687 |
| 1825 | CC1825 | Treasury CC1825 | 106 |
| 1826 | CC1826 | Risk CC1826 | 2880 |
| 1827 | CC1827 | Quality CC1827 | 1198 |
| 1828 | CC1828 | Logistics CC1828 | 1863 |
| 1829 | CC1829 | Compliance CC1829 | 3685 |
| 1830 | CC1830 | Executive CC1830 | 2912 |
| 1831 | CC1831 | Executive CC1831 | 1840 |
| 1832 | CC1832 | Support CC1832 | 2325 |
| 1833 | CC1833 | Legal CC1833 | 1116 |
| 1834 | CC1834 | Executive CC1834 | 2673 |
| 1835 | CC1835 | HR CC1835 | 2584 |
| 1836 | CC1836 | Marketing CC1836 | 63 |
| 1837 | CC1837 | Compliance CC1837 | 725 |
| 1838 | CC1838 | Legal CC1838 | 1932 |
| 1839 | CC1839 | Marketing CC1839 | 1679 |
| 1840 | CC1840 | Risk CC1840 | 3357 |
| 1841 | CC1841 | Strategy CC1841 | 3800 |
| 1842 | CC1842 | Quality CC1842 | 3895 |
| 1843 | CC1843 | Logistics CC1843 | 3853 |
| 1844 | CC1844 | Operations CC1844 | 3939 |
| 1845 | CC1845 | Finance CC1845 | 1424 |
| 1846 | CC1846 | Engineering CC1846 | 304 |
| 1847 | CC1847 | HR CC1847 | 3107 |
| 1848 | CC1848 | Operations CC1848 | 231 |
| 1849 | CC1849 | IT CC1849 | 3633 |
| 1850 | CC1850 | Engineering CC1850 | 488 |
| 1851 | CC1851 | Logistics CC1851 | 3448 |
| 1852 | CC1852 | Executive CC1852 | 186 |
| 1853 | CC1853 | IT CC1853 | 442 |
| 1854 | CC1854 | Sales CC1854 | 3137 |
| 1855 | CC1855 | Audit CC1855 | 3120 |
| 1856 | CC1856 | Strategy CC1856 | 1237 |
| 1857 | CC1857 | Compliance CC1857 | 2581 |
| 1858 | CC1858 | Support CC1858 | 2633 |
| 1859 | CC1859 | Engineering CC1859 | 3044 |
| 1860 | CC1860 | Operations CC1860 | 2187 |
| 1861 | CC1861 | IT CC1861 | 1352 |
| 1862 | CC1862 | Audit CC1862 | 2799 |
| 1863 | CC1863 | HR CC1863 | 3642 |
| 1864 | CC1864 | Marketing CC1864 | 437 |
| 1865 | CC1865 | Strategy CC1865 | 701 |
| 1866 | CC1866 | Operations CC1866 | 2573 |
| 1867 | CC1867 | Compliance CC1867 | 3416 |
| 1868 | CC1868 | Quality CC1868 | 882 |
| 1869 | CC1869 | Executive CC1869 | 1611 |
| 1870 | CC1870 | Legal CC1870 | 1188 |
| 1871 | CC1871 | Procurement CC1871 | 2259 |
| 1872 | CC1872 | Sales CC1872 | 1420 |
| 1873 | CC1873 | Compliance CC1873 | 320 |
| 1874 | CC1874 | R&D CC1874 | 1990 |
| 1875 | CC1875 | Quality CC1875 | 1674 |
| 1876 | CC1876 | Procurement CC1876 | 963 |
| 1877 | CC1877 | Engineering CC1877 | 1003 |
| 1878 | CC1878 | Risk CC1878 | 1537 |
| 1879 | CC1879 | Procurement CC1879 | 2901 |
| 1880 | CC1880 | R&D CC1880 | 2480 |
| 1881 | CC1881 | IT CC1881 | 3020 |
| 1882 | CC1882 | Compliance CC1882 | 680 |
| 1883 | CC1883 | Operations CC1883 | 2045 |
| 1884 | CC1884 | Finance CC1884 | 1051 |
| 1885 | CC1885 | Compliance CC1885 | 941 |
| 1886 | CC1886 | Procurement CC1886 | 1298 |
| 1887 | CC1887 | Sales CC1887 | 271 |
| 1888 | CC1888 | Operations CC1888 | 516 |
| 1889 | CC1889 | Marketing CC1889 | 1307 |
| 1890 | CC1890 | Legal CC1890 | 1088 |
| 1891 | CC1891 | HR CC1891 | 3683 |
| 1892 | CC1892 | Compliance CC1892 | 3237 |
| 1893 | CC1893 | Legal CC1893 | 960 |
| 1894 | CC1894 | R&D CC1894 | 3217 |
| 1895 | CC1895 | Compliance CC1895 | 3182 |
| 1896 | CC1896 | Risk CC1896 | 633 |
| 1897 | CC1897 | Compliance CC1897 | 1114 |
| 1898 | CC1898 | HR CC1898 | 3940 |
| 1899 | CC1899 | Audit CC1899 | 1509 |
| 1900 | CC1900 | Operations CC1900 | 2156 |
| 1901 | CC1901 | Risk CC1901 | 1271 |
| 1902 | CC1902 | Finance CC1902 | 1514 |
| 1903 | CC1903 | Legal CC1903 | 1968 |
| 1904 | CC1904 | Executive CC1904 | 469 |
| 1905 | CC1905 | Quality CC1905 | 3800 |
| 1906 | CC1906 | Legal CC1906 | 3973 |
| 1907 | CC1907 | Operations CC1907 | 375 |
| 1908 | CC1908 | R&D CC1908 | 2832 |
| 1909 | CC1909 | Support CC1909 | 2437 |
| 1910 | CC1910 | R&D CC1910 | 1327 |
| 1911 | CC1911 | IT CC1911 | 2219 |
| 1912 | CC1912 | Marketing CC1912 | 3395 |
| 1913 | CC1913 | Compliance CC1913 | 645 |
| 1914 | CC1914 | Procurement CC1914 | 3113 |
| 1915 | CC1915 | Executive CC1915 | 2936 |
| 1916 | CC1916 | Executive CC1916 | 2827 |
| 1917 | CC1917 | HR CC1917 | 3506 |
| 1918 | CC1918 | Strategy CC1918 | 2563 |
| 1919 | CC1919 | Procurement CC1919 | 3714 |
| 1920 | CC1920 | Treasury CC1920 | 3019 |
| 1921 | CC1921 | Legal CC1921 | 1442 |
| 1922 | CC1922 | Procurement CC1922 | 1483 |
| 1923 | CC1923 | Sales CC1923 | 687 |
| 1924 | CC1924 | Sales CC1924 | 2274 |
| 1925 | CC1925 | R&D CC1925 | 3090 |
| 1926 | CC1926 | R&D CC1926 | 3447 |
| 1927 | CC1927 | HR CC1927 | 1026 |
| 1928 | CC1928 | Treasury CC1928 | 625 |
| 1929 | CC1929 | Treasury CC1929 | 1617 |
| 1930 | CC1930 | IT CC1930 | 2798 |
| 1931 | CC1931 | Analytics CC1931 | 2327 |
| 1932 | CC1932 | Finance CC1932 | 3806 |
| 1933 | CC1933 | Support CC1933 | 1215 |
| 1934 | CC1934 | Sales CC1934 | 944 |
| 1935 | CC1935 | Logistics CC1935 | 634 |
| 1936 | CC1936 | Finance CC1936 | 85 |
| 1937 | CC1937 | Operations CC1937 | 227 |
| 1938 | CC1938 | Legal CC1938 | 2121 |
| 1939 | CC1939 | Logistics CC1939 | 2592 |
| 1940 | CC1940 | Engineering CC1940 | 298 |
| 1941 | CC1941 | Logistics CC1941 | 2720 |
| 1942 | CC1942 | Treasury CC1942 | 3783 |
| 1943 | CC1943 | Legal CC1943 | 1967 |
| 1944 | CC1944 | Risk CC1944 | 2518 |
| 1945 | CC1945 | Legal CC1945 | 1279 |
| 1946 | CC1946 | Operations CC1946 | 2762 |
| 1947 | CC1947 | Marketing CC1947 | 3858 |
| 1948 | CC1948 | R&D CC1948 | 1017 |
| 1949 | CC1949 | Quality CC1949 | 2214 |
| 1950 | CC1950 | Procurement CC1950 | 2631 |
| 1951 | CC1951 | Operations CC1951 | 2757 |
| 1952 | CC1952 | Treasury CC1952 | 1187 |
| 1953 | CC1953 | Treasury CC1953 | 3940 |
| 1954 | CC1954 | Treasury CC1954 | 3649 |
| 1955 | CC1955 | Marketing CC1955 | 2921 |
| 1956 | CC1956 | Strategy CC1956 | 1999 |
| 1957 | CC1957 | R&D CC1957 | 2883 |
| 1958 | CC1958 | R&D CC1958 | 2852 |
| 1959 | CC1959 | Executive CC1959 | 3334 |
| 1960 | CC1960 | Marketing CC1960 | 1427 |
| 1961 | CC1961 | Procurement CC1961 | 2683 |
| 1962 | CC1962 | Legal CC1962 | 995 |
| 1963 | CC1963 | Audit CC1963 | 1966 |
| 1964 | CC1964 | Support CC1964 | 2743 |
| 1965 | CC1965 | Analytics CC1965 | 3402 |
| 1966 | CC1966 | Audit CC1966 | 2319 |
| 1967 | CC1967 | Strategy CC1967 | 3996 |
| 1968 | CC1968 | Compliance CC1968 | 615 |
| 1969 | CC1969 | Audit CC1969 | 2903 |
| 1970 | CC1970 | Quality CC1970 | 580 |
| 1971 | CC1971 | IT CC1971 | 1907 |
| 1972 | CC1972 | Executive CC1972 | 3431 |
| 1973 | CC1973 | Risk CC1973 | 30 |
| 1974 | CC1974 | Marketing CC1974 | 649 |
| 1975 | CC1975 | Analytics CC1975 | 3921 |
| 1976 | CC1976 | HR CC1976 | 3568 |
| 1977 | CC1977 | Legal CC1977 | 1535 |
| 1978 | CC1978 | R&D CC1978 | 3488 |
| 1979 | CC1979 | Treasury CC1979 | 3746 |
| 1980 | CC1980 | Marketing CC1980 | 3558 |
| 1981 | CC1981 | Strategy CC1981 | 2336 |
| 1982 | CC1982 | Finance CC1982 | 2731 |
| 1983 | CC1983 | Finance CC1983 | 567 |
| 1984 | CC1984 | Sales CC1984 | 3824 |
| 1985 | CC1985 | Marketing CC1985 | 1926 |
| 1986 | CC1986 | Marketing CC1986 | 1784 |
| 1987 | CC1987 | Analytics CC1987 | 3065 |
| 1988 | CC1988 | Engineering CC1988 | 962 |
| 1989 | CC1989 | Procurement CC1989 | 1784 |
| 1990 | CC1990 | HR CC1990 | 361 |
| 1991 | CC1991 | Support CC1991 | 1315 |
| 1992 | CC1992 | Audit CC1992 | 2570 |
| 1993 | CC1993 | R&D CC1993 | 1814 |
| 1994 | CC1994 | Treasury CC1994 | 1876 |
| 1995 | CC1995 | Strategy CC1995 | 3083 |
| 1996 | CC1996 | HR CC1996 | 822 |
| 1997 | CC1997 | Legal CC1997 | 2137 |
| 1998 | CC1998 | Executive CC1998 | 419 |
| 1999 | CC1999 | Executive CC1999 | 3460 |
| 2000 | CC2000 | HR CC2000 | 3554 |
| 2001 | CC2001 | Compliance CC2001 | 1161 |
| 2002 | CC2002 | Executive CC2002 | 209 |
| 2003 | CC2003 | Procurement CC2003 | 2646 |
| 2004 | CC2004 | IT CC2004 | 1195 |
| 2005 | CC2005 | Support CC2005 | 2432 |
| 2006 | CC2006 | Analytics CC2006 | 1895 |
| 2007 | CC2007 | Analytics CC2007 | 2727 |
| 2008 | CC2008 | Logistics CC2008 | 758 |
| 2009 | CC2009 | Compliance CC2009 | 3790 |
| 2010 | CC2010 | Legal CC2010 | 2728 |
| 2011 | CC2011 | HR CC2011 | 3712 |
| 2012 | CC2012 | Engineering CC2012 | 661 |
| 2013 | CC2013 | Support CC2013 | 645 |
| 2014 | CC2014 | Finance CC2014 | 1421 |
| 2015 | CC2015 | Marketing CC2015 | 513 |
| 2016 | CC2016 | Compliance CC2016 | 3792 |
| 2017 | CC2017 | R&D CC2017 | 1892 |
| 2018 | CC2018 | Procurement CC2018 | 364 |
| 2019 | CC2019 | Procurement CC2019 | 728 |
| 2020 | CC2020 | Risk CC2020 | 2601 |
| 2021 | CC2021 | Sales CC2021 | 1108 |
| 2022 | CC2022 | Procurement CC2022 | 1187 |
| 2023 | CC2023 | IT CC2023 | 3511 |
| 2024 | CC2024 | Engineering CC2024 | 2438 |
| 2025 | CC2025 | Risk CC2025 | 2592 |
| 2026 | CC2026 | Procurement CC2026 | 1677 |
| 2027 | CC2027 | Strategy CC2027 | 378 |
| 2028 | CC2028 | Treasury CC2028 | 1836 |
| 2029 | CC2029 | Strategy CC2029 | 1291 |
| 2030 | CC2030 | Treasury CC2030 | 2172 |
| 2031 | CC2031 | Engineering CC2031 | 1134 |
| 2032 | CC2032 | Logistics CC2032 | 2626 |
| 2033 | CC2033 | Treasury CC2033 | 1763 |
| 2034 | CC2034 | Audit CC2034 | 211 |
| 2035 | CC2035 | Marketing CC2035 | 52 |
| 2036 | CC2036 | Procurement CC2036 | 330 |
| 2037 | CC2037 | Engineering CC2037 | 3965 |
| 2038 | CC2038 | R&D CC2038 | 816 |
| 2039 | CC2039 | Strategy CC2039 | 574 |
| 2040 | CC2040 | Sales CC2040 | 493 |
| 2041 | CC2041 | HR CC2041 | 2992 |
| 2042 | CC2042 | Strategy CC2042 | 3947 |
| 2043 | CC2043 | HR CC2043 | 3376 |
| 2044 | CC2044 | Finance CC2044 | 423 |
| 2045 | CC2045 | Quality CC2045 | 3869 |
| 2046 | CC2046 | Sales CC2046 | 2239 |
| 2047 | CC2047 | R&D CC2047 | 3239 |
| 2048 | CC2048 | IT CC2048 | 2907 |
| 2049 | CC2049 | Finance CC2049 | 1864 |
| 2050 | CC2050 | IT CC2050 | 1101 |
| 2051 | CC2051 | Analytics CC2051 | 2624 |
| 2052 | CC2052 | R&D CC2052 | 480 |
| 2053 | CC2053 | Risk CC2053 | 804 |
| 2054 | CC2054 | Operations CC2054 | 2349 |
| 2055 | CC2055 | Finance CC2055 | 234 |
| 2056 | CC2056 | Operations CC2056 | 745 |
| 2057 | CC2057 | R&D CC2057 | 1814 |
| 2058 | CC2058 | Support CC2058 | 3635 |
| 2059 | CC2059 | Finance CC2059 | 935 |
| 2060 | CC2060 | Treasury CC2060 | 1163 |
| 2061 | CC2061 | HR CC2061 | 3437 |
| 2062 | CC2062 | Strategy CC2062 | 2680 |
| 2063 | CC2063 | Support CC2063 | 3408 |
| 2064 | CC2064 | Treasury CC2064 | 190 |
| 2065 | CC2065 | HR CC2065 | 1852 |
| 2066 | CC2066 | Executive CC2066 | 2037 |
| 2067 | CC2067 | Procurement CC2067 | 1589 |
| 2068 | CC2068 | Legal CC2068 | 3558 |
| 2069 | CC2069 | Legal CC2069 | 1053 |
| 2070 | CC2070 | Support CC2070 | 3094 |
| 2071 | CC2071 | Engineering CC2071 | 68 |
| 2072 | CC2072 | Operations CC2072 | 506 |
| 2073 | CC2073 | Legal CC2073 | 1984 |
| 2074 | CC2074 | Logistics CC2074 | 2898 |
| 2075 | CC2075 | Treasury CC2075 | 3137 |
| 2076 | CC2076 | Marketing CC2076 | 2968 |
| 2077 | CC2077 | IT CC2077 | 3388 |
| 2078 | CC2078 | Executive CC2078 | 2433 |
| 2079 | CC2079 | Logistics CC2079 | 3270 |
| 2080 | CC2080 | Logistics CC2080 | 3487 |
| 2081 | CC2081 | Risk CC2081 | 1279 |
| 2082 | CC2082 | Operations CC2082 | 2249 |
| 2083 | CC2083 | Marketing CC2083 | 2130 |
| 2084 | CC2084 | Audit CC2084 | 2192 |
| 2085 | CC2085 | Executive CC2085 | 1081 |
| 2086 | CC2086 | Treasury CC2086 | 3866 |
| 2087 | CC2087 | Engineering CC2087 | 2689 |
| 2088 | CC2088 | R&D CC2088 | 434 |
| 2089 | CC2089 | IT CC2089 | 332 |
| 2090 | CC2090 | IT CC2090 | 2227 |
| 2091 | CC2091 | Procurement CC2091 | 351 |
| 2092 | CC2092 | Engineering CC2092 | 3807 |
| 2093 | CC2093 | Logistics CC2093 | 2061 |
| 2094 | CC2094 | HR CC2094 | 68 |
| 2095 | CC2095 | Logistics CC2095 | 3995 |
| 2096 | CC2096 | IT CC2096 | 1814 |
| 2097 | CC2097 | Finance CC2097 | 719 |
| 2098 | CC2098 | Procurement CC2098 | 3122 |
| 2099 | CC2099 | Quality CC2099 | 1311 |
| 2100 | CC2100 | Treasury CC2100 | 652 |
| 2101 | CC2101 | Audit CC2101 | 1253 |
| 2102 | CC2102 | Support CC2102 | 1794 |
| 2103 | CC2103 | Marketing CC2103 | 451 |
| 2104 | CC2104 | Sales CC2104 | 3251 |
| 2105 | CC2105 | Engineering CC2105 | 699 |
| 2106 | CC2106 | HR CC2106 | 129 |
| 2107 | CC2107 | Compliance CC2107 | 1355 |
| 2108 | CC2108 | Strategy CC2108 | 2053 |
| 2109 | CC2109 | Compliance CC2109 | 1746 |
| 2110 | CC2110 | Finance CC2110 | 3571 |
| 2111 | CC2111 | Operations CC2111 | 3570 |
| 2112 | CC2112 | IT CC2112 | 1967 |
| 2113 | CC2113 | Logistics CC2113 | 2323 |
| 2114 | CC2114 | Quality CC2114 | 2824 |
| 2115 | CC2115 | Quality CC2115 | 1925 |
| 2116 | CC2116 | Logistics CC2116 | 2320 |
| 2117 | CC2117 | Analytics CC2117 | 185 |
| 2118 | CC2118 | IT CC2118 | 3721 |
| 2119 | CC2119 | Executive CC2119 | 2063 |
| 2120 | CC2120 | Finance CC2120 | 1831 |
| 2121 | CC2121 | Finance CC2121 | 3790 |
| 2122 | CC2122 | Strategy CC2122 | 1931 |
| 2123 | CC2123 | Sales CC2123 | 2893 |
| 2124 | CC2124 | Compliance CC2124 | 3513 |
| 2125 | CC2125 | Compliance CC2125 | 3933 |
| 2126 | CC2126 | R&D CC2126 | 3741 |
| 2127 | CC2127 | Marketing CC2127 | 2628 |
| 2128 | CC2128 | Audit CC2128 | 3427 |
| 2129 | CC2129 | Risk CC2129 | 2757 |
| 2130 | CC2130 | Finance CC2130 | 2975 |
| 2131 | CC2131 | Sales CC2131 | 3460 |
| 2132 | CC2132 | Strategy CC2132 | 1888 |
| 2133 | CC2133 | HR CC2133 | 3084 |
| 2134 | CC2134 | Support CC2134 | 452 |
| 2135 | CC2135 | Strategy CC2135 | 3203 |
| 2136 | CC2136 | R&D CC2136 | 2361 |
| 2137 | CC2137 | Sales CC2137 | 1202 |
| 2138 | CC2138 | R&D CC2138 | 250 |
| 2139 | CC2139 | Logistics CC2139 | 2392 |
| 2140 | CC2140 | Quality CC2140 | 1764 |
| 2141 | CC2141 | Support CC2141 | 1210 |
| 2142 | CC2142 | R&D CC2142 | 3785 |
| 2143 | CC2143 | Procurement CC2143 | 359 |
| 2144 | CC2144 | Audit CC2144 | 149 |
| 2145 | CC2145 | Marketing CC2145 | 3708 |
| 2146 | CC2146 | IT CC2146 | 2404 |
| 2147 | CC2147 | R&D CC2147 | 1973 |
| 2148 | CC2148 | Finance CC2148 | 1926 |
| 2149 | CC2149 | Marketing CC2149 | 1604 |
| 2150 | CC2150 | Legal CC2150 | 3671 |
| 2151 | CC2151 | Logistics CC2151 | 1293 |
| 2152 | CC2152 | Support CC2152 | 2087 |
| 2153 | CC2153 | Procurement CC2153 | 3259 |
| 2154 | CC2154 | Executive CC2154 | 2171 |
| 2155 | CC2155 | Marketing CC2155 | 945 |
| 2156 | CC2156 | Audit CC2156 | 1220 |
| 2157 | CC2157 | Quality CC2157 | 2969 |
| 2158 | CC2158 | Treasury CC2158 | 3670 |
| 2159 | CC2159 | HR CC2159 | 2967 |
| 2160 | CC2160 | Legal CC2160 | 3070 |
| 2161 | CC2161 | Audit CC2161 | 3955 |
| 2162 | CC2162 | Operations CC2162 | 663 |
| 2163 | CC2163 | Support CC2163 | 2294 |
| 2164 | CC2164 | Analytics CC2164 | 1185 |
| 2165 | CC2165 | Operations CC2165 | 2577 |
| 2166 | CC2166 | IT CC2166 | 2489 |
| 2167 | CC2167 | Treasury CC2167 | 3630 |
| 2168 | CC2168 | Treasury CC2168 | 3339 |
| 2169 | CC2169 | Compliance CC2169 | 1485 |
| 2170 | CC2170 | Compliance CC2170 | 504 |
| 2171 | CC2171 | Analytics CC2171 | 1609 |
| 2172 | CC2172 | Executive CC2172 | 604 |
| 2173 | CC2173 | Sales CC2173 | 404 |
| 2174 | CC2174 | HR CC2174 | 3235 |
| 2175 | CC2175 | Procurement CC2175 | 2975 |
| 2176 | CC2176 | IT CC2176 | 2267 |
| 2177 | CC2177 | Support CC2177 | 2573 |
| 2178 | CC2178 | Strategy CC2178 | 2021 |
| 2179 | CC2179 | Treasury CC2179 | 2107 |
| 2180 | CC2180 | Risk CC2180 | 2978 |
| 2181 | CC2181 | HR CC2181 | 2280 |
| 2182 | CC2182 | Treasury CC2182 | 2275 |
| 2183 | CC2183 | Compliance CC2183 | 1935 |
| 2184 | CC2184 | Support CC2184 | 3499 |
| 2185 | CC2185 | Treasury CC2185 | 2536 |
| 2186 | CC2186 | Analytics CC2186 | 1843 |
| 2187 | CC2187 | Strategy CC2187 | 3492 |
| 2188 | CC2188 | Engineering CC2188 | 2073 |
| 2189 | CC2189 | Sales CC2189 | 1515 |
| 2190 | CC2190 | Sales CC2190 | 1709 |
| 2191 | CC2191 | Procurement CC2191 | 3937 |
| 2192 | CC2192 | Treasury CC2192 | 3642 |
| 2193 | CC2193 | Finance CC2193 | 319 |
| 2194 | CC2194 | HR CC2194 | 12 |
| 2195 | CC2195 | R&D CC2195 | 338 |
| 2196 | CC2196 | Risk CC2196 | 1930 |
| 2197 | CC2197 | HR CC2197 | 14 |
| 2198 | CC2198 | Finance CC2198 | 141 |
| 2199 | CC2199 | Quality CC2199 | 1179 |
| 2200 | CC2200 | Logistics CC2200 | 1159 |
| 2201 | CC2201 | Sales CC2201 | 1485 |
| 2202 | CC2202 | Marketing CC2202 | 2195 |
| 2203 | CC2203 | IT CC2203 | 2603 |
| 2204 | CC2204 | HR CC2204 | 1301 |
| 2205 | CC2205 | Treasury CC2205 | 3524 |
| 2206 | CC2206 | Executive CC2206 | 2214 |
| 2207 | CC2207 | Treasury CC2207 | 764 |
| 2208 | CC2208 | HR CC2208 | 2293 |
| 2209 | CC2209 | Marketing CC2209 | 206 |
| 2210 | CC2210 | Engineering CC2210 | 2067 |
| 2211 | CC2211 | Operations CC2211 | 2501 |
| 2212 | CC2212 | Strategy CC2212 | 3963 |
| 2213 | CC2213 | Marketing CC2213 | 1314 |
| 2214 | CC2214 | Treasury CC2214 | 3960 |
| 2215 | CC2215 | Operations CC2215 | 3194 |
| 2216 | CC2216 | Executive CC2216 | 3767 |
| 2217 | CC2217 | R&D CC2217 | 597 |
| 2218 | CC2218 | R&D CC2218 | 1780 |
| 2219 | CC2219 | Executive CC2219 | 1884 |
| 2220 | CC2220 | Strategy CC2220 | 2309 |
| 2221 | CC2221 | Marketing CC2221 | 2160 |
| 2222 | CC2222 | Support CC2222 | 1907 |
| 2223 | CC2223 | Procurement CC2223 | 2820 |
| 2224 | CC2224 | Quality CC2224 | 1179 |
| 2225 | CC2225 | Executive CC2225 | 1923 |
| 2226 | CC2226 | Operations CC2226 | 495 |
| 2227 | CC2227 | Marketing CC2227 | 3573 |
| 2228 | CC2228 | Executive CC2228 | 654 |
| 2229 | CC2229 | Support CC2229 | 3951 |
| 2230 | CC2230 | Logistics CC2230 | 1978 |
| 2231 | CC2231 | Compliance CC2231 | 1607 |
| 2232 | CC2232 | HR CC2232 | 1579 |
| 2233 | CC2233 | Engineering CC2233 | 2483 |
| 2234 | CC2234 | Audit CC2234 | 3677 |
| 2235 | CC2235 | Compliance CC2235 | 1759 |
| 2236 | CC2236 | Logistics CC2236 | 2637 |
| 2237 | CC2237 | Marketing CC2237 | 932 |
| 2238 | CC2238 | Sales CC2238 | 3557 |
| 2239 | CC2239 | Sales CC2239 | 303 |
| 2240 | CC2240 | HR CC2240 | 169 |
| 2241 | CC2241 | R&D CC2241 | 1153 |
| 2242 | CC2242 | Logistics CC2242 | 2488 |
| 2243 | CC2243 | Risk CC2243 | 3305 |
| 2244 | CC2244 | Analytics CC2244 | 2159 |
| 2245 | CC2245 | Risk CC2245 | 3741 |
| 2246 | CC2246 | Procurement CC2246 | 480 |
| 2247 | CC2247 | Treasury CC2247 | 3256 |
| 2248 | CC2248 | Risk CC2248 | 1219 |
| 2249 | CC2249 | HR CC2249 | 3897 |
| 2250 | CC2250 | IT CC2250 | 2013 |
| 2251 | CC2251 | Analytics CC2251 | 492 |
| 2252 | CC2252 | R&D CC2252 | 2105 |
| 2253 | CC2253 | Quality CC2253 | 2788 |
| 2254 | CC2254 | Finance CC2254 | 3743 |
| 2255 | CC2255 | Finance CC2255 | 2459 |
| 2256 | CC2256 | Analytics CC2256 | 458 |
| 2257 | CC2257 | Risk CC2257 | 1443 |
| 2258 | CC2258 | Quality CC2258 | 3030 |
| 2259 | CC2259 | Procurement CC2259 | 2019 |
| 2260 | CC2260 | Treasury CC2260 | 3981 |
| 2261 | CC2261 | Engineering CC2261 | 1766 |
| 2262 | CC2262 | IT CC2262 | 265 |
| 2263 | CC2263 | Risk CC2263 | 120 |
| 2264 | CC2264 | Operations CC2264 | 1044 |
| 2265 | CC2265 | Risk CC2265 | 1962 |
| 2266 | CC2266 | Legal CC2266 | 233 |
| 2267 | CC2267 | Quality CC2267 | 2375 |
| 2268 | CC2268 | IT CC2268 | 2946 |
| 2269 | CC2269 | Procurement CC2269 | 2903 |
| 2270 | CC2270 | Logistics CC2270 | 292 |
| 2271 | CC2271 | Quality CC2271 | 169 |
| 2272 | CC2272 | Legal CC2272 | 2844 |
| 2273 | CC2273 | Support CC2273 | 2564 |
| 2274 | CC2274 | Procurement CC2274 | 1967 |
| 2275 | CC2275 | HR CC2275 | 3160 |
| 2276 | CC2276 | Logistics CC2276 | 625 |
| 2277 | CC2277 | Logistics CC2277 | 3076 |
| 2278 | CC2278 | Strategy CC2278 | 2779 |
| 2279 | CC2279 | Engineering CC2279 | 1082 |
| 2280 | CC2280 | Logistics CC2280 | 1780 |
| 2281 | CC2281 | Analytics CC2281 | 2471 |
| 2282 | CC2282 | Compliance CC2282 | 944 |
| 2283 | CC2283 | Engineering CC2283 | 1331 |
| 2284 | CC2284 | R&D CC2284 | 649 |
| 2285 | CC2285 | Audit CC2285 | 378 |
| 2286 | CC2286 | Compliance CC2286 | 91 |
| 2287 | CC2287 | Analytics CC2287 | 1338 |
| 2288 | CC2288 | Legal CC2288 | 1482 |
| 2289 | CC2289 | Compliance CC2289 | 2941 |
| 2290 | CC2290 | Procurement CC2290 | 2932 |
| 2291 | CC2291 | Legal CC2291 | 860 |
| 2292 | CC2292 | Support CC2292 | 447 |
| 2293 | CC2293 | Support CC2293 | 3130 |
| 2294 | CC2294 | Audit CC2294 | 1618 |
| 2295 | CC2295 | Executive CC2295 | 927 |
| 2296 | CC2296 | Marketing CC2296 | 916 |
| 2297 | CC2297 | Support CC2297 | 1740 |
| 2298 | CC2298 | Operations CC2298 | 608 |
| 2299 | CC2299 | Executive CC2299 | 2297 |
| 2300 | CC2300 | R&D CC2300 | 2205 |
| 2301 | CC2301 | HR CC2301 | 2973 |
| 2302 | CC2302 | Analytics CC2302 | 753 |
| 2303 | CC2303 | Procurement CC2303 | 938 |
| 2304 | CC2304 | Compliance CC2304 | 1136 |
| 2305 | CC2305 | R&D CC2305 | 2388 |
| 2306 | CC2306 | Logistics CC2306 | 2887 |
| 2307 | CC2307 | Legal CC2307 | 2893 |
| 2308 | CC2308 | Risk CC2308 | 2876 |
| 2309 | CC2309 | IT CC2309 | 827 |
| 2310 | CC2310 | Analytics CC2310 | 3534 |
| 2311 | CC2311 | Executive CC2311 | 525 |
| 2312 | CC2312 | Analytics CC2312 | 2166 |
| 2313 | CC2313 | Procurement CC2313 | 2138 |
| 2314 | CC2314 | Sales CC2314 | 707 |
| 2315 | CC2315 | Sales CC2315 | 1654 |
| 2316 | CC2316 | Strategy CC2316 | 81 |
| 2317 | CC2317 | Engineering CC2317 | 3031 |
| 2318 | CC2318 | Logistics CC2318 | 227 |
| 2319 | CC2319 | Logistics CC2319 | 3683 |
| 2320 | CC2320 | Analytics CC2320 | 2266 |
| 2321 | CC2321 | Legal CC2321 | 813 |
| 2322 | CC2322 | Legal CC2322 | 3065 |
| 2323 | CC2323 | Engineering CC2323 | 3145 |
| 2324 | CC2324 | Sales CC2324 | 3426 |
| 2325 | CC2325 | Support CC2325 | 49 |
| 2326 | CC2326 | Analytics CC2326 | 3385 |
| 2327 | CC2327 | Logistics CC2327 | 3356 |
| 2328 | CC2328 | IT CC2328 | 2597 |
| 2329 | CC2329 | Marketing CC2329 | 3127 |
| 2330 | CC2330 | Logistics CC2330 | 2342 |
| 2331 | CC2331 | Executive CC2331 | 1265 |
| 2332 | CC2332 | HR CC2332 | 2379 |
| 2333 | CC2333 | Treasury CC2333 | 1138 |
| 2334 | CC2334 | Audit CC2334 | 595 |
| 2335 | CC2335 | IT CC2335 | 1514 |
| 2336 | CC2336 | HR CC2336 | 625 |
| 2337 | CC2337 | Audit CC2337 | 2348 |
| 2338 | CC2338 | Procurement CC2338 | 381 |
| 2339 | CC2339 | Logistics CC2339 | 291 |
| 2340 | CC2340 | Legal CC2340 | 3072 |
| 2341 | CC2341 | Support CC2341 | 3269 |
| 2342 | CC2342 | Analytics CC2342 | 2684 |
| 2343 | CC2343 | Finance CC2343 | 3261 |
| 2344 | CC2344 | Treasury CC2344 | 2129 |
| 2345 | CC2345 | Finance CC2345 | 3734 |
| 2346 | CC2346 | R&D CC2346 | 1499 |
| 2347 | CC2347 | Support CC2347 | 2531 |
| 2348 | CC2348 | Strategy CC2348 | 1905 |
| 2349 | CC2349 | Engineering CC2349 | 3737 |
| 2350 | CC2350 | Risk CC2350 | 1715 |
| 2351 | CC2351 | Risk CC2351 | 2064 |
| 2352 | CC2352 | Sales CC2352 | 5 |
| 2353 | CC2353 | Legal CC2353 | 2688 |
| 2354 | CC2354 | Audit CC2354 | 3270 |
| 2355 | CC2355 | R&D CC2355 | 3754 |
| 2356 | CC2356 | Support CC2356 | 3721 |
| 2357 | CC2357 | IT CC2357 | 1248 |
| 2358 | CC2358 | Risk CC2358 | 1896 |
| 2359 | CC2359 | Procurement CC2359 | 3573 |
| 2360 | CC2360 | Procurement CC2360 | 1507 |
| 2361 | CC2361 | R&D CC2361 | 2364 |
| 2362 | CC2362 | Risk CC2362 | 72 |
| 2363 | CC2363 | Quality CC2363 | 59 |
| 2364 | CC2364 | Analytics CC2364 | 996 |
| 2365 | CC2365 | Analytics CC2365 | 1846 |
| 2366 | CC2366 | Logistics CC2366 | 1959 |
| 2367 | CC2367 | Treasury CC2367 | 1261 |
| 2368 | CC2368 | HR CC2368 | 2481 |
| 2369 | CC2369 | Procurement CC2369 | 1950 |
| 2370 | CC2370 | R&D CC2370 | 115 |
| 2371 | CC2371 | Quality CC2371 | 3917 |
| 2372 | CC2372 | Finance CC2372 | 1505 |
| 2373 | CC2373 | Compliance CC2373 | 2386 |
| 2374 | CC2374 | Engineering CC2374 | 2601 |
| 2375 | CC2375 | Analytics CC2375 | 478 |
| 2376 | CC2376 | Operations CC2376 | 1974 |
| 2377 | CC2377 | Sales CC2377 | 1192 |
| 2378 | CC2378 | Sales CC2378 | 1364 |
| 2379 | CC2379 | Compliance CC2379 | 3230 |
| 2380 | CC2380 | Finance CC2380 | 2671 |
| 2381 | CC2381 | Procurement CC2381 | 2844 |
| 2382 | CC2382 | IT CC2382 | 2976 |
| 2383 | CC2383 | Marketing CC2383 | 616 |
| 2384 | CC2384 | IT CC2384 | 848 |
| 2385 | CC2385 | Analytics CC2385 | 892 |
| 2386 | CC2386 | Procurement CC2386 | 3881 |
| 2387 | CC2387 | HR CC2387 | 871 |
| 2388 | CC2388 | Procurement CC2388 | 723 |
| 2389 | CC2389 | Operations CC2389 | 2228 |
| 2390 | CC2390 | Logistics CC2390 | 1298 |
| 2391 | CC2391 | HR CC2391 | 2848 |
| 2392 | CC2392 | Treasury CC2392 | 1687 |
| 2393 | CC2393 | Support CC2393 | 3092 |
| 2394 | CC2394 | R&D CC2394 | 509 |
| 2395 | CC2395 | Finance CC2395 | 224 |
| 2396 | CC2396 | Finance CC2396 | 3646 |
| 2397 | CC2397 | Analytics CC2397 | 447 |
| 2398 | CC2398 | Executive CC2398 | 819 |
| 2399 | CC2399 | Strategy CC2399 | 392 |
| 2400 | CC2400 | Legal CC2400 | 2795 |
| 2401 | CC2401 | Compliance CC2401 | 2351 |
| 2402 | CC2402 | Quality CC2402 | 3775 |
| 2403 | CC2403 | Operations CC2403 | 3342 |
| 2404 | CC2404 | Risk CC2404 | 300 |
| 2405 | CC2405 | Quality CC2405 | 1241 |
| 2406 | CC2406 | Procurement CC2406 | 2518 |
| 2407 | CC2407 | Operations CC2407 | 1368 |
| 2408 | CC2408 | Marketing CC2408 | 3558 |
| 2409 | CC2409 | Operations CC2409 | 1648 |
| 2410 | CC2410 | Strategy CC2410 | 2465 |
| 2411 | CC2411 | Logistics CC2411 | 2231 |
| 2412 | CC2412 | Finance CC2412 | 609 |
| 2413 | CC2413 | Executive CC2413 | 1548 |
| 2414 | CC2414 | Compliance CC2414 | 3577 |
| 2415 | CC2415 | Engineering CC2415 | 1512 |
| 2416 | CC2416 | Analytics CC2416 | 901 |
| 2417 | CC2417 | Logistics CC2417 | 3642 |
| 2418 | CC2418 | Compliance CC2418 | 2387 |
| 2419 | CC2419 | Analytics CC2419 | 3719 |
| 2420 | CC2420 | HR CC2420 | 2287 |
| 2421 | CC2421 | R&D CC2421 | 1458 |
| 2422 | CC2422 | Audit CC2422 | 1220 |
| 2423 | CC2423 | Strategy CC2423 | 2965 |
| 2424 | CC2424 | Strategy CC2424 | 1270 |
| 2425 | CC2425 | Operations CC2425 | 3816 |
| 2426 | CC2426 | Legal CC2426 | 2844 |
| 2427 | CC2427 | Logistics CC2427 | 2348 |
| 2428 | CC2428 | Engineering CC2428 | 466 |
| 2429 | CC2429 | Engineering CC2429 | 3447 |
| 2430 | CC2430 | Executive CC2430 | 1413 |
| 2431 | CC2431 | Risk CC2431 | 3614 |
| 2432 | CC2432 | IT CC2432 | 2842 |
| 2433 | CC2433 | Sales CC2433 | 3539 |
| 2434 | CC2434 | Strategy CC2434 | 2812 |
| 2435 | CC2435 | Executive CC2435 | 1824 |
| 2436 | CC2436 | Operations CC2436 | 778 |
| 2437 | CC2437 | Engineering CC2437 | 1435 |
| 2438 | CC2438 | Quality CC2438 | 1774 |
| 2439 | CC2439 | Operations CC2439 | 3882 |
| 2440 | CC2440 | Executive CC2440 | 1494 |
| 2441 | CC2441 | IT CC2441 | 1170 |
| 2442 | CC2442 | Finance CC2442 | 2019 |
| 2443 | CC2443 | Audit CC2443 | 2842 |
| 2444 | CC2444 | Engineering CC2444 | 1030 |
| 2445 | CC2445 | R&D CC2445 | 378 |
| 2446 | CC2446 | Sales CC2446 | 3966 |
| 2447 | CC2447 | Marketing CC2447 | 1562 |
| 2448 | CC2448 | Marketing CC2448 | 3138 |
| 2449 | CC2449 | Support CC2449 | 413 |
| 2450 | CC2450 | Strategy CC2450 | 1612 |
| 2451 | CC2451 | HR CC2451 | 3644 |
| 2452 | CC2452 | Compliance CC2452 | 1125 |
| 2453 | CC2453 | Compliance CC2453 | 456 |
| 2454 | CC2454 | Finance CC2454 | 1593 |
| 2455 | CC2455 | HR CC2455 | 126 |
| 2456 | CC2456 | HR CC2456 | 3010 |
| 2457 | CC2457 | Support CC2457 | 248 |
| 2458 | CC2458 | Treasury CC2458 | 2212 |
| 2459 | CC2459 | Support CC2459 | 1660 |
| 2460 | CC2460 | Logistics CC2460 | 1494 |
| 2461 | CC2461 | Audit CC2461 | 3175 |
| 2462 | CC2462 | Executive CC2462 | 822 |
| 2463 | CC2463 | Finance CC2463 | 2171 |
| 2464 | CC2464 | Risk CC2464 | 3332 |
| 2465 | CC2465 | Engineering CC2465 | 2067 |
| 2466 | CC2466 | Procurement CC2466 | 2672 |
| 2467 | CC2467 | Audit CC2467 | 3332 |
| 2468 | CC2468 | Logistics CC2468 | 3836 |
| 2469 | CC2469 | Engineering CC2469 | 2322 |
| 2470 | CC2470 | Engineering CC2470 | 2637 |
| 2471 | CC2471 | Legal CC2471 | 3809 |
| 2472 | CC2472 | Procurement CC2472 | 1827 |
| 2473 | CC2473 | IT CC2473 | 2979 |
| 2474 | CC2474 | Executive CC2474 | 1923 |
| 2475 | CC2475 | Legal CC2475 | 697 |
| 2476 | CC2476 | Analytics CC2476 | 2552 |
| 2477 | CC2477 | Strategy CC2477 | 1413 |
| 2478 | CC2478 | R&D CC2478 | 545 |
| 2479 | CC2479 | Audit CC2479 | 2555 |
| 2480 | CC2480 | Analytics CC2480 | 3352 |
| 2481 | CC2481 | Quality CC2481 | 2916 |
| 2482 | CC2482 | Legal CC2482 | 1807 |
| 2483 | CC2483 | Quality CC2483 | 495 |
| 2484 | CC2484 | R&D CC2484 | 1467 |
| 2485 | CC2485 | Support CC2485 | 3174 |
| 2486 | CC2486 | Sales CC2486 | 1057 |
| 2487 | CC2487 | Executive CC2487 | 1524 |
| 2488 | CC2488 | Marketing CC2488 | 994 |
| 2489 | CC2489 | Audit CC2489 | 2819 |
| 2490 | CC2490 | HR CC2490 | 1478 |
| 2491 | CC2491 | Logistics CC2491 | 2768 |
| 2492 | CC2492 | Support CC2492 | 1071 |
| 2493 | CC2493 | Operations CC2493 | 3913 |
| 2494 | CC2494 | HR CC2494 | 3455 |
| 2495 | CC2495 | Procurement CC2495 | 2471 |
| 2496 | CC2496 | Marketing CC2496 | 1967 |
| 2497 | CC2497 | R&D CC2497 | 437 |
| 2498 | CC2498 | Logistics CC2498 | 2178 |
| 2499 | CC2499 | R&D CC2499 | 2194 |
| 2500 | CC2500 | Legal CC2500 | 2178 |
| 2501 | CC2501 | Sales CC2501 | 3319 |
| 2502 | CC2502 | Analytics CC2502 | 3823 |
| 2503 | CC2503 | HR CC2503 | 384 |
| 2504 | CC2504 | R&D CC2504 | 709 |
| 2505 | CC2505 | Analytics CC2505 | 2372 |
| 2506 | CC2506 | HR CC2506 | 3937 |
| 2507 | CC2507 | Audit CC2507 | 444 |
| 2508 | CC2508 | Procurement CC2508 | 3108 |
| 2509 | CC2509 | Sales CC2509 | 2934 |
| 2510 | CC2510 | Finance CC2510 | 3717 |
| 2511 | CC2511 | Procurement CC2511 | 296 |
| 2512 | CC2512 | Analytics CC2512 | 3963 |
| 2513 | CC2513 | Finance CC2513 | 3358 |
| 2514 | CC2514 | Audit CC2514 | 2379 |
| 2515 | CC2515 | Strategy CC2515 | 3637 |
| 2516 | CC2516 | Executive CC2516 | 1692 |
| 2517 | CC2517 | Quality CC2517 | 1243 |
| 2518 | CC2518 | Operations CC2518 | 457 |
| 2519 | CC2519 | Compliance CC2519 | 1326 |
| 2520 | CC2520 | Procurement CC2520 | 1539 |
| 2521 | CC2521 | R&D CC2521 | 520 |
| 2522 | CC2522 | Risk CC2522 | 3835 |
| 2523 | CC2523 | Support CC2523 | 3101 |
| 2524 | CC2524 | Legal CC2524 | 1936 |
| 2525 | CC2525 | HR CC2525 | 1333 |
| 2526 | CC2526 | Marketing CC2526 | 2429 |
| 2527 | CC2527 | Procurement CC2527 | 3063 |
| 2528 | CC2528 | Treasury CC2528 | 708 |
| 2529 | CC2529 | Marketing CC2529 | 3634 |
| 2530 | CC2530 | Sales CC2530 | 1064 |
| 2531 | CC2531 | HR CC2531 | 1416 |
| 2532 | CC2532 | Support CC2532 | 3004 |
| 2533 | CC2533 | Sales CC2533 | 1216 |
| 2534 | CC2534 | IT CC2534 | 3392 |
| 2535 | CC2535 | Executive CC2535 | 970 |
| 2536 | CC2536 | Logistics CC2536 | 2230 |
| 2537 | CC2537 | Marketing CC2537 | 2549 |
| 2538 | CC2538 | Logistics CC2538 | 3120 |
| 2539 | CC2539 | Legal CC2539 | 2392 |
| 2540 | CC2540 | Support CC2540 | 843 |
| 2541 | CC2541 | Quality CC2541 | 2498 |
| 2542 | CC2542 | Executive CC2542 | 516 |
| 2543 | CC2543 | R&D CC2543 | 3859 |
| 2544 | CC2544 | Finance CC2544 | 2662 |
| 2545 | CC2545 | Strategy CC2545 | 3319 |
| 2546 | CC2546 | Strategy CC2546 | 1663 |
| 2547 | CC2547 | Analytics CC2547 | 12 |
| 2548 | CC2548 | R&D CC2548 | 918 |
| 2549 | CC2549 | Sales CC2549 | 2446 |
| 2550 | CC2550 | Compliance CC2550 | 77 |
| 2551 | CC2551 | Compliance CC2551 | 2518 |
| 2552 | CC2552 | Operations CC2552 | 1393 |
| 2553 | CC2553 | Analytics CC2553 | 2251 |
| 2554 | CC2554 | Risk CC2554 | 2908 |
| 2555 | CC2555 | Finance CC2555 | 3571 |
| 2556 | CC2556 | Procurement CC2556 | 3161 |
| 2557 | CC2557 | R&D CC2557 | 1966 |
| 2558 | CC2558 | Compliance CC2558 | 457 |
| 2559 | CC2559 | Sales CC2559 | 1257 |
| 2560 | CC2560 | Executive CC2560 | 1388 |
| 2561 | CC2561 | Operations CC2561 | 3313 |
| 2562 | CC2562 | Sales CC2562 | 1290 |
| 2563 | CC2563 | Procurement CC2563 | 2721 |
| 2564 | CC2564 | Legal CC2564 | 1276 |
| 2565 | CC2565 | Strategy CC2565 | 3040 |
| 2566 | CC2566 | Analytics CC2566 | 416 |
| 2567 | CC2567 | Legal CC2567 | 713 |
| 2568 | CC2568 | R&D CC2568 | 3437 |
| 2569 | CC2569 | HR CC2569 | 1192 |
| 2570 | CC2570 | Legal CC2570 | 2711 |
| 2571 | CC2571 | Quality CC2571 | 2445 |
| 2572 | CC2572 | Support CC2572 | 18 |
| 2573 | CC2573 | Finance CC2573 | 1521 |
| 2574 | CC2574 | Support CC2574 | 1176 |
| 2575 | CC2575 | IT CC2575 | 2638 |
| 2576 | CC2576 | Sales CC2576 | 1051 |
| 2577 | CC2577 | R&D CC2577 | 3758 |
| 2578 | CC2578 | Support CC2578 | 1936 |
| 2579 | CC2579 | Strategy CC2579 | 1159 |
| 2580 | CC2580 | Support CC2580 | 3516 |
| 2581 | CC2581 | Compliance CC2581 | 1428 |
| 2582 | CC2582 | Marketing CC2582 | 10 |
| 2583 | CC2583 | Procurement CC2583 | 306 |
| 2584 | CC2584 | Compliance CC2584 | 3113 |
| 2585 | CC2585 | R&D CC2585 | 3336 |
| 2586 | CC2586 | Risk CC2586 | 494 |
| 2587 | CC2587 | Analytics CC2587 | 3477 |
| 2588 | CC2588 | R&D CC2588 | 3717 |
| 2589 | CC2589 | Risk CC2589 | 3825 |
| 2590 | CC2590 | Finance CC2590 | 1765 |
| 2591 | CC2591 | IT CC2591 | 2049 |
| 2592 | CC2592 | Quality CC2592 | 2914 |
| 2593 | CC2593 | Quality CC2593 | 2321 |
| 2594 | CC2594 | IT CC2594 | 217 |
| 2595 | CC2595 | Risk CC2595 | 2355 |
| 2596 | CC2596 | Risk CC2596 | 1341 |
| 2597 | CC2597 | Treasury CC2597 | 501 |
| 2598 | CC2598 | Marketing CC2598 | 3839 |
| 2599 | CC2599 | HR CC2599 | 177 |
| 2600 | CC2600 | Strategy CC2600 | 15 |
| 2601 | CC2601 | Procurement CC2601 | 2813 |
| 2602 | CC2602 | Operations CC2602 | 2109 |
| 2603 | CC2603 | Strategy CC2603 | 52 |
| 2604 | CC2604 | Risk CC2604 | 1281 |
| 2605 | CC2605 | Audit CC2605 | 2089 |
| 2606 | CC2606 | Executive CC2606 | 419 |
| 2607 | CC2607 | Support CC2607 | 293 |
| 2608 | CC2608 | Executive CC2608 | 3715 |
| 2609 | CC2609 | HR CC2609 | 3347 |
| 2610 | CC2610 | Marketing CC2610 | 1493 |
| 2611 | CC2611 | Logistics CC2611 | 2346 |
| 2612 | CC2612 | Audit CC2612 | 703 |
| 2613 | CC2613 | Support CC2613 | 2425 |
| 2614 | CC2614 | Strategy CC2614 | 229 |
| 2615 | CC2615 | Analytics CC2615 | 510 |
| 2616 | CC2616 | Executive CC2616 | 3101 |
| 2617 | CC2617 | Compliance CC2617 | 1127 |
| 2618 | CC2618 | IT CC2618 | 248 |
| 2619 | CC2619 | Audit CC2619 | 904 |
| 2620 | CC2620 | Analytics CC2620 | 957 |
| 2621 | CC2621 | Sales CC2621 | 1298 |
| 2622 | CC2622 | Sales CC2622 | 1209 |
| 2623 | CC2623 | Finance CC2623 | 1655 |
| 2624 | CC2624 | HR CC2624 | 172 |
| 2625 | CC2625 | Support CC2625 | 912 |
| 2626 | CC2626 | Logistics CC2626 | 235 |
| 2627 | CC2627 | Risk CC2627 | 1973 |
| 2628 | CC2628 | Finance CC2628 | 2851 |
| 2629 | CC2629 | Operations CC2629 | 1609 |
| 2630 | CC2630 | IT CC2630 | 2541 |
| 2631 | CC2631 | Operations CC2631 | 1139 |
| 2632 | CC2632 | Marketing CC2632 | 3638 |
| 2633 | CC2633 | Compliance CC2633 | 2346 |
| 2634 | CC2634 | Sales CC2634 | 2297 |
| 2635 | CC2635 | Support CC2635 | 2763 |
| 2636 | CC2636 | Logistics CC2636 | 1955 |
| 2637 | CC2637 | R&D CC2637 | 875 |
| 2638 | CC2638 | Executive CC2638 | 2461 |
| 2639 | CC2639 | Compliance CC2639 | 1546 |
| 2640 | CC2640 | Legal CC2640 | 29 |
| 2641 | CC2641 | Marketing CC2641 | 1581 |
| 2642 | CC2642 | HR CC2642 | 1012 |
| 2643 | CC2643 | Analytics CC2643 | 1374 |
| 2644 | CC2644 | R&D CC2644 | 3473 |
| 2645 | CC2645 | Audit CC2645 | 3062 |
| 2646 | CC2646 | Compliance CC2646 | 822 |
| 2647 | CC2647 | Analytics CC2647 | 3005 |
| 2648 | CC2648 | Logistics CC2648 | 254 |
| 2649 | CC2649 | Executive CC2649 | 3431 |
| 2650 | CC2650 | Treasury CC2650 | 3922 |
| 2651 | CC2651 | Treasury CC2651 | 2228 |
| 2652 | CC2652 | Compliance CC2652 | 1653 |
| 2653 | CC2653 | Risk CC2653 | 1744 |
| 2654 | CC2654 | Finance CC2654 | 2395 |
| 2655 | CC2655 | Executive CC2655 | 866 |
| 2656 | CC2656 | Audit CC2656 | 2033 |
| 2657 | CC2657 | Risk CC2657 | 1703 |
| 2658 | CC2658 | R&D CC2658 | 3210 |
| 2659 | CC2659 | Quality CC2659 | 1720 |
| 2660 | CC2660 | Quality CC2660 | 707 |
| 2661 | CC2661 | Engineering CC2661 | 3654 |
| 2662 | CC2662 | Operations CC2662 | 2265 |
| 2663 | CC2663 | Risk CC2663 | 1522 |
| 2664 | CC2664 | Logistics CC2664 | 3386 |
| 2665 | CC2665 | Legal CC2665 | 2461 |
| 2666 | CC2666 | Legal CC2666 | 1313 |
| 2667 | CC2667 | Executive CC2667 | 1433 |
| 2668 | CC2668 | Engineering CC2668 | 3146 |
| 2669 | CC2669 | Legal CC2669 | 1010 |
| 2670 | CC2670 | Risk CC2670 | 2584 |
| 2671 | CC2671 | Risk CC2671 | 3619 |
| 2672 | CC2672 | Strategy CC2672 | 3071 |
| 2673 | CC2673 | Engineering CC2673 | 2344 |
| 2674 | CC2674 | Compliance CC2674 | 2050 |
| 2675 | CC2675 | Support CC2675 | 107 |
| 2676 | CC2676 | Marketing CC2676 | 3808 |
| 2677 | CC2677 | Finance CC2677 | 286 |
| 2678 | CC2678 | Support CC2678 | 3748 |
| 2679 | CC2679 | Procurement CC2679 | 3845 |
| 2680 | CC2680 | Engineering CC2680 | 3605 |
| 2681 | CC2681 | Executive CC2681 | 2192 |
| 2682 | CC2682 | Strategy CC2682 | 1196 |
| 2683 | CC2683 | Procurement CC2683 | 2394 |
| 2684 | CC2684 | Procurement CC2684 | 3349 |
| 2685 | CC2685 | Analytics CC2685 | 3765 |
| 2686 | CC2686 | Compliance CC2686 | 2784 |
| 2687 | CC2687 | Procurement CC2687 | 2184 |
| 2688 | CC2688 | Logistics CC2688 | 382 |
| 2689 | CC2689 | R&D CC2689 | 1497 |
| 2690 | CC2690 | Risk CC2690 | 2175 |
| 2691 | CC2691 | Compliance CC2691 | 3962 |
| 2692 | CC2692 | R&D CC2692 | 3295 |
| 2693 | CC2693 | Sales CC2693 | 3797 |
| 2694 | CC2694 | IT CC2694 | 2053 |
| 2695 | CC2695 | Finance CC2695 | 2294 |
| 2696 | CC2696 | Engineering CC2696 | 2244 |
| 2697 | CC2697 | Engineering CC2697 | 699 |
| 2698 | CC2698 | Analytics CC2698 | 2445 |
| 2699 | CC2699 | Finance CC2699 | 2018 |
| 2700 | CC2700 | IT CC2700 | 120 |
| 2701 | CC2701 | Finance CC2701 | 114 |
| 2702 | CC2702 | Strategy CC2702 | 3076 |
| 2703 | CC2703 | HR CC2703 | 3192 |
| 2704 | CC2704 | Treasury CC2704 | 305 |
| 2705 | CC2705 | Finance CC2705 | 3468 |
| 2706 | CC2706 | Compliance CC2706 | 298 |
| 2707 | CC2707 | Support CC2707 | 1461 |
| 2708 | CC2708 | IT CC2708 | 3525 |
| 2709 | CC2709 | Operations CC2709 | 3785 |
| 2710 | CC2710 | R&D CC2710 | 223 |
| 2711 | CC2711 | Treasury CC2711 | 1863 |
| 2712 | CC2712 | Treasury CC2712 | 2455 |
| 2713 | CC2713 | Engineering CC2713 | 3458 |
| 2714 | CC2714 | Strategy CC2714 | 36 |
| 2715 | CC2715 | Procurement CC2715 | 1774 |
| 2716 | CC2716 | Executive CC2716 | 2321 |
| 2717 | CC2717 | Audit CC2717 | 3032 |
| 2718 | CC2718 | Finance CC2718 | 2555 |
| 2719 | CC2719 | Executive CC2719 | 2227 |
| 2720 | CC2720 | Operations CC2720 | 3882 |
| 2721 | CC2721 | Analytics CC2721 | 1181 |
| 2722 | CC2722 | Sales CC2722 | 3633 |
| 2723 | CC2723 | Risk CC2723 | 1393 |
| 2724 | CC2724 | IT CC2724 | 2792 |
| 2725 | CC2725 | Engineering CC2725 | 624 |
| 2726 | CC2726 | R&D CC2726 | 2088 |
| 2727 | CC2727 | R&D CC2727 | 1919 |
| 2728 | CC2728 | Sales CC2728 | 2384 |
| 2729 | CC2729 | Strategy CC2729 | 85 |
| 2730 | CC2730 | Marketing CC2730 | 1088 |
| 2731 | CC2731 | Operations CC2731 | 871 |
| 2732 | CC2732 | Support CC2732 | 374 |
| 2733 | CC2733 | HR CC2733 | 2736 |
| 2734 | CC2734 | IT CC2734 | 3202 |
| 2735 | CC2735 | Logistics CC2735 | 310 |
| 2736 | CC2736 | Audit CC2736 | 757 |
| 2737 | CC2737 | HR CC2737 | 3614 |
| 2738 | CC2738 | Finance CC2738 | 1139 |
| 2739 | CC2739 | Quality CC2739 | 1452 |
| 2740 | CC2740 | Executive CC2740 | 317 |
| 2741 | CC2741 | Logistics CC2741 | 737 |
| 2742 | CC2742 | Legal CC2742 | 1131 |
| 2743 | CC2743 | Compliance CC2743 | 2401 |
| 2744 | CC2744 | Strategy CC2744 | 681 |
| 2745 | CC2745 | Engineering CC2745 | 1691 |
| 2746 | CC2746 | Operations CC2746 | 2937 |
| 2747 | CC2747 | Operations CC2747 | 2038 |
| 2748 | CC2748 | Strategy CC2748 | 24 |
| 2749 | CC2749 | Engineering CC2749 | 1117 |
| 2750 | CC2750 | Compliance CC2750 | 1449 |
| 2751 | CC2751 | Support CC2751 | 2490 |
| 2752 | CC2752 | Strategy CC2752 | 952 |
| 2753 | CC2753 | Compliance CC2753 | 1910 |
| 2754 | CC2754 | Marketing CC2754 | 948 |
| 2755 | CC2755 | R&D CC2755 | 649 |
| 2756 | CC2756 | Treasury CC2756 | 465 |
| 2757 | CC2757 | Compliance CC2757 | 1069 |
| 2758 | CC2758 | Strategy CC2758 | 1183 |
| 2759 | CC2759 | Quality CC2759 | 1995 |
| 2760 | CC2760 | Compliance CC2760 | 576 |
| 2761 | CC2761 | Strategy CC2761 | 2516 |
| 2762 | CC2762 | Finance CC2762 | 683 |
| 2763 | CC2763 | Sales CC2763 | 3113 |
| 2764 | CC2764 | Marketing CC2764 | 3189 |
| 2765 | CC2765 | Audit CC2765 | 479 |
| 2766 | CC2766 | Support CC2766 | 2737 |
| 2767 | CC2767 | Strategy CC2767 | 455 |
| 2768 | CC2768 | Treasury CC2768 | 291 |
| 2769 | CC2769 | Risk CC2769 | 2200 |
| 2770 | CC2770 | R&D CC2770 | 2859 |
| 2771 | CC2771 | Executive CC2771 | 3725 |
| 2772 | CC2772 | Compliance CC2772 | 1726 |
| 2773 | CC2773 | Logistics CC2773 | 3983 |
| 2774 | CC2774 | IT CC2774 | 558 |
| 2775 | CC2775 | Sales CC2775 | 478 |
| 2776 | CC2776 | HR CC2776 | 2859 |
| 2777 | CC2777 | Quality CC2777 | 3253 |
| 2778 | CC2778 | Finance CC2778 | 2132 |
| 2779 | CC2779 | Marketing CC2779 | 3504 |
| 2780 | CC2780 | Executive CC2780 | 2348 |
| 2781 | CC2781 | HR CC2781 | 1575 |
| 2782 | CC2782 | R&D CC2782 | 2781 |
| 2783 | CC2783 | Procurement CC2783 | 3583 |
| 2784 | CC2784 | Operations CC2784 | 2728 |
| 2785 | CC2785 | Strategy CC2785 | 261 |
| 2786 | CC2786 | Audit CC2786 | 3182 |
| 2787 | CC2787 | Sales CC2787 | 3389 |
| 2788 | CC2788 | Legal CC2788 | 3186 |
| 2789 | CC2789 | Support CC2789 | 3960 |
| 2790 | CC2790 | Logistics CC2790 | 1391 |
| 2791 | CC2791 | Treasury CC2791 | 120 |
| 2792 | CC2792 | R&D CC2792 | 1374 |
| 2793 | CC2793 | Sales CC2793 | 3004 |
| 2794 | CC2794 | Marketing CC2794 | 1002 |
| 2795 | CC2795 | Compliance CC2795 | 2868 |
| 2796 | CC2796 | R&D CC2796 | 2196 |
| 2797 | CC2797 | Marketing CC2797 | 1413 |
| 2798 | CC2798 | Operations CC2798 | 1331 |
| 2799 | CC2799 | Marketing CC2799 | 3844 |
| 2800 | CC2800 | Risk CC2800 | 1385 |
| 2801 | CC2801 | Strategy CC2801 | 884 |
| 2802 | CC2802 | Analytics CC2802 | 1125 |
| 2803 | CC2803 | Support CC2803 | 3133 |
| 2804 | CC2804 | Compliance CC2804 | 852 |
| 2805 | CC2805 | Risk CC2805 | 533 |
| 2806 | CC2806 | Audit CC2806 | 3441 |
| 2807 | CC2807 | Legal CC2807 | 2952 |
| 2808 | CC2808 | Logistics CC2808 | 3748 |
| 2809 | CC2809 | Marketing CC2809 | 1872 |
| 2810 | CC2810 | Sales CC2810 | 3015 |
| 2811 | CC2811 | R&D CC2811 | 2797 |
| 2812 | CC2812 | Treasury CC2812 | 2836 |
| 2813 | CC2813 | IT CC2813 | 2259 |
| 2814 | CC2814 | Analytics CC2814 | 3561 |
| 2815 | CC2815 | Finance CC2815 | 698 |
| 2816 | CC2816 | Operations CC2816 | 3295 |
| 2817 | CC2817 | Audit CC2817 | 3940 |
| 2818 | CC2818 | Strategy CC2818 | 3112 |
| 2819 | CC2819 | Logistics CC2819 | 3445 |
| 2820 | CC2820 | Marketing CC2820 | 1798 |
| 2821 | CC2821 | Support CC2821 | 672 |
| 2822 | CC2822 | Strategy CC2822 | 3344 |
| 2823 | CC2823 | Support CC2823 | 2162 |
| 2824 | CC2824 | Risk CC2824 | 1549 |
| 2825 | CC2825 | Procurement CC2825 | 3658 |
| 2826 | CC2826 | Compliance CC2826 | 3129 |
| 2827 | CC2827 | Legal CC2827 | 573 |
| 2828 | CC2828 | HR CC2828 | 516 |
| 2829 | CC2829 | Risk CC2829 | 2941 |
| 2830 | CC2830 | Finance CC2830 | 1437 |
| 2831 | CC2831 | Operations CC2831 | 1449 |
| 2832 | CC2832 | Marketing CC2832 | 1207 |
| 2833 | CC2833 | R&D CC2833 | 2718 |
| 2834 | CC2834 | Strategy CC2834 | 567 |
| 2835 | CC2835 | Support CC2835 | 96 |
| 2836 | CC2836 | Engineering CC2836 | 1817 |
| 2837 | CC2837 | Marketing CC2837 | 2340 |
| 2838 | CC2838 | Logistics CC2838 | 1961 |
| 2839 | CC2839 | Support CC2839 | 2795 |
| 2840 | CC2840 | Operations CC2840 | 2850 |
| 2841 | CC2841 | Analytics CC2841 | 1621 |
| 2842 | CC2842 | Compliance CC2842 | 2498 |
| 2843 | CC2843 | Treasury CC2843 | 1300 |
| 2844 | CC2844 | IT CC2844 | 3733 |
| 2845 | CC2845 | Risk CC2845 | 233 |
| 2846 | CC2846 | Operations CC2846 | 2479 |
| 2847 | CC2847 | Risk CC2847 | 2452 |
| 2848 | CC2848 | Procurement CC2848 | 3745 |
| 2849 | CC2849 | Compliance CC2849 | 1280 |
| 2850 | CC2850 | Sales CC2850 | 1758 |
| 2851 | CC2851 | Marketing CC2851 | 2760 |
| 2852 | CC2852 | Compliance CC2852 | 370 |
| 2853 | CC2853 | Treasury CC2853 | 2165 |
| 2854 | CC2854 | Marketing CC2854 | 1558 |
| 2855 | CC2855 | R&D CC2855 | 3979 |
| 2856 | CC2856 | R&D CC2856 | 2155 |
| 2857 | CC2857 | Legal CC2857 | 1740 |
| 2858 | CC2858 | Executive CC2858 | 3742 |
| 2859 | CC2859 | HR CC2859 | 880 |
| 2860 | CC2860 | Procurement CC2860 | 3263 |
| 2861 | CC2861 | R&D CC2861 | 1550 |
| 2862 | CC2862 | Support CC2862 | 3195 |
| 2863 | CC2863 | Analytics CC2863 | 2728 |
| 2864 | CC2864 | Marketing CC2864 | 2412 |
| 2865 | CC2865 | Analytics CC2865 | 2484 |
| 2866 | CC2866 | Sales CC2866 | 1793 |
| 2867 | CC2867 | Strategy CC2867 | 1066 |
| 2868 | CC2868 | Sales CC2868 | 1859 |
| 2869 | CC2869 | Legal CC2869 | 597 |
| 2870 | CC2870 | Marketing CC2870 | 3739 |
| 2871 | CC2871 | Quality CC2871 | 3005 |
| 2872 | CC2872 | Sales CC2872 | 2971 |
| 2873 | CC2873 | Finance CC2873 | 1555 |
| 2874 | CC2874 | Sales CC2874 | 358 |
| 2875 | CC2875 | Legal CC2875 | 309 |
| 2876 | CC2876 | Sales CC2876 | 2676 |
| 2877 | CC2877 | Executive CC2877 | 1991 |
| 2878 | CC2878 | Procurement CC2878 | 3497 |
| 2879 | CC2879 | Treasury CC2879 | 262 |
| 2880 | CC2880 | Compliance CC2880 | 2699 |
| 2881 | CC2881 | Logistics CC2881 | 2558 |
| 2882 | CC2882 | Procurement CC2882 | 544 |
| 2883 | CC2883 | Engineering CC2883 | 1941 |
| 2884 | CC2884 | Finance CC2884 | 2993 |
| 2885 | CC2885 | Procurement CC2885 | 2864 |
| 2886 | CC2886 | Treasury CC2886 | 532 |
| 2887 | CC2887 | Sales CC2887 | 1180 |
| 2888 | CC2888 | Procurement CC2888 | 2423 |
| 2889 | CC2889 | Engineering CC2889 | 2291 |
| 2890 | CC2890 | HR CC2890 | 1933 |
| 2891 | CC2891 | Compliance CC2891 | 2895 |
| 2892 | CC2892 | Marketing CC2892 | 320 |
| 2893 | CC2893 | Risk CC2893 | 1403 |
| 2894 | CC2894 | Audit CC2894 | 3393 |
| 2895 | CC2895 | Executive CC2895 | 70 |
| 2896 | CC2896 | R&D CC2896 | 1515 |
| 2897 | CC2897 | Strategy CC2897 | 1848 |
| 2898 | CC2898 | Executive CC2898 | 3082 |
| 2899 | CC2899 | Finance CC2899 | 3672 |
| 2900 | CC2900 | Operations CC2900 | 1639 |
| 2901 | CC2901 | Risk CC2901 | 754 |
| 2902 | CC2902 | Risk CC2902 | 1550 |
| 2903 | CC2903 | Support CC2903 | 3550 |
| 2904 | CC2904 | Treasury CC2904 | 1293 |
| 2905 | CC2905 | Risk CC2905 | 1612 |
| 2906 | CC2906 | Engineering CC2906 | 911 |
| 2907 | CC2907 | Sales CC2907 | 1651 |
| 2908 | CC2908 | Logistics CC2908 | 1807 |
| 2909 | CC2909 | Risk CC2909 | 171 |
| 2910 | CC2910 | Marketing CC2910 | 2902 |
| 2911 | CC2911 | Logistics CC2911 | 1668 |
| 2912 | CC2912 | Compliance CC2912 | 3629 |
| 2913 | CC2913 | Strategy CC2913 | 1488 |
| 2914 | CC2914 | HR CC2914 | 1620 |
| 2915 | CC2915 | Audit CC2915 | 1201 |
| 2916 | CC2916 | Operations CC2916 | 993 |
| 2917 | CC2917 | Executive CC2917 | 2940 |
| 2918 | CC2918 | Procurement CC2918 | 647 |
| 2919 | CC2919 | Compliance CC2919 | 3184 |
| 2920 | CC2920 | Quality CC2920 | 1700 |
| 2921 | CC2921 | Procurement CC2921 | 882 |
| 2922 | CC2922 | Analytics CC2922 | 2005 |
| 2923 | CC2923 | Support CC2923 | 1161 |
| 2924 | CC2924 | Executive CC2924 | 2133 |
| 2925 | CC2925 | Marketing CC2925 | 3064 |
| 2926 | CC2926 | Logistics CC2926 | 3735 |
| 2927 | CC2927 | Strategy CC2927 | 1480 |
| 2928 | CC2928 | Sales CC2928 | 3530 |
| 2929 | CC2929 | Analytics CC2929 | 466 |
| 2930 | CC2930 | Finance CC2930 | 2154 |
| 2931 | CC2931 | Engineering CC2931 | 2584 |
| 2932 | CC2932 | IT CC2932 | 2067 |
| 2933 | CC2933 | Analytics CC2933 | 2306 |
| 2934 | CC2934 | Audit CC2934 | 2471 |
| 2935 | CC2935 | Operations CC2935 | 1935 |
| 2936 | CC2936 | Audit CC2936 | 475 |
| 2937 | CC2937 | Quality CC2937 | 246 |
| 2938 | CC2938 | Treasury CC2938 | 3994 |
| 2939 | CC2939 | Audit CC2939 | 2009 |
| 2940 | CC2940 | IT CC2940 | 2224 |
| 2941 | CC2941 | Quality CC2941 | 1814 |
| 2942 | CC2942 | Executive CC2942 | 132 |
| 2943 | CC2943 | Engineering CC2943 | 3332 |
| 2944 | CC2944 | R&D CC2944 | 286 |
| 2945 | CC2945 | Support CC2945 | 49 |
| 2946 | CC2946 | Support CC2946 | 1722 |
| 2947 | CC2947 | Audit CC2947 | 2643 |
| 2948 | CC2948 | Engineering CC2948 | 2766 |
| 2949 | CC2949 | Treasury CC2949 | 1142 |
| 2950 | CC2950 | Logistics CC2950 | 1970 |
| 2951 | CC2951 | Analytics CC2951 | 2995 |
| 2952 | CC2952 | Compliance CC2952 | 3128 |
| 2953 | CC2953 | Marketing CC2953 | 2258 |
| 2954 | CC2954 | Sales CC2954 | 1099 |
| 2955 | CC2955 | Engineering CC2955 | 1046 |
| 2956 | CC2956 | Legal CC2956 | 3482 |
| 2957 | CC2957 | Treasury CC2957 | 684 |
| 2958 | CC2958 | Support CC2958 | 3127 |
| 2959 | CC2959 | Procurement CC2959 | 121 |
| 2960 | CC2960 | Audit CC2960 | 2165 |
| 2961 | CC2961 | Logistics CC2961 | 1077 |
| 2962 | CC2962 | IT CC2962 | 2175 |
| 2963 | CC2963 | Operations CC2963 | 1456 |
| 2964 | CC2964 | Audit CC2964 | 2652 |
| 2965 | CC2965 | R&D CC2965 | 2649 |
| 2966 | CC2966 | R&D CC2966 | 1669 |
| 2967 | CC2967 | Audit CC2967 | 3527 |
| 2968 | CC2968 | Quality CC2968 | 3565 |
| 2969 | CC2969 | Treasury CC2969 | 1332 |
| 2970 | CC2970 | Analytics CC2970 | 3874 |
| 2971 | CC2971 | Finance CC2971 | 1987 |
| 2972 | CC2972 | Support CC2972 | 3425 |
| 2973 | CC2973 | Sales CC2973 | 792 |
| 2974 | CC2974 | Risk CC2974 | 2475 |
| 2975 | CC2975 | Procurement CC2975 | 204 |
| 2976 | CC2976 | Sales CC2976 | 2940 |
| 2977 | CC2977 | Support CC2977 | 2355 |
| 2978 | CC2978 | Legal CC2978 | 2548 |
| 2979 | CC2979 | Operations CC2979 | 3561 |
| 2980 | CC2980 | Legal CC2980 | 20 |
| 2981 | CC2981 | Support CC2981 | 562 |
| 2982 | CC2982 | Engineering CC2982 | 1411 |
| 2983 | CC2983 | Quality CC2983 | 224 |
| 2984 | CC2984 | R&D CC2984 | 312 |
| 2985 | CC2985 | Executive CC2985 | 2696 |
| 2986 | CC2986 | HR CC2986 | 1432 |
| 2987 | CC2987 | Audit CC2987 | 2475 |
| 2988 | CC2988 | Procurement CC2988 | 2361 |
| 2989 | CC2989 | Risk CC2989 | 3121 |
| 2990 | CC2990 | Support CC2990 | 1686 |
| 2991 | CC2991 | Sales CC2991 | 487 |
| 2992 | CC2992 | Executive CC2992 | 324 |
| 2993 | CC2993 | IT CC2993 | 3433 |
| 2994 | CC2994 | Legal CC2994 | 638 |
| 2995 | CC2995 | Operations CC2995 | 2521 |
| 2996 | CC2996 | Operations CC2996 | 1917 |
| 2997 | CC2997 | Operations CC2997 | 3576 |
| 2998 | CC2998 | Risk CC2998 | 110 |
| 2999 | CC2999 | Treasury CC2999 | 2381 |
| 3000 | CC3000 | Risk CC3000 | 661 |
| 3001 | CC3001 | Procurement CC3001 | 2509 |
| 3002 | CC3002 | IT CC3002 | 2817 |
| 3003 | CC3003 | R&D CC3003 | 3638 |
| 3004 | CC3004 | Analytics CC3004 | 3855 |
| 3005 | CC3005 | IT CC3005 | 3095 |
| 3006 | CC3006 | Compliance CC3006 | 3249 |
| 3007 | CC3007 | Sales CC3007 | 3178 |
| 3008 | CC3008 | Strategy CC3008 | 1748 |
| 3009 | CC3009 | R&D CC3009 | 402 |
| 3010 | CC3010 | Operations CC3010 | 2499 |
| 3011 | CC3011 | Quality CC3011 | 304 |
| 3012 | CC3012 | R&D CC3012 | 3168 |
| 3013 | CC3013 | Audit CC3013 | 3858 |
| 3014 | CC3014 | Strategy CC3014 | 2562 |
| 3015 | CC3015 | Strategy CC3015 | 1393 |
| 3016 | CC3016 | Support CC3016 | 1609 |
| 3017 | CC3017 | R&D CC3017 | 33 |
| 3018 | CC3018 | Audit CC3018 | 1850 |
| 3019 | CC3019 | Audit CC3019 | 280 |
| 3020 | CC3020 | Strategy CC3020 | 2805 |
| 3021 | CC3021 | Support CC3021 | 1384 |
| 3022 | CC3022 | HR CC3022 | 2817 |
| 3023 | CC3023 | Strategy CC3023 | 2167 |
| 3024 | CC3024 | Audit CC3024 | 2343 |
| 3025 | CC3025 | Strategy CC3025 | 2711 |
| 3026 | CC3026 | Analytics CC3026 | 2056 |
| 3027 | CC3027 | IT CC3027 | 2360 |
| 3028 | CC3028 | Engineering CC3028 | 3289 |
| 3029 | CC3029 | Procurement CC3029 | 157 |
| 3030 | CC3030 | Sales CC3030 | 485 |
| 3031 | CC3031 | Strategy CC3031 | 3547 |
| 3032 | CC3032 | Treasury CC3032 | 439 |
| 3033 | CC3033 | IT CC3033 | 1741 |
| 3034 | CC3034 | Risk CC3034 | 122 |
| 3035 | CC3035 | Executive CC3035 | 806 |
| 3036 | CC3036 | Legal CC3036 | 677 |
| 3037 | CC3037 | Risk CC3037 | 3613 |
| 3038 | CC3038 | Executive CC3038 | 86 |
| 3039 | CC3039 | Sales CC3039 | 15 |
| 3040 | CC3040 | Sales CC3040 | 2892 |
| 3041 | CC3041 | Strategy CC3041 | 92 |
| 3042 | CC3042 | Treasury CC3042 | 2683 |
| 3043 | CC3043 | Analytics CC3043 | 677 |
| 3044 | CC3044 | Logistics CC3044 | 2916 |
| 3045 | CC3045 | Compliance CC3045 | 2474 |
| 3046 | CC3046 | Support CC3046 | 2083 |
| 3047 | CC3047 | Treasury CC3047 | 10 |
| 3048 | CC3048 | Risk CC3048 | 2758 |
| 3049 | CC3049 | Finance CC3049 | 224 |
| 3050 | CC3050 | Operations CC3050 | 2251 |
| 3051 | CC3051 | Finance CC3051 | 2024 |
| 3052 | CC3052 | Operations CC3052 | 3521 |
| 3053 | CC3053 | R&D CC3053 | 3544 |
| 3054 | CC3054 | Engineering CC3054 | 2012 |
| 3055 | CC3055 | R&D CC3055 | 851 |
| 3056 | CC3056 | Engineering CC3056 | 3583 |
| 3057 | CC3057 | Risk CC3057 | 3229 |
| 3058 | CC3058 | Executive CC3058 | 1521 |
| 3059 | CC3059 | IT CC3059 | 2747 |
| 3060 | CC3060 | Quality CC3060 | 3026 |
| 3061 | CC3061 | Operations CC3061 | 1046 |
| 3062 | CC3062 | Finance CC3062 | 2488 |
| 3063 | CC3063 | Compliance CC3063 | 1271 |
| 3064 | CC3064 | Marketing CC3064 | 1014 |
| 3065 | CC3065 | Executive CC3065 | 1378 |
| 3066 | CC3066 | Strategy CC3066 | 854 |
| 3067 | CC3067 | Procurement CC3067 | 1502 |
| 3068 | CC3068 | Risk CC3068 | 2180 |
| 3069 | CC3069 | Procurement CC3069 | 224 |
| 3070 | CC3070 | Finance CC3070 | 716 |
| 3071 | CC3071 | Engineering CC3071 | 952 |
| 3072 | CC3072 | R&D CC3072 | 65 |
| 3073 | CC3073 | Compliance CC3073 | 1435 |
| 3074 | CC3074 | Engineering CC3074 | 1972 |
| 3075 | CC3075 | Engineering CC3075 | 772 |
| 3076 | CC3076 | Support CC3076 | 3594 |
| 3077 | CC3077 | IT CC3077 | 3476 |
| 3078 | CC3078 | HR CC3078 | 600 |
| 3079 | CC3079 | Operations CC3079 | 974 |
| 3080 | CC3080 | Procurement CC3080 | 3999 |
| 3081 | CC3081 | Quality CC3081 | 262 |
| 3082 | CC3082 | IT CC3082 | 3921 |
| 3083 | CC3083 | Engineering CC3083 | 317 |
| 3084 | CC3084 | IT CC3084 | 1074 |
| 3085 | CC3085 | Marketing CC3085 | 779 |
| 3086 | CC3086 | Executive CC3086 | 3399 |
| 3087 | CC3087 | IT CC3087 | 599 |
| 3088 | CC3088 | Compliance CC3088 | 563 |
| 3089 | CC3089 | IT CC3089 | 835 |
| 3090 | CC3090 | Treasury CC3090 | 2374 |
| 3091 | CC3091 | Executive CC3091 | 1059 |
| 3092 | CC3092 | R&D CC3092 | 228 |
| 3093 | CC3093 | HR CC3093 | 1998 |
| 3094 | CC3094 | Executive CC3094 | 616 |
| 3095 | CC3095 | Legal CC3095 | 3044 |
| 3096 | CC3096 | Quality CC3096 | 1083 |
| 3097 | CC3097 | Finance CC3097 | 2165 |
| 3098 | CC3098 | Legal CC3098 | 105 |
| 3099 | CC3099 | Engineering CC3099 | 305 |
| 3100 | CC3100 | Sales CC3100 | 2289 |
| 3101 | CC3101 | Procurement CC3101 | 610 |
| 3102 | CC3102 | Quality CC3102 | 1486 |
| 3103 | CC3103 | Analytics CC3103 | 389 |
| 3104 | CC3104 | HR CC3104 | 2683 |
| 3105 | CC3105 | Support CC3105 | 3190 |
| 3106 | CC3106 | Treasury CC3106 | 1199 |
| 3107 | CC3107 | HR CC3107 | 1041 |
| 3108 | CC3108 | Support CC3108 | 1939 |
| 3109 | CC3109 | Quality CC3109 | 2787 |
| 3110 | CC3110 | R&D CC3110 | 3796 |
| 3111 | CC3111 | Audit CC3111 | 3983 |
| 3112 | CC3112 | Procurement CC3112 | 3599 |
| 3113 | CC3113 | Audit CC3113 | 3555 |
| 3114 | CC3114 | Risk CC3114 | 1851 |
| 3115 | CC3115 | Risk CC3115 | 3224 |
| 3116 | CC3116 | Legal CC3116 | 1808 |
| 3117 | CC3117 | HR CC3117 | 1053 |
| 3118 | CC3118 | Audit CC3118 | 959 |
| 3119 | CC3119 | IT CC3119 | 2998 |
| 3120 | CC3120 | Treasury CC3120 | 161 |
| 3121 | CC3121 | IT CC3121 | 488 |
| 3122 | CC3122 | Audit CC3122 | 1677 |
| 3123 | CC3123 | Risk CC3123 | 3352 |
| 3124 | CC3124 | Logistics CC3124 | 201 |
| 3125 | CC3125 | IT CC3125 | 3875 |
| 3126 | CC3126 | Finance CC3126 | 740 |
| 3127 | CC3127 | Support CC3127 | 1828 |
| 3128 | CC3128 | Treasury CC3128 | 3333 |
| 3129 | CC3129 | Legal CC3129 | 1759 |
| 3130 | CC3130 | Logistics CC3130 | 2007 |
| 3131 | CC3131 | Logistics CC3131 | 177 |
| 3132 | CC3132 | Audit CC3132 | 1139 |
| 3133 | CC3133 | Finance CC3133 | 1482 |
| 3134 | CC3134 | Audit CC3134 | 3473 |
| 3135 | CC3135 | Engineering CC3135 | 1791 |
| 3136 | CC3136 | Compliance CC3136 | 1123 |
| 3137 | CC3137 | IT CC3137 | 3479 |
| 3138 | CC3138 | Support CC3138 | 309 |
| 3139 | CC3139 | Operations CC3139 | 1003 |
| 3140 | CC3140 | Marketing CC3140 | 1104 |
| 3141 | CC3141 | R&D CC3141 | 3115 |
| 3142 | CC3142 | Quality CC3142 | 3344 |
| 3143 | CC3143 | Risk CC3143 | 3790 |
| 3144 | CC3144 | Marketing CC3144 | 2938 |
| 3145 | CC3145 | Legal CC3145 | 2604 |
| 3146 | CC3146 | HR CC3146 | 1355 |
| 3147 | CC3147 | Audit CC3147 | 2301 |
| 3148 | CC3148 | HR CC3148 | 2957 |
| 3149 | CC3149 | Legal CC3149 | 2180 |
| 3150 | CC3150 | Analytics CC3150 | 2608 |
| 3151 | CC3151 | Compliance CC3151 | 1936 |
| 3152 | CC3152 | Risk CC3152 | 30 |
| 3153 | CC3153 | Sales CC3153 | 268 |
| 3154 | CC3154 | Legal CC3154 | 3058 |
| 3155 | CC3155 | Strategy CC3155 | 868 |
| 3156 | CC3156 | Audit CC3156 | 1547 |
| 3157 | CC3157 | Treasury CC3157 | 1875 |
| 3158 | CC3158 | Sales CC3158 | 59 |
| 3159 | CC3159 | Sales CC3159 | 2719 |
| 3160 | CC3160 | IT CC3160 | 2882 |
| 3161 | CC3161 | Procurement CC3161 | 3459 |
| 3162 | CC3162 | R&D CC3162 | 2079 |
| 3163 | CC3163 | Finance CC3163 | 3225 |
| 3164 | CC3164 | Audit CC3164 | 3796 |
| 3165 | CC3165 | Compliance CC3165 | 1770 |
| 3166 | CC3166 | Risk CC3166 | 1270 |
| 3167 | CC3167 | Quality CC3167 | 3260 |
| 3168 | CC3168 | Legal CC3168 | 2816 |
| 3169 | CC3169 | IT CC3169 | 1606 |
| 3170 | CC3170 | HR CC3170 | 3180 |
| 3171 | CC3171 | Quality CC3171 | 1579 |
| 3172 | CC3172 | Treasury CC3172 | 525 |
| 3173 | CC3173 | Risk CC3173 | 3960 |
| 3174 | CC3174 | Engineering CC3174 | 3184 |
| 3175 | CC3175 | Operations CC3175 | 2179 |
| 3176 | CC3176 | Operations CC3176 | 2831 |
| 3177 | CC3177 | R&D CC3177 | 289 |
| 3178 | CC3178 | Operations CC3178 | 3170 |
| 3179 | CC3179 | Support CC3179 | 3393 |
| 3180 | CC3180 | Support CC3180 | 3246 |
| 3181 | CC3181 | Sales CC3181 | 3411 |
| 3182 | CC3182 | Executive CC3182 | 1639 |
| 3183 | CC3183 | Analytics CC3183 | 1692 |
| 3184 | CC3184 | Procurement CC3184 | 2357 |
| 3185 | CC3185 | Quality CC3185 | 1160 |
| 3186 | CC3186 | Engineering CC3186 | 200 |
| 3187 | CC3187 | Treasury CC3187 | 2430 |
| 3188 | CC3188 | Strategy CC3188 | 3646 |
| 3189 | CC3189 | Logistics CC3189 | 3386 |
| 3190 | CC3190 | Marketing CC3190 | 822 |
| 3191 | CC3191 | Legal CC3191 | 1022 |
| 3192 | CC3192 | Compliance CC3192 | 2093 |
| 3193 | CC3193 | Legal CC3193 | 1891 |
| 3194 | CC3194 | Engineering CC3194 | 556 |
| 3195 | CC3195 | IT CC3195 | 1466 |
| 3196 | CC3196 | Procurement CC3196 | 2250 |
| 3197 | CC3197 | Procurement CC3197 | 1721 |
| 3198 | CC3198 | Procurement CC3198 | 3241 |
| 3199 | CC3199 | Procurement CC3199 | 350 |
| 3200 | CC3200 | HR CC3200 | 3019 |
| 3201 | CC3201 | IT CC3201 | 89 |
| 3202 | CC3202 | Finance CC3202 | 3256 |
| 3203 | CC3203 | Compliance CC3203 | 3680 |
| 3204 | CC3204 | Support CC3204 | 586 |
| 3205 | CC3205 | HR CC3205 | 3477 |
| 3206 | CC3206 | Strategy CC3206 | 3905 |
| 3207 | CC3207 | Legal CC3207 | 1159 |
| 3208 | CC3208 | Analytics CC3208 | 584 |
| 3209 | CC3209 | HR CC3209 | 1991 |
| 3210 | CC3210 | Operations CC3210 | 2244 |
| 3211 | CC3211 | Operations CC3211 | 2783 |
| 3212 | CC3212 | Procurement CC3212 | 865 |
| 3213 | CC3213 | Treasury CC3213 | 935 |
| 3214 | CC3214 | Quality CC3214 | 1998 |
| 3215 | CC3215 | Logistics CC3215 | 2757 |
| 3216 | CC3216 | Risk CC3216 | 1480 |
| 3217 | CC3217 | Legal CC3217 | 3579 |
| 3218 | CC3218 | Quality CC3218 | 3415 |
| 3219 | CC3219 | Audit CC3219 | 3484 |
| 3220 | CC3220 | Strategy CC3220 | 1703 |
| 3221 | CC3221 | Strategy CC3221 | 1555 |
| 3222 | CC3222 | Marketing CC3222 | 1023 |
| 3223 | CC3223 | Risk CC3223 | 658 |
| 3224 | CC3224 | Procurement CC3224 | 3846 |
| 3225 | CC3225 | Compliance CC3225 | 2477 |
| 3226 | CC3226 | HR CC3226 | 2824 |
| 3227 | CC3227 | Logistics CC3227 | 2275 |
| 3228 | CC3228 | Compliance CC3228 | 3325 |
| 3229 | CC3229 | Procurement CC3229 | 3483 |
| 3230 | CC3230 | Operations CC3230 | 1783 |
| 3231 | CC3231 | Audit CC3231 | 1849 |
| 3232 | CC3232 | Finance CC3232 | 1444 |
| 3233 | CC3233 | Sales CC3233 | 1283 |
| 3234 | CC3234 | Marketing CC3234 | 2783 |
| 3235 | CC3235 | Procurement CC3235 | 3232 |
| 3236 | CC3236 | Logistics CC3236 | 2888 |
| 3237 | CC3237 | Quality CC3237 | 76 |
| 3238 | CC3238 | Quality CC3238 | 1827 |
| 3239 | CC3239 | Support CC3239 | 3426 |
| 3240 | CC3240 | Legal CC3240 | 2777 |
| 3241 | CC3241 | Operations CC3241 | 3359 |
| 3242 | CC3242 | Engineering CC3242 | 2327 |
| 3243 | CC3243 | Procurement CC3243 | 1765 |
| 3244 | CC3244 | Support CC3244 | 1901 |
| 3245 | CC3245 | Legal CC3245 | 3387 |
| 3246 | CC3246 | Compliance CC3246 | 768 |
| 3247 | CC3247 | Support CC3247 | 133 |
| 3248 | CC3248 | IT CC3248 | 3227 |
| 3249 | CC3249 | Audit CC3249 | 1054 |
| 3250 | CC3250 | Audit CC3250 | 1441 |
| 3251 | CC3251 | Marketing CC3251 | 1368 |
| 3252 | CC3252 | Engineering CC3252 | 1436 |
| 3253 | CC3253 | Finance CC3253 | 1897 |
| 3254 | CC3254 | Support CC3254 | 1466 |
| 3255 | CC3255 | Operations CC3255 | 3209 |
| 3256 | CC3256 | HR CC3256 | 2676 |
| 3257 | CC3257 | Engineering CC3257 | 1258 |
| 3258 | CC3258 | Marketing CC3258 | 835 |
| 3259 | CC3259 | Analytics CC3259 | 466 |
| 3260 | CC3260 | Support CC3260 | 3730 |
| 3261 | CC3261 | Logistics CC3261 | 3793 |
| 3262 | CC3262 | Finance CC3262 | 82 |
| 3263 | CC3263 | HR CC3263 | 3299 |
| 3264 | CC3264 | Treasury CC3264 | 3825 |
| 3265 | CC3265 | Legal CC3265 | 398 |
| 3266 | CC3266 | Compliance CC3266 | 3143 |
| 3267 | CC3267 | Engineering CC3267 | 1218 |
| 3268 | CC3268 | Executive CC3268 | 286 |
| 3269 | CC3269 | Operations CC3269 | 2550 |
| 3270 | CC3270 | Legal CC3270 | 3188 |
| 3271 | CC3271 | Sales CC3271 | 3732 |
| 3272 | CC3272 | R&D CC3272 | 2125 |
| 3273 | CC3273 | Quality CC3273 | 1458 |
| 3274 | CC3274 | R&D CC3274 | 2460 |
| 3275 | CC3275 | Quality CC3275 | 2263 |
| 3276 | CC3276 | Sales CC3276 | 3902 |
| 3277 | CC3277 | Compliance CC3277 | 1821 |
| 3278 | CC3278 | Audit CC3278 | 1641 |
| 3279 | CC3279 | Analytics CC3279 | 731 |
| 3280 | CC3280 | Strategy CC3280 | 1988 |
| 3281 | CC3281 | Marketing CC3281 | 3850 |
| 3282 | CC3282 | Engineering CC3282 | 1024 |
| 3283 | CC3283 | Operations CC3283 | 1615 |
| 3284 | CC3284 | Finance CC3284 | 1690 |
| 3285 | CC3285 | Quality CC3285 | 3514 |
| 3286 | CC3286 | HR CC3286 | 1554 |
| 3287 | CC3287 | Procurement CC3287 | 1464 |
| 3288 | CC3288 | Compliance CC3288 | 62 |
| 3289 | CC3289 | R&D CC3289 | 3378 |
| 3290 | CC3290 | Support CC3290 | 1691 |
| 3291 | CC3291 | Procurement CC3291 | 484 |
| 3292 | CC3292 | Strategy CC3292 | 2751 |
| 3293 | CC3293 | Sales CC3293 | 964 |
| 3294 | CC3294 | Finance CC3294 | 535 |
| 3295 | CC3295 | Quality CC3295 | 1216 |
| 3296 | CC3296 | Marketing CC3296 | 1763 |
| 3297 | CC3297 | Quality CC3297 | 2472 |
| 3298 | CC3298 | Engineering CC3298 | 1037 |
| 3299 | CC3299 | IT CC3299 | 3486 |
| 3300 | CC3300 | Operations CC3300 | 3546 |
| 3301 | CC3301 | Audit CC3301 | 3730 |
| 3302 | CC3302 | Audit CC3302 | 3897 |
| 3303 | CC3303 | Risk CC3303 | 2953 |
| 3304 | CC3304 | Legal CC3304 | 229 |
| 3305 | CC3305 | Marketing CC3305 | 1612 |
| 3306 | CC3306 | Support CC3306 | 736 |
| 3307 | CC3307 | Support CC3307 | 2846 |
| 3308 | CC3308 | Logistics CC3308 | 1497 |
| 3309 | CC3309 | Legal CC3309 | 3180 |
| 3310 | CC3310 | Quality CC3310 | 2573 |
| 3311 | CC3311 | Finance CC3311 | 137 |
| 3312 | CC3312 | Treasury CC3312 | 2890 |
| 3313 | CC3313 | R&D CC3313 | 3100 |
| 3314 | CC3314 | Legal CC3314 | 1386 |
| 3315 | CC3315 | HR CC3315 | 1923 |
| 3316 | CC3316 | Operations CC3316 | 1211 |
| 3317 | CC3317 | Legal CC3317 | 2339 |
| 3318 | CC3318 | Quality CC3318 | 3282 |
| 3319 | CC3319 | Sales CC3319 | 384 |
| 3320 | CC3320 | Procurement CC3320 | 871 |
| 3321 | CC3321 | Logistics CC3321 | 2550 |
| 3322 | CC3322 | Audit CC3322 | 1667 |
| 3323 | CC3323 | Operations CC3323 | 1643 |
| 3324 | CC3324 | HR CC3324 | 3286 |
| 3325 | CC3325 | Operations CC3325 | 14 |
| 3326 | CC3326 | Procurement CC3326 | 3691 |
| 3327 | CC3327 | R&D CC3327 | 856 |
| 3328 | CC3328 | Legal CC3328 | 3408 |
| 3329 | CC3329 | Compliance CC3329 | 1202 |
| 3330 | CC3330 | Compliance CC3330 | 506 |
| 3331 | CC3331 | HR CC3331 | 966 |
| 3332 | CC3332 | Marketing CC3332 | 3340 |
| 3333 | CC3333 | Finance CC3333 | 3054 |
| 3334 | CC3334 | HR CC3334 | 30 |
| 3335 | CC3335 | HR CC3335 | 388 |
| 3336 | CC3336 | Support CC3336 | 268 |
| 3337 | CC3337 | Strategy CC3337 | 1295 |
| 3338 | CC3338 | HR CC3338 | 3995 |
| 3339 | CC3339 | Sales CC3339 | 1755 |
| 3340 | CC3340 | HR CC3340 | 3549 |
| 3341 | CC3341 | R&D CC3341 | 2157 |
| 3342 | CC3342 | Support CC3342 | 2914 |
| 3343 | CC3343 | Analytics CC3343 | 3087 |
| 3344 | CC3344 | Strategy CC3344 | 3086 |
| 3345 | CC3345 | Analytics CC3345 | 1186 |
| 3346 | CC3346 | HR CC3346 | 1935 |
| 3347 | CC3347 | Compliance CC3347 | 2685 |
| 3348 | CC3348 | Sales CC3348 | 760 |
| 3349 | CC3349 | Strategy CC3349 | 3009 |
| 3350 | CC3350 | Strategy CC3350 | 1764 |
| 3351 | CC3351 | Executive CC3351 | 1666 |
| 3352 | CC3352 | Sales CC3352 | 1942 |
| 3353 | CC3353 | Treasury CC3353 | 439 |
| 3354 | CC3354 | IT CC3354 | 3533 |
| 3355 | CC3355 | Quality CC3355 | 716 |
| 3356 | CC3356 | Strategy CC3356 | 2348 |
| 3357 | CC3357 | Risk CC3357 | 2561 |
| 3358 | CC3358 | Compliance CC3358 | 1117 |
| 3359 | CC3359 | Sales CC3359 | 27 |
| 3360 | CC3360 | Risk CC3360 | 2416 |
| 3361 | CC3361 | R&D CC3361 | 179 |
| 3362 | CC3362 | Logistics CC3362 | 1409 |
| 3363 | CC3363 | R&D CC3363 | 2039 |
| 3364 | CC3364 | Marketing CC3364 | 2944 |
| 3365 | CC3365 | Analytics CC3365 | 3621 |
| 3366 | CC3366 | R&D CC3366 | 1649 |
| 3367 | CC3367 | Analytics CC3367 | 95 |
| 3368 | CC3368 | Finance CC3368 | 3266 |
| 3369 | CC3369 | Logistics CC3369 | 3977 |
| 3370 | CC3370 | Compliance CC3370 | 1999 |
| 3371 | CC3371 | IT CC3371 | 527 |
| 3372 | CC3372 | Operations CC3372 | 3698 |
| 3373 | CC3373 | R&D CC3373 | 1292 |
| 3374 | CC3374 | Sales CC3374 | 2264 |
| 3375 | CC3375 | Quality CC3375 | 1563 |
| 3376 | CC3376 | Audit CC3376 | 2384 |
| 3377 | CC3377 | Analytics CC3377 | 2861 |
| 3378 | CC3378 | Audit CC3378 | 3694 |
| 3379 | CC3379 | Finance CC3379 | 2706 |
| 3380 | CC3380 | Sales CC3380 | 3860 |
| 3381 | CC3381 | Audit CC3381 | 2007 |
| 3382 | CC3382 | Treasury CC3382 | 1099 |
| 3383 | CC3383 | Finance CC3383 | 1530 |
| 3384 | CC3384 | Analytics CC3384 | 616 |
| 3385 | CC3385 | HR CC3385 | 3293 |
| 3386 | CC3386 | Support CC3386 | 3609 |
| 3387 | CC3387 | Treasury CC3387 | 3890 |
| 3388 | CC3388 | Support CC3388 | 2924 |
| 3389 | CC3389 | Procurement CC3389 | 1928 |
| 3390 | CC3390 | Compliance CC3390 | 316 |
| 3391 | CC3391 | Legal CC3391 | 1437 |
| 3392 | CC3392 | Executive CC3392 | 1826 |
| 3393 | CC3393 | Operations CC3393 | 1051 |
| 3394 | CC3394 | Strategy CC3394 | 1943 |
| 3395 | CC3395 | Procurement CC3395 | 34 |
| 3396 | CC3396 | Risk CC3396 | 2742 |
| 3397 | CC3397 | Analytics CC3397 | 1374 |
| 3398 | CC3398 | Engineering CC3398 | 1082 |
| 3399 | CC3399 | Logistics CC3399 | 1903 |
| 3400 | CC3400 | Finance CC3400 | 2062 |
| 3401 | CC3401 | Compliance CC3401 | 1970 |
| 3402 | CC3402 | Logistics CC3402 | 3947 |
| 3403 | CC3403 | Sales CC3403 | 1827 |
| 3404 | CC3404 | Engineering CC3404 | 870 |
| 3405 | CC3405 | Procurement CC3405 | 1910 |
| 3406 | CC3406 | Strategy CC3406 | 3098 |
| 3407 | CC3407 | R&D CC3407 | 3783 |
| 3408 | CC3408 | Risk CC3408 | 844 |
| 3409 | CC3409 | Treasury CC3409 | 1018 |
| 3410 | CC3410 | Operations CC3410 | 1653 |
| 3411 | CC3411 | Marketing CC3411 | 1415 |
| 3412 | CC3412 | HR CC3412 | 235 |
| 3413 | CC3413 | HR CC3413 | 3912 |
| 3414 | CC3414 | Support CC3414 | 541 |
| 3415 | CC3415 | Logistics CC3415 | 1522 |
| 3416 | CC3416 | IT CC3416 | 1960 |
| 3417 | CC3417 | Finance CC3417 | 706 |
| 3418 | CC3418 | Engineering CC3418 | 1696 |
| 3419 | CC3419 | Logistics CC3419 | 32 |
| 3420 | CC3420 | Risk CC3420 | 3264 |
| 3421 | CC3421 | Analytics CC3421 | 1356 |
| 3422 | CC3422 | Finance CC3422 | 3552 |
| 3423 | CC3423 | Procurement CC3423 | 99 |
| 3424 | CC3424 | Treasury CC3424 | 3764 |
| 3425 | CC3425 | Legal CC3425 | 2208 |
| 3426 | CC3426 | Procurement CC3426 | 3767 |
| 3427 | CC3427 | Risk CC3427 | 57 |
| 3428 | CC3428 | Support CC3428 | 2898 |
| 3429 | CC3429 | Legal CC3429 | 776 |
| 3430 | CC3430 | Legal CC3430 | 3458 |
| 3431 | CC3431 | Logistics CC3431 | 409 |
| 3432 | CC3432 | Analytics CC3432 | 2438 |
| 3433 | CC3433 | Marketing CC3433 | 1483 |
| 3434 | CC3434 | Audit CC3434 | 1818 |
| 3435 | CC3435 | R&D CC3435 | 3595 |
| 3436 | CC3436 | Logistics CC3436 | 2195 |
| 3437 | CC3437 | Finance CC3437 | 2396 |
| 3438 | CC3438 | Logistics CC3438 | 3952 |
| 3439 | CC3439 | Finance CC3439 | 3959 |
| 3440 | CC3440 | HR CC3440 | 2202 |
| 3441 | CC3441 | Support CC3441 | 485 |
| 3442 | CC3442 | Sales CC3442 | 541 |
| 3443 | CC3443 | Sales CC3443 | 3506 |
| 3444 | CC3444 | R&D CC3444 | 583 |
| 3445 | CC3445 | Audit CC3445 | 566 |
| 3446 | CC3446 | Quality CC3446 | 1137 |
| 3447 | CC3447 | IT CC3447 | 2622 |
| 3448 | CC3448 | Treasury CC3448 | 729 |
| 3449 | CC3449 | Finance CC3449 | 111 |
| 3450 | CC3450 | Executive CC3450 | 2796 |
| 3451 | CC3451 | Quality CC3451 | 2709 |
| 3452 | CC3452 | Compliance CC3452 | 867 |
| 3453 | CC3453 | R&D CC3453 | 3418 |
| 3454 | CC3454 | Support CC3454 | 2774 |
| 3455 | CC3455 | Risk CC3455 | 2377 |
| 3456 | CC3456 | Compliance CC3456 | 1210 |
| 3457 | CC3457 | Legal CC3457 | 2424 |
| 3458 | CC3458 | Logistics CC3458 | 711 |
| 3459 | CC3459 | Risk CC3459 | 614 |
| 3460 | CC3460 | Logistics CC3460 | 128 |
| 3461 | CC3461 | Quality CC3461 | 3831 |
| 3462 | CC3462 | Analytics CC3462 | 3805 |
| 3463 | CC3463 | Marketing CC3463 | 1543 |
| 3464 | CC3464 | Audit CC3464 | 848 |
| 3465 | CC3465 | Treasury CC3465 | 2741 |
| 3466 | CC3466 | HR CC3466 | 1929 |
| 3467 | CC3467 | Procurement CC3467 | 1082 |
| 3468 | CC3468 | IT CC3468 | 3772 |
| 3469 | CC3469 | Analytics CC3469 | 2755 |
| 3470 | CC3470 | Compliance CC3470 | 2233 |
| 3471 | CC3471 | Engineering CC3471 | 2665 |
| 3472 | CC3472 | Executive CC3472 | 8 |
| 3473 | CC3473 | Audit CC3473 | 2851 |
| 3474 | CC3474 | Analytics CC3474 | 160 |
| 3475 | CC3475 | Risk CC3475 | 3729 |
| 3476 | CC3476 | HR CC3476 | 3448 |
| 3477 | CC3477 | Risk CC3477 | 3812 |
| 3478 | CC3478 | Logistics CC3478 | 2330 |
| 3479 | CC3479 | HR CC3479 | 638 |
| 3480 | CC3480 | Risk CC3480 | 2702 |
| 3481 | CC3481 | Legal CC3481 | 3558 |
| 3482 | CC3482 | Strategy CC3482 | 2711 |
| 3483 | CC3483 | Operations CC3483 | 3152 |
| 3484 | CC3484 | R&D CC3484 | 3916 |
| 3485 | CC3485 | Compliance CC3485 | 1475 |
| 3486 | CC3486 | R&D CC3486 | 3950 |
| 3487 | CC3487 | Operations CC3487 | 1107 |
| 3488 | CC3488 | Treasury CC3488 | 2764 |
| 3489 | CC3489 | Operations CC3489 | 1097 |
| 3490 | CC3490 | HR CC3490 | 2247 |
| 3491 | CC3491 | Treasury CC3491 | 717 |
| 3492 | CC3492 | Strategy CC3492 | 506 |
| 3493 | CC3493 | Support CC3493 | 1154 |
| 3494 | CC3494 | Marketing CC3494 | 3720 |
| 3495 | CC3495 | Engineering CC3495 | 1542 |
| 3496 | CC3496 | Strategy CC3496 | 235 |
| 3497 | CC3497 | Procurement CC3497 | 2725 |
| 3498 | CC3498 | Logistics CC3498 | 1664 |
| 3499 | CC3499 | Executive CC3499 | 3224 |
| 3500 | CC3500 | IT CC3500 | 88 |
| 3501 | CC3501 | Executive CC3501 | 2262 |
| 3502 | CC3502 | HR CC3502 | 3893 |
| 3503 | CC3503 | Support CC3503 | 3050 |
| 3504 | CC3504 | Support CC3504 | 1815 |
| 3505 | CC3505 | Analytics CC3505 | 2225 |
| 3506 | CC3506 | R&D CC3506 | 473 |
| 3507 | CC3507 | Engineering CC3507 | 760 |
| 3508 | CC3508 | R&D CC3508 | 770 |
| 3509 | CC3509 | Legal CC3509 | 3066 |
| 3510 | CC3510 | Procurement CC3510 | 2737 |
| 3511 | CC3511 | Strategy CC3511 | 2417 |
| 3512 | CC3512 | Strategy CC3512 | 2139 |
| 3513 | CC3513 | Operations CC3513 | 1979 |
| 3514 | CC3514 | HR CC3514 | 2589 |
| 3515 | CC3515 | Finance CC3515 | 553 |
| 3516 | CC3516 | Quality CC3516 | 1034 |
| 3517 | CC3517 | Analytics CC3517 | 3909 |
| 3518 | CC3518 | Treasury CC3518 | 1177 |
| 3519 | CC3519 | Executive CC3519 | 3953 |
| 3520 | CC3520 | Strategy CC3520 | 2766 |
| 3521 | CC3521 | Audit CC3521 | 3200 |
| 3522 | CC3522 | Audit CC3522 | 826 |
| 3523 | CC3523 | Sales CC3523 | 486 |
| 3524 | CC3524 | Risk CC3524 | 1761 |
| 3525 | CC3525 | Operations CC3525 | 1046 |
| 3526 | CC3526 | Operations CC3526 | 130 |
| 3527 | CC3527 | IT CC3527 | 3109 |
| 3528 | CC3528 | R&D CC3528 | 2644 |
| 3529 | CC3529 | Procurement CC3529 | 2146 |
| 3530 | CC3530 | Sales CC3530 | 1076 |
| 3531 | CC3531 | Strategy CC3531 | 2148 |
| 3532 | CC3532 | Audit CC3532 | 3107 |
| 3533 | CC3533 | Logistics CC3533 | 614 |
| 3534 | CC3534 | Analytics CC3534 | 1490 |
| 3535 | CC3535 | Engineering CC3535 | 3841 |
| 3536 | CC3536 | Support CC3536 | 3776 |
| 3537 | CC3537 | IT CC3537 | 3224 |
| 3538 | CC3538 | Legal CC3538 | 1406 |
| 3539 | CC3539 | R&D CC3539 | 612 |
| 3540 | CC3540 | IT CC3540 | 1703 |
| 3541 | CC3541 | Operations CC3541 | 2065 |
| 3542 | CC3542 | Analytics CC3542 | 312 |
| 3543 | CC3543 | Strategy CC3543 | 35 |
| 3544 | CC3544 | Compliance CC3544 | 3151 |
| 3545 | CC3545 | HR CC3545 | 881 |
| 3546 | CC3546 | Procurement CC3546 | 3520 |
| 3547 | CC3547 | Executive CC3547 | 1575 |
| 3548 | CC3548 | Engineering CC3548 | 2302 |
| 3549 | CC3549 | Procurement CC3549 | 2196 |
| 3550 | CC3550 | Logistics CC3550 | 1671 |
| 3551 | CC3551 | Operations CC3551 | 442 |
| 3552 | CC3552 | Marketing CC3552 | 1601 |
| 3553 | CC3553 | Executive CC3553 | 1598 |
| 3554 | CC3554 | Sales CC3554 | 3997 |
| 3555 | CC3555 | Procurement CC3555 | 2606 |
| 3556 | CC3556 | Finance CC3556 | 3586 |
| 3557 | CC3557 | Risk CC3557 | 2335 |
| 3558 | CC3558 | Operations CC3558 | 2423 |
| 3559 | CC3559 | Analytics CC3559 | 926 |
| 3560 | CC3560 | HR CC3560 | 2868 |
| 3561 | CC3561 | R&D CC3561 | 655 |
| 3562 | CC3562 | Engineering CC3562 | 12 |
| 3563 | CC3563 | HR CC3563 | 2998 |
| 3564 | CC3564 | Sales CC3564 | 203 |
| 3565 | CC3565 | IT CC3565 | 1162 |
| 3566 | CC3566 | Legal CC3566 | 1592 |
| 3567 | CC3567 | Logistics CC3567 | 762 |
| 3568 | CC3568 | Support CC3568 | 1787 |
| 3569 | CC3569 | Procurement CC3569 | 2575 |
| 3570 | CC3570 | Logistics CC3570 | 3674 |
| 3571 | CC3571 | Logistics CC3571 | 2551 |
| 3572 | CC3572 | Risk CC3572 | 3060 |
| 3573 | CC3573 | Engineering CC3573 | 1361 |
| 3574 | CC3574 | Operations CC3574 | 2894 |
| 3575 | CC3575 | IT CC3575 | 2441 |
| 3576 | CC3576 | Engineering CC3576 | 2747 |
| 3577 | CC3577 | Strategy CC3577 | 2851 |
| 3578 | CC3578 | R&D CC3578 | 2061 |
| 3579 | CC3579 | Marketing CC3579 | 487 |
| 3580 | CC3580 | Procurement CC3580 | 1538 |
| 3581 | CC3581 | HR CC3581 | 1809 |
| 3582 | CC3582 | Strategy CC3582 | 3729 |
| 3583 | CC3583 | Operations CC3583 | 3883 |
| 3584 | CC3584 | Sales CC3584 | 3294 |
| 3585 | CC3585 | Finance CC3585 | 792 |
| 3586 | CC3586 | IT CC3586 | 3493 |
| 3587 | CC3587 | Risk CC3587 | 384 |
| 3588 | CC3588 | R&D CC3588 | 3832 |
| 3589 | CC3589 | Executive CC3589 | 3882 |
| 3590 | CC3590 | Compliance CC3590 | 2554 |
| 3591 | CC3591 | Risk CC3591 | 2572 |
| 3592 | CC3592 | Procurement CC3592 | 2363 |
| 3593 | CC3593 | Sales CC3593 | 2168 |
| 3594 | CC3594 | IT CC3594 | 1167 |
| 3595 | CC3595 | Engineering CC3595 | 1892 |
| 3596 | CC3596 | R&D CC3596 | 2001 |
| 3597 | CC3597 | Analytics CC3597 | 461 |
| 3598 | CC3598 | IT CC3598 | 1196 |
| 3599 | CC3599 | Audit CC3599 | 1457 |
| 3600 | CC3600 | Audit CC3600 | 2421 |
| 3601 | CC3601 | Analytics CC3601 | 2282 |
| 3602 | CC3602 | Executive CC3602 | 3935 |
| 3603 | CC3603 | Treasury CC3603 | 3058 |
| 3604 | CC3604 | Support CC3604 | 2305 |
| 3605 | CC3605 | R&D CC3605 | 3174 |
| 3606 | CC3606 | IT CC3606 | 2026 |
| 3607 | CC3607 | Marketing CC3607 | 549 |
| 3608 | CC3608 | Support CC3608 | 984 |
| 3609 | CC3609 | Operations CC3609 | 691 |
| 3610 | CC3610 | IT CC3610 | 2664 |
| 3611 | CC3611 | Legal CC3611 | 3639 |
| 3612 | CC3612 | Logistics CC3612 | 3337 |
| 3613 | CC3613 | Quality CC3613 | 873 |
| 3614 | CC3614 | IT CC3614 | 772 |
| 3615 | CC3615 | Procurement CC3615 | 714 |
| 3616 | CC3616 | Procurement CC3616 | 3167 |
| 3617 | CC3617 | Operations CC3617 | 2309 |
| 3618 | CC3618 | Operations CC3618 | 3455 |
| 3619 | CC3619 | Risk CC3619 | 1318 |
| 3620 | CC3620 | Operations CC3620 | 3980 |
| 3621 | CC3621 | HR CC3621 | 3769 |
| 3622 | CC3622 | IT CC3622 | 2055 |
| 3623 | CC3623 | Marketing CC3623 | 169 |
| 3624 | CC3624 | Support CC3624 | 1056 |
| 3625 | CC3625 | Support CC3625 | 3547 |
| 3626 | CC3626 | Legal CC3626 | 3644 |
| 3627 | CC3627 | Operations CC3627 | 931 |
| 3628 | CC3628 | Audit CC3628 | 3167 |
| 3629 | CC3629 | Legal CC3629 | 374 |
| 3630 | CC3630 | Engineering CC3630 | 979 |
| 3631 | CC3631 | Sales CC3631 | 533 |
| 3632 | CC3632 | Marketing CC3632 | 2683 |
| 3633 | CC3633 | Treasury CC3633 | 3432 |
| 3634 | CC3634 | Audit CC3634 | 549 |
| 3635 | CC3635 | Audit CC3635 | 3933 |
| 3636 | CC3636 | Logistics CC3636 | 143 |
| 3637 | CC3637 | Finance CC3637 | 1732 |
| 3638 | CC3638 | Strategy CC3638 | 3998 |
| 3639 | CC3639 | Strategy CC3639 | 784 |
| 3640 | CC3640 | Logistics CC3640 | 973 |
| 3641 | CC3641 | R&D CC3641 | 2340 |
| 3642 | CC3642 | IT CC3642 | 3321 |
| 3643 | CC3643 | Legal CC3643 | 3466 |
| 3644 | CC3644 | Audit CC3644 | 3692 |
| 3645 | CC3645 | Engineering CC3645 | 2266 |
| 3646 | CC3646 | Logistics CC3646 | 496 |
| 3647 | CC3647 | Engineering CC3647 | 356 |
| 3648 | CC3648 | Marketing CC3648 | 2225 |
| 3649 | CC3649 | Procurement CC3649 | 3426 |
| 3650 | CC3650 | Quality CC3650 | 3486 |
| 3651 | CC3651 | Operations CC3651 | 3178 |
| 3652 | CC3652 | Procurement CC3652 | 388 |
| 3653 | CC3653 | Marketing CC3653 | 1007 |
| 3654 | CC3654 | HR CC3654 | 972 |
| 3655 | CC3655 | Strategy CC3655 | 270 |
| 3656 | CC3656 | Engineering CC3656 | 3006 |
| 3657 | CC3657 | Audit CC3657 | 825 |
| 3658 | CC3658 | Marketing CC3658 | 450 |
| 3659 | CC3659 | Strategy CC3659 | 3788 |
| 3660 | CC3660 | Strategy CC3660 | 3108 |
| 3661 | CC3661 | Operations CC3661 | 2573 |
| 3662 | CC3662 | Marketing CC3662 | 1382 |
| 3663 | CC3663 | Treasury CC3663 | 246 |
| 3664 | CC3664 | Marketing CC3664 | 3113 |
| 3665 | CC3665 | Risk CC3665 | 81 |
| 3666 | CC3666 | Treasury CC3666 | 2747 |
| 3667 | CC3667 | Marketing CC3667 | 2804 |
| 3668 | CC3668 | R&D CC3668 | 3388 |
| 3669 | CC3669 | Marketing CC3669 | 1463 |
| 3670 | CC3670 | Treasury CC3670 | 3013 |
| 3671 | CC3671 | IT CC3671 | 2694 |
| 3672 | CC3672 | Finance CC3672 | 3414 |
| 3673 | CC3673 | Procurement CC3673 | 3481 |
| 3674 | CC3674 | Finance CC3674 | 1077 |
| 3675 | CC3675 | HR CC3675 | 1529 |
| 3676 | CC3676 | IT CC3676 | 3375 |
| 3677 | CC3677 | Procurement CC3677 | 1867 |
| 3678 | CC3678 | Support CC3678 | 2829 |
| 3679 | CC3679 | Risk CC3679 | 2440 |
| 3680 | CC3680 | Quality CC3680 | 1848 |
| 3681 | CC3681 | Compliance CC3681 | 1721 |
| 3682 | CC3682 | Operations CC3682 | 2098 |
| 3683 | CC3683 | HR CC3683 | 1249 |
| 3684 | CC3684 | Compliance CC3684 | 2011 |
| 3685 | CC3685 | Engineering CC3685 | 3805 |
| 3686 | CC3686 | Operations CC3686 | 3443 |
| 3687 | CC3687 | Strategy CC3687 | 472 |
| 3688 | CC3688 | Treasury CC3688 | 871 |
| 3689 | CC3689 | Sales CC3689 | 1417 |
| 3690 | CC3690 | Treasury CC3690 | 3299 |
| 3691 | CC3691 | Operations CC3691 | 1421 |
| 3692 | CC3692 | Finance CC3692 | 1854 |
| 3693 | CC3693 | Legal CC3693 | 2190 |
| 3694 | CC3694 | Quality CC3694 | 2318 |
| 3695 | CC3695 | Finance CC3695 | 3905 |
| 3696 | CC3696 | Operations CC3696 | 2143 |
| 3697 | CC3697 | Engineering CC3697 | 3652 |
| 3698 | CC3698 | Procurement CC3698 | 2810 |
| 3699 | CC3699 | Analytics CC3699 | 3655 |
| 3700 | CC3700 | IT CC3700 | 258 |
| 3701 | CC3701 | Operations CC3701 | 231 |
| 3702 | CC3702 | Procurement CC3702 | 720 |
| 3703 | CC3703 | Risk CC3703 | 18 |
| 3704 | CC3704 | Risk CC3704 | 2058 |
| 3705 | CC3705 | Analytics CC3705 | 3273 |
| 3706 | CC3706 | Marketing CC3706 | 3706 |
| 3707 | CC3707 | R&D CC3707 | 2931 |
| 3708 | CC3708 | R&D CC3708 | 3732 |
| 3709 | CC3709 | Audit CC3709 | 601 |
| 3710 | CC3710 | Support CC3710 | 2813 |
| 3711 | CC3711 | Treasury CC3711 | 1556 |
| 3712 | CC3712 | Support CC3712 | 325 |
| 3713 | CC3713 | Quality CC3713 | 3036 |
| 3714 | CC3714 | Quality CC3714 | 3928 |
| 3715 | CC3715 | Sales CC3715 | 1706 |
| 3716 | CC3716 | Executive CC3716 | 632 |
| 3717 | CC3717 | IT CC3717 | 1854 |
| 3718 | CC3718 | Engineering CC3718 | 1876 |
| 3719 | CC3719 | Legal CC3719 | 1012 |
| 3720 | CC3720 | Compliance CC3720 | 3350 |
| 3721 | CC3721 | Risk CC3721 | 1906 |
| 3722 | CC3722 | Sales CC3722 | 2343 |
| 3723 | CC3723 | Compliance CC3723 | 1550 |
| 3724 | CC3724 | Engineering CC3724 | 1491 |
| 3725 | CC3725 | Operations CC3725 | 2405 |
| 3726 | CC3726 | Procurement CC3726 | 2980 |
| 3727 | CC3727 | Audit CC3727 | 1002 |
| 3728 | CC3728 | Marketing CC3728 | 215 |
| 3729 | CC3729 | Treasury CC3729 | 2852 |
| 3730 | CC3730 | Support CC3730 | 831 |
| 3731 | CC3731 | Finance CC3731 | 2315 |
| 3732 | CC3732 | R&D CC3732 | 2723 |
| 3733 | CC3733 | IT CC3733 | 1722 |
| 3734 | CC3734 | Audit CC3734 | 3857 |
| 3735 | CC3735 | Support CC3735 | 14 |
| 3736 | CC3736 | HR CC3736 | 2434 |
| 3737 | CC3737 | Support CC3737 | 1125 |
| 3738 | CC3738 | Support CC3738 | 3704 |
| 3739 | CC3739 | Quality CC3739 | 3205 |
| 3740 | CC3740 | Operations CC3740 | 2307 |
| 3741 | CC3741 | HR CC3741 | 344 |
| 3742 | CC3742 | Support CC3742 | 3597 |
| 3743 | CC3743 | Executive CC3743 | 2747 |
| 3744 | CC3744 | IT CC3744 | 1219 |
| 3745 | CC3745 | Compliance CC3745 | 1315 |
| 3746 | CC3746 | Quality CC3746 | 3230 |
| 3747 | CC3747 | Sales CC3747 | 1531 |
| 3748 | CC3748 | Support CC3748 | 1990 |
| 3749 | CC3749 | Compliance CC3749 | 331 |
| 3750 | CC3750 | Audit CC3750 | 3144 |
| 3751 | CC3751 | Sales CC3751 | 72 |
| 3752 | CC3752 | Procurement CC3752 | 3526 |
| 3753 | CC3753 | Quality CC3753 | 2772 |
| 3754 | CC3754 | Quality CC3754 | 2016 |
| 3755 | CC3755 | Finance CC3755 | 1247 |
| 3756 | CC3756 | HR CC3756 | 2525 |
| 3757 | CC3757 | Quality CC3757 | 3406 |
| 3758 | CC3758 | Logistics CC3758 | 40 |
| 3759 | CC3759 | Risk CC3759 | 1221 |
| 3760 | CC3760 | Support CC3760 | 3651 |
| 3761 | CC3761 | Analytics CC3761 | 1303 |
| 3762 | CC3762 | Procurement CC3762 | 3832 |
| 3763 | CC3763 | HR CC3763 | 2352 |
| 3764 | CC3764 | Engineering CC3764 | 433 |
| 3765 | CC3765 | Strategy CC3765 | 2686 |
| 3766 | CC3766 | Compliance CC3766 | 1560 |
| 3767 | CC3767 | Treasury CC3767 | 1556 |
| 3768 | CC3768 | Marketing CC3768 | 1627 |
| 3769 | CC3769 | Support CC3769 | 3757 |
| 3770 | CC3770 | Analytics CC3770 | 176 |
| 3771 | CC3771 | Procurement CC3771 | 2572 |
| 3772 | CC3772 | HR CC3772 | 1904 |
| 3773 | CC3773 | Treasury CC3773 | 2025 |
| 3774 | CC3774 | IT CC3774 | 2737 |
| 3775 | CC3775 | Operations CC3775 | 985 |
| 3776 | CC3776 | Procurement CC3776 | 1523 |
| 3777 | CC3777 | HR CC3777 | 118 |
| 3778 | CC3778 | R&D CC3778 | 3358 |
| 3779 | CC3779 | Engineering CC3779 | 3741 |
| 3780 | CC3780 | Support CC3780 | 478 |
| 3781 | CC3781 | Legal CC3781 | 1108 |
| 3782 | CC3782 | Treasury CC3782 | 161 |
| 3783 | CC3783 | Legal CC3783 | 714 |
| 3784 | CC3784 | Compliance CC3784 | 808 |
| 3785 | CC3785 | Support CC3785 | 370 |
| 3786 | CC3786 | Risk CC3786 | 581 |
| 3787 | CC3787 | Finance CC3787 | 2178 |
| 3788 | CC3788 | Support CC3788 | 884 |
| 3789 | CC3789 | Support CC3789 | 546 |
| 3790 | CC3790 | Support CC3790 | 3229 |
| 3791 | CC3791 | Procurement CC3791 | 1727 |
| 3792 | CC3792 | Analytics CC3792 | 54 |
| 3793 | CC3793 | Engineering CC3793 | 429 |
| 3794 | CC3794 | Finance CC3794 | 16 |
| 3795 | CC3795 | Quality CC3795 | 983 |
| 3796 | CC3796 | Audit CC3796 | 988 |
| 3797 | CC3797 | Strategy CC3797 | 3311 |
| 3798 | CC3798 | Compliance CC3798 | 308 |
| 3799 | CC3799 | Support CC3799 | 1424 |
| 3800 | CC3800 | Risk CC3800 | 1279 |
| 3801 | CC3801 | Finance CC3801 | 3474 |
| 3802 | CC3802 | Sales CC3802 | 2414 |
| 3803 | CC3803 | Quality CC3803 | 1704 |
| 3804 | CC3804 | Finance CC3804 | 965 |
| 3805 | CC3805 | Strategy CC3805 | 690 |
| 3806 | CC3806 | IT CC3806 | 3690 |
| 3807 | CC3807 | Compliance CC3807 | 900 |
| 3808 | CC3808 | Executive CC3808 | 2537 |
| 3809 | CC3809 | Support CC3809 | 1520 |
| 3810 | CC3810 | R&D CC3810 | 38 |
| 3811 | CC3811 | Strategy CC3811 | 1949 |
| 3812 | CC3812 | Audit CC3812 | 1889 |
| 3813 | CC3813 | Risk CC3813 | 3664 |
| 3814 | CC3814 | Sales CC3814 | 1424 |
| 3815 | CC3815 | Treasury CC3815 | 3880 |
| 3816 | CC3816 | Analytics CC3816 | 1835 |
| 3817 | CC3817 | Analytics CC3817 | 1262 |
| 3818 | CC3818 | Analytics CC3818 | 386 |
| 3819 | CC3819 | Legal CC3819 | 580 |
| 3820 | CC3820 | Audit CC3820 | 2017 |
| 3821 | CC3821 | Treasury CC3821 | 2496 |
| 3822 | CC3822 | HR CC3822 | 1744 |
| 3823 | CC3823 | Operations CC3823 | 80 |
| 3824 | CC3824 | Quality CC3824 | 1968 |
| 3825 | CC3825 | Operations CC3825 | 3828 |
| 3826 | CC3826 | Logistics CC3826 | 3936 |
| 3827 | CC3827 | Analytics CC3827 | 217 |
| 3828 | CC3828 | Executive CC3828 | 3464 |
| 3829 | CC3829 | Sales CC3829 | 2542 |
| 3830 | CC3830 | Engineering CC3830 | 2339 |
| 3831 | CC3831 | Executive CC3831 | 964 |
| 3832 | CC3832 | Executive CC3832 | 651 |
| 3833 | CC3833 | Quality CC3833 | 497 |
| 3834 | CC3834 | Sales CC3834 | 568 |
| 3835 | CC3835 | Procurement CC3835 | 1036 |
| 3836 | CC3836 | IT CC3836 | 3507 |
| 3837 | CC3837 | Operations CC3837 | 2614 |
| 3838 | CC3838 | Risk CC3838 | 568 |
| 3839 | CC3839 | Support CC3839 | 1991 |
| 3840 | CC3840 | Marketing CC3840 | 553 |
| 3841 | CC3841 | Engineering CC3841 | 198 |
| 3842 | CC3842 | Treasury CC3842 | 414 |
| 3843 | CC3843 | Risk CC3843 | 1322 |
| 3844 | CC3844 | Treasury CC3844 | 1446 |
| 3845 | CC3845 | Treasury CC3845 | 485 |
| 3846 | CC3846 | Quality CC3846 | 1123 |
| 3847 | CC3847 | R&D CC3847 | 3158 |
| 3848 | CC3848 | Strategy CC3848 | 2130 |
| 3849 | CC3849 | Legal CC3849 | 3737 |
| 3850 | CC3850 | Finance CC3850 | 3646 |
| 3851 | CC3851 | Compliance CC3851 | 2541 |
| 3852 | CC3852 | Procurement CC3852 | 83 |
| 3853 | CC3853 | HR CC3853 | 3793 |
| 3854 | CC3854 | Analytics CC3854 | 1452 |
| 3855 | CC3855 | Executive CC3855 | 3794 |
| 3856 | CC3856 | Procurement CC3856 | 338 |
| 3857 | CC3857 | Support CC3857 | 2517 |
| 3858 | CC3858 | Treasury CC3858 | 2327 |
| 3859 | CC3859 | Engineering CC3859 | 3375 |
| 3860 | CC3860 | Treasury CC3860 | 3419 |
| 3861 | CC3861 | Executive CC3861 | 3862 |
| 3862 | CC3862 | Procurement CC3862 | 1389 |
| 3863 | CC3863 | Marketing CC3863 | 3656 |
| 3864 | CC3864 | Strategy CC3864 | 1789 |
| 3865 | CC3865 | Analytics CC3865 | 3543 |
| 3866 | CC3866 | Risk CC3866 | 1941 |
| 3867 | CC3867 | R&D CC3867 | 322 |
| 3868 | CC3868 | Strategy CC3868 | 1111 |
| 3869 | CC3869 | IT CC3869 | 829 |
| 3870 | CC3870 | HR CC3870 | 1951 |
| 3871 | CC3871 | Quality CC3871 | 3479 |
| 3872 | CC3872 | Operations CC3872 | 1133 |
| 3873 | CC3873 | Executive CC3873 | 3287 |
| 3874 | CC3874 | R&D CC3874 | 257 |
| 3875 | CC3875 | Treasury CC3875 | 496 |
| 3876 | CC3876 | R&D CC3876 | 1439 |
| 3877 | CC3877 | Compliance CC3877 | 97 |
| 3878 | CC3878 | Compliance CC3878 | 3295 |
| 3879 | CC3879 | Operations CC3879 | 3289 |
| 3880 | CC3880 | Logistics CC3880 | 1393 |
| 3881 | CC3881 | Finance CC3881 | 2920 |
| 3882 | CC3882 | Legal CC3882 | 2682 |
| 3883 | CC3883 | Treasury CC3883 | 3109 |
| 3884 | CC3884 | Analytics CC3884 | 3162 |
| 3885 | CC3885 | Logistics CC3885 | 453 |
| 3886 | CC3886 | Engineering CC3886 | 3938 |
| 3887 | CC3887 | Treasury CC3887 | 3748 |
| 3888 | CC3888 | Finance CC3888 | 1696 |
| 3889 | CC3889 | R&D CC3889 | 3805 |
| 3890 | CC3890 | Operations CC3890 | 478 |
| 3891 | CC3891 | Compliance CC3891 | 995 |
| 3892 | CC3892 | Legal CC3892 | 634 |
| 3893 | CC3893 | Sales CC3893 | 2633 |
| 3894 | CC3894 | Analytics CC3894 | 3898 |
| 3895 | CC3895 | Audit CC3895 | 60 |
| 3896 | CC3896 | Quality CC3896 | 32 |
| 3897 | CC3897 | Executive CC3897 | 2611 |
| 3898 | CC3898 | Marketing CC3898 | 1700 |
| 3899 | CC3899 | Risk CC3899 | 2817 |
| 3900 | CC3900 | Risk CC3900 | 1341 |
| 3901 | CC3901 | Legal CC3901 | 3186 |
| 3902 | CC3902 | Procurement CC3902 | 184 |
| 3903 | CC3903 | IT CC3903 | 2060 |
| 3904 | CC3904 | R&D CC3904 | 2242 |
| 3905 | CC3905 | IT CC3905 | 1688 |
| 3906 | CC3906 | Strategy CC3906 | 2924 |
| 3907 | CC3907 | Audit CC3907 | 1091 |
| 3908 | CC3908 | Compliance CC3908 | 2463 |
| 3909 | CC3909 | Compliance CC3909 | 3476 |
| 3910 | CC3910 | Logistics CC3910 | 3305 |
| 3911 | CC3911 | Sales CC3911 | 903 |
| 3912 | CC3912 | Sales CC3912 | 2378 |
| 3913 | CC3913 | Marketing CC3913 | 2976 |
| 3914 | CC3914 | Executive CC3914 | 1908 |
| 3915 | CC3915 | Marketing CC3915 | 2940 |
| 3916 | CC3916 | Finance CC3916 | 2639 |
| 3917 | CC3917 | Compliance CC3917 | 1779 |
| 3918 | CC3918 | Executive CC3918 | 1744 |
| 3919 | CC3919 | Engineering CC3919 | 2199 |
| 3920 | CC3920 | Operations CC3920 | 1268 |
| 3921 | CC3921 | Procurement CC3921 | 3936 |
| 3922 | CC3922 | Finance CC3922 | 612 |
| 3923 | CC3923 | Executive CC3923 | 589 |
| 3924 | CC3924 | Operations CC3924 | 3757 |
| 3925 | CC3925 | HR CC3925 | 330 |
| 3926 | CC3926 | Marketing CC3926 | 2363 |
| 3927 | CC3927 | Quality CC3927 | 3365 |
| 3928 | CC3928 | Strategy CC3928 | 2130 |
| 3929 | CC3929 | Sales CC3929 | 989 |
| 3930 | CC3930 | Support CC3930 | 3832 |
| 3931 | CC3931 | Risk CC3931 | 1660 |
| 3932 | CC3932 | Analytics CC3932 | 2234 |
| 3933 | CC3933 | Marketing CC3933 | 1299 |
| 3934 | CC3934 | Legal CC3934 | 2046 |
| 3935 | CC3935 | Finance CC3935 | 3757 |
| 3936 | CC3936 | Compliance CC3936 | 3856 |
| 3937 | CC3937 | Audit CC3937 | 736 |
| 3938 | CC3938 | Audit CC3938 | 3997 |
| 3939 | CC3939 | Marketing CC3939 | 2515 |
| 3940 | CC3940 | Treasury CC3940 | 1954 |
| 3941 | CC3941 | IT CC3941 | 3907 |
| 3942 | CC3942 | Procurement CC3942 | 2126 |
| 3943 | CC3943 | HR CC3943 | 1478 |
| 3944 | CC3944 | Logistics CC3944 | 3474 |
| 3945 | CC3945 | Finance CC3945 | 3112 |
| 3946 | CC3946 | Legal CC3946 | 3241 |
| 3947 | CC3947 | Audit CC3947 | 3366 |
| 3948 | CC3948 | Executive CC3948 | 687 |
| 3949 | CC3949 | Strategy CC3949 | 1950 |
| 3950 | CC3950 | Support CC3950 | 3950 |
| 3951 | CC3951 | Strategy CC3951 | 713 |
| 3952 | CC3952 | Procurement CC3952 | 2303 |
| 3953 | CC3953 | Executive CC3953 | 3574 |
| 3954 | CC3954 | Audit CC3954 | 379 |
| 3955 | CC3955 | Sales CC3955 | 2286 |
| 3956 | CC3956 | IT CC3956 | 2265 |
| 3957 | CC3957 | Strategy CC3957 | 3338 |
| 3958 | CC3958 | Sales CC3958 | 1810 |
| 3959 | CC3959 | Finance CC3959 | 3568 |
| 3960 | CC3960 | Analytics CC3960 | 3459 |
| 3961 | CC3961 | Executive CC3961 | 1664 |
| 3962 | CC3962 | Treasury CC3962 | 2591 |
| 3963 | CC3963 | Executive CC3963 | 929 |
| 3964 | CC3964 | Compliance CC3964 | 2686 |
| 3965 | CC3965 | Treasury CC3965 | 2419 |
| 3966 | CC3966 | HR CC3966 | 2137 |
| 3967 | CC3967 | Legal CC3967 | 3180 |
| 3968 | CC3968 | IT CC3968 | 2947 |
| 3969 | CC3969 | HR CC3969 | 1834 |
| 3970 | CC3970 | Logistics CC3970 | 1953 |
| 3971 | CC3971 | Quality CC3971 | 2675 |
| 3972 | CC3972 | Marketing CC3972 | 1823 |
| 3973 | CC3973 | Support CC3973 | 3359 |
| 3974 | CC3974 | Sales CC3974 | 2825 |
| 3975 | CC3975 | Analytics CC3975 | 2879 |
| 3976 | CC3976 | Sales CC3976 | 3441 |
| 3977 | CC3977 | Legal CC3977 | 2905 |
| 3978 | CC3978 | Treasury CC3978 | 2063 |
| 3979 | CC3979 | Quality CC3979 | 3100 |
| 3980 | CC3980 | Legal CC3980 | 13 |
| 3981 | CC3981 | Sales CC3981 | 2977 |
| 3982 | CC3982 | HR CC3982 | 1734 |
| 3983 | CC3983 | Treasury CC3983 | 2637 |
| 3984 | CC3984 | Finance CC3984 | 1664 |
| 3985 | CC3985 | Quality CC3985 | 1854 |
| 3986 | CC3986 | Support CC3986 | 634 |
| 3987 | CC3987 | Operations CC3987 | 1574 |
| 3988 | CC3988 | Executive CC3988 | 721 |
| 3989 | CC3989 | IT CC3989 | 2683 |
| 3990 | CC3990 | Legal CC3990 | 3972 |
| 3991 | CC3991 | Finance CC3991 | 3197 |
| 3992 | CC3992 | Finance CC3992 | 1514 |
| 3993 | CC3993 | HR CC3993 | 1602 |
| 3994 | CC3994 | Quality CC3994 | 362 |
| 3995 | CC3995 | Engineering CC3995 | 1749 |
| 3996 | CC3996 | Compliance CC3996 | 1249 |
| 3997 | CC3997 | Treasury CC3997 | 3647 |
| 3998 | CC3998 | Logistics CC3998 | 945 |
| 3999 | CC3999 | Quality CC3999 | 1459 |
| 4000 | CC4000 | Compliance CC4000 | 3865 |

## Assignment Status Breakdown (hcm_assignments)

| Status | Count |
|---|---|
| ACTIVE | 3,980 |
| INACTIVE | 20 |

## Key Amount Ranges

- **fin_budget_lines.amount**: min=10,000.00, max=500,000.00, avg=251,283.50, count=4,000
- **fin_gl_balances.period_net**: min=50,000.00, max=450,000.00
- **fin_gl_balances.end_balance**: min=10,000.00, max=500,000.00
- **proc_po_headers.total_amount**: min=5,000.00, max=500,000.00, count=4,000
- **fin_ap_invoices.invoice_amount**: min=1,000.00, max=300,000.00, count=4,000

---

# SAMPLE DATA

## `hcm_persons` — sample rows

| person_id | person_number | first_name | last_name | date_of_birth | gender | nationality | national_id | marital_status | person_type | status | created_at | updated_at |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | EMP0001 | James | Okonkwo | NULL | M | British | NULL | NULL | EMPLOYEE | ACTIVE | 2026-03-02 18:28:58.686271 | 2026-03-02 18:28:58.686271 |
| 2 | EMP0002 | Sarah | Chen | NULL | M | British | NULL | NULL | EMPLOYEE | ACTIVE | 2026-03-02 18:28:58.686271 | 2026-03-02 18:28:58.686271 |
| 3 | EMP0003 | Priya | Sharma | NULL | F | British | NULL | NULL | EMPLOYEE | ACTIVE | 2026-03-02 18:28:58.686271 | 2026-03-02 18:28:58.686271 |
| 4 | EMP0004 | David | Williams | NULL | M | British | NULL | NULL | EMPLOYEE | ACTIVE | 2026-03-02 18:28:58.686271 | 2026-03-02 18:28:58.686271 |
| 5 | EMP0005 | Fatima | Al-Hassan | NULL | M | British | NULL | NULL | EMPLOYEE | ACTIVE | 2026-03-02 18:28:58.686271 | 2026-03-02 18:28:58.686271 |

## `hcm_assignments` — sample rows

| assignment_id | assignment_number | person_id | position_id | dept_id | org_id | grade_id | job_id | location_id | assignment_type | assignment_status | employment_status | job_title | salary | salary_currency | manager_person_id | effective_from | effective_to | created_at | updated_at |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | ASN0001 | 1 | NULL | 1 | 1 | 6 | NULL | 1 | PRIMARY | ACTIVE | ACTIVE | VP of Engineering | 118000.00 | GBP | NULL | 2019-03-15 | NULL | 2026-03-02 18:28:58.707966 | 2026-03-02 18:28:58.707966 |
| 2 | ASN0002 | 2 | NULL | 1 | 1 | 6 | NULL | 1 | PRIMARY | ACTIVE | ACTIVE | Engineering Director | 112000.00 | GBP | 1 | 2019-06-01 | NULL | 2026-03-02 18:28:58.707966 | 2026-03-02 18:28:58.707966 |
| 3 | ASN0003 | 3 | NULL | 1 | 1 | 5 | NULL | 1 | PRIMARY | ACTIVE | ACTIVE | Senior Staff Engineer | 102000.00 | GBP | 1 | 2019-09-12 | NULL | 2026-03-02 18:28:58.707966 | 2026-03-02 18:28:58.707966 |
| 4 | ASN0004 | 4 | NULL | 1 | 1 | 5 | NULL | 2 | PRIMARY | ACTIVE | ACTIVE | Staff Engineer | 96000.00 | GBP | 1 | 2020-01-20 | NULL | 2026-03-02 18:28:58.707966 | 2026-03-02 18:28:58.707966 |
| 5 | ASN0005 | 5 | NULL | 1 | 1 | 5 | NULL | 1 | PRIMARY | ACTIVE | ACTIVE | Staff Engineer | 94000.00 | GBP | 1 | 2020-03-10 | NULL | 2026-03-02 18:28:58.707966 | 2026-03-02 18:28:58.707966 |

## `hcm_departments` — sample rows

| dept_id | dept_code | dept_name | org_id | cost_centre_code | manager_person_id | status | created_at |
|---|---|---|---|---|---|---|---|
| 1 | D001 | Engineering | 1 | CC001 | NULL | ACTIVE | 2026-03-02 18:28:58.675948 |
| 2 | D002 | Finance | 1 | CC002 | NULL | ACTIVE | 2026-03-02 18:28:58.675948 |
| 3 | D003 | HR | 1 | CC004 | NULL | ACTIVE | 2026-03-02 18:28:58.675948 |
| 4 | D004 | Procurement | 1 | CC005 | NULL | ACTIVE | 2026-03-02 18:28:58.675948 |
| 5 | D005 | Marketing | 1 | CC003 | NULL | ACTIVE | 2026-03-02 18:28:58.675948 |

## `fin_cost_centres` — sample rows

| cost_centre_id | cost_centre_code | cost_centre_name | dept_id | manager_person_id | status | created_at |
|---|---|---|---|---|---|---|
| 1 | CC001 | Engineering | 1 | NULL | ACTIVE | 2026-03-02 18:28:58.747146 |
| 2 | CC002 | Finance | 2 | NULL | ACTIVE | 2026-03-02 18:28:58.747146 |
| 3 | CC004 | HR | 3 | NULL | ACTIVE | 2026-03-02 18:28:58.747146 |
| 4 | CC005 | Procurement | 4 | NULL | ACTIVE | 2026-03-02 18:28:58.747146 |
| 5 | CC003 | Marketing | 5 | NULL | ACTIVE | 2026-03-02 18:28:58.747146 |

## `fin_budget_headers` — sample rows

| budget_header_id | budget_name | ledger_id | budget_version_id | fiscal_year | total_amount | status | created_at |
|---|---|---|---|---|---|---|---|
| 1 | FY2025 Operating Budget | 1 | 1 | 2025 | 25000000.00 | APPROVED | 2026-03-02 18:28:58.771316 |
| 2 | FY2026 Operating Budget | 1 | 3 | 2026 | 27000000.00 | DRAFT | 2026-03-02 18:28:58.771316 |
| 3 | Budget 1 | 1201 | 3375 | 2025 | 354000.00 | APPROVED | 2026-03-03 12:02:03.900751 |
| 4 | Budget 2 | 2641 | 2213 | 2024 | 1720000.00 | APPROVED | 2026-03-03 12:02:03.900751 |
| 5 | Budget 3 | 2122 | 422 | 2025 | 1941000.00 | APPROVED | 2026-03-03 12:02:03.900751 |

## `fin_budget_lines` — sample rows

| budget_line_id | budget_header_id | cost_centre_id | account_code_id | period_name | amount | created_at |
|---|---|---|---|---|---|---|
| 1 | 1 | 1 | 1 | JAN-2025 | 430000.00 | 2026-03-02 18:28:58.773820 |
| 2 | 1 | 2 | 1 | JAN-2025 | 90000.00 | 2026-03-02 18:28:58.773820 |
| 3 | 1 | 3 | 1 | JAN-2025 | 150000.00 | 2026-03-02 18:28:58.773820 |
| 4 | 1 | 4 | 1 | JAN-2025 | 65000.00 | 2026-03-02 18:28:58.773820 |
| 5 | 1 | 5 | 1 | JAN-2025 | 55000.00 | 2026-03-02 18:28:58.773820 |

## `fin_gl_balances` — sample rows

| balance_id | cost_centre_id | account_code_id | period_name | fiscal_year | fiscal_quarter | period_debit | period_credit | period_net | begin_balance | end_balance | currency | created_at | actual_amount | budget_amount |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 29 | 5 | 8 | MAR-2025 | 2025 | 1 | 145000.00 | 0.00 | 145000.00 | 0.00 | 145000.00 | GBP | 2026-03-02 18:28:58.759997 | 145000.00 | 150000.00 |
| 54 | 4 | 6 | FEB-2025 | 2025 | 1 | 51000.00 | 0.00 | 51000.00 | 0.00 | 51000.00 | GBP | 2026-03-02 18:28:58.759997 | 51000.00 | 55000.00 |
| 79 | 7 | 7 | JAN-2025 | 2025 | 1 | 95000.00 | 0.00 | 95000.00 | 0.00 | 95000.00 | GBP | 2026-03-02 18:28:58.759997 | 95000.00 | 100000.00 |
| 179 | 1728 | 3074 | FEB-2026 | 2026 | 1 | 52000.00 | 20800.00 | NULL | NULL | 52000.00 | GBP | 2026-03-03 12:02:15.247051 | 46800.00 | 208000.00 |
| 180 | 814 | 1502 | FEB-2025 | 2025 | 1 | 115000.00 | 46000.00 | NULL | NULL | 115000.00 | GBP | 2026-03-03 12:02:15.247051 | 103500.00 | 325000.00 |

## `proc_po_headers` — sample rows

| po_header_id | po_number | supplier_id | requisition_id | buyer_id | total_amount | approved_amount | status | created_date | approved_date | approved_by | category | created_at | updated_at |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1722 | PO-B001722 | 2618 | 1722 | 61 | 7000.00 | 7000.00 | PENDING | 2023-07-17 | NULL | NULL | IT | 2026-03-03 12:02:25.466753 | 2026-03-03 12:02:25.466753 |
| 1933 | PO-B001933 | 3211 | 1933 | 44 | 149000.00 | 0.00 | PENDING | 2024-05-08 | NULL | NULL | IT | 2026-03-03 12:02:25.466753 | 2026-03-03 12:02:25.466753 |
| 2596 | PO-B002596 | 334 | 2596 | 18 | 330000.00 | 0.00 | APPROVED | 2025-12-11 | NULL | NULL | IT | 2026-03-03 12:02:25.649572 | 2026-03-03 12:02:25.649572 |
| 3349 | PO-B003349 | 3798 | 3349 | 76 | 330000.00 | 0.00 | PENDING | 2024-06-03 | NULL | NULL | IT | 2026-03-03 12:02:25.731087 | 2026-03-03 12:02:25.731087 |
| 1 | PO-2025-001 | 11 | 1 | 53 | 85000.00 | 0.00 | PENDING | NULL | NULL | NULL | IT Services | 2026-03-02 18:28:58.835487 | 2026-03-02 18:28:58.835487 |

## `proc_po_lines` — sample rows

| po_line_id | po_header_id | line_number | item_id | description | quantity | unit_price | line_amount | status | created_at |
|---|---|---|---|---|---|---|---|---|---|
| 1 | 1 | 1 | 1 | Services - PO-2025-001 | 1.00 | 85000.00 | 85000.00 | OPEN | 2026-03-02 18:28:58.840248 |
| 2 | 2 | 1 | 1 | Services - PO-2025-002 | 1.00 | 42000.00 | 42000.00 | OPEN | 2026-03-02 18:28:58.840248 |
| 3 | 3 | 1 | 1 | Services - PO-2025-003 | 1.00 | 120000.00 | 120000.00 | OPEN | 2026-03-02 18:28:58.840248 |
| 4 | 4 | 1 | 1 | Services - PO-2025-011 | 1.00 | 150000.00 | 150000.00 | OPEN | 2026-03-02 18:28:58.840248 |
| 5 | 5 | 1 | 1 | Services - PO-2025-012 | 1.00 | 48000.00 | 48000.00 | OPEN | 2026-03-02 18:28:58.840248 |

## `proc_po_distributions` — sample rows

| po_dist_id | po_line_id | cost_centre_id | account_code_id | distribution_pct | amount | created_at |
|---|---|---|---|---|---|---|
| 1 | 1 | 1 | 1 | 100.00 | 85000.00 | 2026-03-02 18:28:58.843394 |
| 2 | 2 | 1 | 1 | 100.00 | 42000.00 | 2026-03-02 18:28:58.843394 |
| 3 | 3 | 1 | 1 | 100.00 | 120000.00 | 2026-03-02 18:28:58.843394 |
| 4 | 4 | 1 | 1 | 100.00 | 150000.00 | 2026-03-02 18:28:58.843394 |
| 5 | 5 | 1 | 1 | 100.00 | 48000.00 | 2026-03-02 18:28:58.843394 |

## `fin_ap_invoices` — sample rows

| invoice_id | invoice_number | supplier_id | ledger_id | invoice_date | due_date | invoice_amount | paid_amount | outstanding_amount | currency | status | created_by | approved_by | created_at | updated_at |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | INV-2025-001 | 1 | 1 | 2025-01-10 | 2025-02-10 | 25000.00 | 25000.00 | 0.00 | GBP | PAID | NULL | NULL | 2026-03-02 18:28:58.786999 | 2026-03-02 18:28:58.786999 |
| 2 | INV-2025-002 | 2 | 1 | 2025-01-15 | 2025-02-15 | 18500.00 | 18500.00 | 0.00 | GBP | PAID | NULL | NULL | 2026-03-02 18:28:58.786999 | 2026-03-02 18:28:58.786999 |
| 3 | INV-2025-003 | 3 | 1 | 2025-02-01 | 2025-03-01 | 42000.00 | 42000.00 | 0.00 | GBP | PAID | NULL | NULL | 2026-03-02 18:28:58.786999 | 2026-03-02 18:28:58.786999 |
| 4 | INV-2025-004 | 4 | 1 | 2025-02-10 | 2025-03-10 | 8500.00 | 8500.00 | 0.00 | GBP | PAID | NULL | NULL | 2026-03-02 18:28:58.786999 | 2026-03-02 18:28:58.786999 |
| 5 | INV-2025-005 | 5 | 1 | 2025-03-01 | 2025-04-01 | 12000.00 | 12000.00 | 0.00 | GBP | PAID | NULL | NULL | 2026-03-02 18:28:58.786999 | 2026-03-02 18:28:58.786999 |

## `fin_ap_payments` — sample rows

| payment_id | payment_number | supplier_id | payment_date | payment_amount | payment_method | reference | status | created_at |
|---|---|---|---|---|---|---|---|---|
| 1 | PAY-2025-001 | 1 | 2025-02-10 | 25000.00 | BACS | BACS-0001 | COMPLETED | 2026-03-02 18:28:58.796572 |
| 2 | PAY-2025-002 | 2 | 2025-02-15 | 18500.00 | BACS | BACS-0002 | COMPLETED | 2026-03-02 18:28:58.796572 |
| 3 | PAY-2025-003 | 3 | 2025-03-01 | 42000.00 | BACS | BACS-0003 | COMPLETED | 2026-03-02 18:28:58.796572 |
| 4 | PAY-2025-004 | 4 | 2025-03-10 | 8500.00 | BACS | BACS-0004 | COMPLETED | 2026-03-02 18:28:58.796572 |
| 5 | PAY-2025-005 | 5 | 2025-04-01 | 12000.00 | BACS | BACS-0005 | COMPLETED | 2026-03-02 18:28:58.796572 |

## `sup_suppliers` — sample rows

| supplier_id | supplier_number | supplier_name | tax_registration | payment_terms | supplier_type | risk_rating | qualification_status | status | country | created_at | updated_at |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | SUP001 | Capita Solutions Ltd | GB100000000 | NET30 | IT_SERVICES | LOW | QUALIFIED | ACTIVE | United Kingdom | 2026-03-02 18:28:58.776948 | 2026-03-02 18:28:58.776948 |
| 2 | SUP002 | Serco Group plc | GB100000001 | NET30 | IT_SERVICES | LOW | QUALIFIED | ACTIVE | United Kingdom | 2026-03-02 18:28:58.776948 | 2026-03-02 18:28:58.776948 |
| 3 | SUP003 | Computacenter UK | GB100000002 | NET30 | HARDWARE | LOW | QUALIFIED | ACTIVE | United Kingdom | 2026-03-02 18:28:58.776948 | 2026-03-02 18:28:58.776948 |
| 4 | SUP004 | BT Business | GB100000003 | NET30 | TELECOM | LOW | QUALIFIED | ACTIVE | United Kingdom | 2026-03-02 18:28:58.776948 | 2026-03-02 18:28:58.776948 |
| 5 | SUP005 | Vodafone UK Ltd | GB100000004 | NET30 | TELECOM | LOW | QUALIFIED | ACTIVE | United Kingdom | 2026-03-02 18:28:58.776948 | 2026-03-02 18:28:58.776948 |

---

# JOIN PATH ANALYSIS

## Core Join Paths

### 1. Headcount by Department

```sql
hcm_assignments a
JOIN hcm_departments d ON d.dept_id = a.dept_id
WHERE a.assignment_status = 'ACTIVE'
GROUP BY d.dept_name
```

> hcm_assignments is the single source of all org context (department, salary, grade).
> hcm_persons contains identity only — it has NO dept_id.

---

### 2. Budget by Cost Centre (correct path)

```sql
fin_budget_lines bl
JOIN fin_budget_headers bh   ON bh.budget_header_id = bl.budget_header_id
JOIN fin_cost_centres   cc   ON cc.cost_centre_id    = bl.cost_centre_id
WHERE bh.fiscal_year = 2024
GROUP BY cc.cost_centre_name
-- VALUE COLUMN: bl.amount
```

> fin_budget_headers has only metadata (fiscal_year, total_amount for the whole budget).
> NEVER use fin_budget_headers.total_amount for per-cost-centre budget amounts.

---

### 3. GL Actuals by Cost Centre

```sql
SELECT cc.cost_centre_name,
       SUM(gl.period_net) AS net_activity,
       SUM(gl.end_balance) AS closing_balance
FROM fin_gl_balances gl
JOIN fin_cost_centres cc ON cc.cost_centre_id = gl.cost_centre_id
WHERE gl.fiscal_year = 2024
GROUP BY cc.cost_centre_name
```

> fin_gl_balances does NOT have actual_amount or budget_amount columns.
> Use period_net for the net movement and end_balance for the period-end balance.

---

### 4. PO Spend by Department (full traversal required)

```sql
SELECT d.dept_name, SUM(pod.amount) AS total_spend
FROM proc_po_distributions pod
JOIN fin_cost_centres     cc  ON cc.cost_centre_id    = pod.cost_centre_id
JOIN hcm_departments      d   ON d.dept_id            = cc.dept_id
GROUP BY d.dept_name
-- Optionally JOIN proc_po_lines / proc_po_headers for date/supplier filtering
```

> proc_po_headers has NO cost_centre_id.
> proc_po_distributions has NO po_header_id.
> Must traverse: distributions -> po_lines -> po_headers.

---

### 5. AP Invoice by Supplier

```sql
SELECT s.supplier_name, SUM(i.invoice_amount) AS total_invoiced
FROM fin_ap_invoices i
JOIN sup_suppliers s ON s.supplier_id = i.supplier_id
GROUP BY s.supplier_name
-- Column: invoice_amount (NOT amount)
```

---

### 6. AP Payments by Supplier

```sql
SELECT s.supplier_name, SUM(p.payment_amount) AS total_paid
FROM fin_ap_payments p
JOIN sup_suppliers s ON s.supplier_id = p.supplier_id
GROUP BY s.supplier_name
-- fin_ap_payments has NO invoice_id column
```

---

### 7. Budget vs GL Comparison (cross-table — requires CTE or subquery)

```sql
WITH budget AS (
    SELECT cc.cost_centre_name, SUM(bl.amount) AS budget_amount
    FROM fin_budget_lines bl
    JOIN fin_cost_centres cc ON cc.cost_centre_id = bl.cost_centre_id
    JOIN fin_budget_headers bh ON bh.budget_header_id = bl.budget_header_id
    WHERE bh.fiscal_year = 2024
    GROUP BY cc.cost_centre_name
),
actuals AS (
    SELECT cc.cost_centre_name, SUM(gl.period_net) AS actual_amount
    FROM fin_gl_balances gl
    JOIN fin_cost_centres cc ON cc.cost_centre_id = gl.cost_centre_id
    WHERE gl.fiscal_year = 2024
    GROUP BY cc.cost_centre_name
)
SELECT b.cost_centre_name,
       b.budget_amount,
       a.actual_amount,
       a.actual_amount - b.budget_amount AS variance
FROM budget b
LEFT JOIN actuals a ON a.cost_centre_name = b.cost_centre_name
```

---

### 8. Employee → Cost Centre Bridge (via hcm_cost_allocations)

```sql
hcm_assignments a
JOIN hcm_cost_allocations ca ON ca.assignment_id = a.assignment_id
JOIN fin_cost_centres cc     ON cc.cost_centre_id = ca.cost_centre_id
WHERE ca.effective_to IS NULL
```

---

# POTENTIAL DATA ISSUES

## Integrity Check Results

| Check | Orphan Count | Status |
|---|---|---|
| Cost centres with no matching dept | 0 | OK |
| Budget lines with orphan budget_header_id | 0 | OK |
| Budget lines with orphan cost_centre_id | 0 | OK |
| GL balances with orphan cost_centre_id | 0 | OK |
| Assignments with missing person_id | 0 | OK |
| PO distributions with missing po_line_id | 0 | OK |
| Budget lines where amount IS NULL or 0 | 0 | OK |
| GL balances where period_net IS NULL | 3870 | ISSUE |
| AP invoices where invoice_amount IS NULL | 0 | OK |
| PO distributions where amount IS NULL | 0 | OK |

## Tables With Zero Rows

All tables have at least 1 row.

## Critical Schema Gotchas


| Issue | Incorrect Assumption | Correct Fact |
|---|---|---|
| Budget values | `fin_budget_headers.budget_amount` | `fin_budget_lines.amount` |
| GL actuals | `fin_gl_balances.actual_amount` | `fin_gl_balances.period_net` or `end_balance` |
| AP invoice amount column | `fin_ap_invoices.amount` | `fin_ap_invoices.invoice_amount` |
| Cost centre on PO | `proc_po_headers.cost_centre_id` | Does not exist — use `proc_po_distributions.cost_centre_id` |
| PO header from distribution | `proc_po_distributions.po_header_id` | Does not exist — traverse via `proc_po_lines` |
| Salary location | `hcm_persons.salary` | `hcm_assignments.salary` |
| Department on person | `hcm_persons.dept_id` | Does not exist — use `hcm_assignments.dept_id` |
| Payment → Invoice FK | `fin_ap_payments.invoice_id` | Does not exist — join only via `supplier_id` |
| GL budget_amount column | `fin_gl_balances.budget_amount` | Does not exist in this schema |
| GL actual_amount column | `fin_gl_balances.actual_amount` | Does not exist — use `period_net` or `end_balance` |
| fin_budget_lines date | `fin_budget_lines.start_date` | Does not exist — use `period_name` + JOIN to `fin_reporting_periods` |

---

# SQL AGENT RISK AREAS


| Risk | Root Cause | Fix |
|---|---|---|
| Budget query returns 0 rows | Querying `fin_budget_headers.budget_amount` (budget_version total, not per cost centre) | Always use `fin_budget_lines.amount` |
| GL actual query fails | LLM generates `fin_gl_balances.actual_amount` — column does not exist | Use `period_net` (activity) or `end_balance` (balance) |
| AP invoice query fails | LLM uses `fin_ap_invoices.amount` — column does not exist | Use `invoice_amount` |
| PO spend wrong level | LLM sums `proc_po_headers.total_amount` giving org-level, not dept-level | Must use `proc_po_distributions.amount` |
| No dept-level finance data | LLM joins HCM departments directly to finance tables | Route through `fin_cost_centres.dept_id` |
| Time filter broken | LLM uses `fin_budget_lines.start_date` — column does not exist | Join `fin_budget_lines` to `fin_reporting_periods` via `period_name` |
| Budget vs actual comparison fails | LLM attempts single table join — tables have no common amount columns | Use CTE: budget from `fin_budget_lines`, actuals from `fin_gl_balances` |
| Cross-domain Cartesian explosion | Flat JOIN of 3 domains without aggregation anchor | Use CTEs per domain, then LEFT JOIN on cost_centre_name |
| Supplier name no match | LLM uses exact string match | Use `ILIKE '%%name%%'` |
| Payment not linked to invoice | LLM tries JOIN on invoice_id | `fin_ap_payments` has no `invoice_id`; use `fin_ap_payment_schedules` → `fin_ap_invoices` |

---

# SUMMARY

## Key Tables by Use Case


| Use Case | Primary Table | Value Column | Critical Join |
|---|---|---|---|
| Budget by cost centre | `fin_budget_lines` | `amount` | JOIN `fin_budget_headers` (fiscal_year), `fin_cost_centres` |
| GL net activity | `fin_gl_balances` | `period_net` | JOIN `fin_cost_centres` |
| GL closing balance | `fin_gl_balances` | `end_balance` | JOIN `fin_cost_centres` |
| PO spend by dept | `proc_po_distributions` | `amount` | JOIN `proc_po_lines`, `fin_cost_centres`, `hcm_departments` |
| AP invoices | `fin_ap_invoices` | `invoice_amount` | JOIN `sup_suppliers` |
| AP payments | `fin_ap_payments` | `payment_amount` | JOIN `sup_suppliers` |
| Employee salary | `hcm_assignments` | `salary` | JOIN `hcm_departments`, `hcm_persons` |
| Headcount | `hcm_assignments` | COUNT(DISTINCT person_id) | WHERE assignment_status='ACTIVE' |


## Mandatory AI SQL Agent Rules


1. **NEVER** use `fin_budget_headers.budget_amount` — always `fin_budget_lines.amount`
2. **NEVER** use `fin_gl_balances.actual_amount` — always `period_net` or `end_balance`
3. **NEVER** use `fin_ap_invoices.amount` — always `invoice_amount`
4. **NEVER** put `cost_centre_id` on `proc_po_headers` — it's on `proc_po_distributions`
5. **NEVER** put `po_header_id` on `proc_po_distributions` — traverse via `proc_po_lines`
6. **NEVER** access `fin_budget_lines.start_date` — it doesn't exist; use `period_name`
7. **NEVER** put `dept_id` or `salary` on `hcm_persons` — they're on `hcm_assignments`
8. **ALWAYS** filter headcount with `WHERE assignment_status='ACTIVE'`
9. **ALWAYS** use `ILIKE '%%name%%'` for supplier/department name lookups
10. **ALWAYS** use CTEs for cross-domain queries (HCM + Finance + Procurement)
