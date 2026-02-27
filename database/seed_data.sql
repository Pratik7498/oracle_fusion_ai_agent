-- ============================================================
-- Oracle Fusion AI Agent POC — Seed Data
-- ============================================================

-- ────────────────────────────────────────
-- hcm_employees: 80 rows (60 ACTIVE, 20 TERMINATED)
-- Engineering: 47 active | Finance:8 | HR:4 | Procurement:3 | Marketing:5 | Sales:4 | Operations:4 (total active = 75... wait)
-- Corrected: Eng=47, Fin=3, HR=1, Proc=1, Mktg=3, Sales=3, Ops=2 = 60 active
-- Actually per spec: Engineering(47), Finance(8), HR(4), Procurement(3), Marketing(5), Sales(4), Operations(4)
-- That sums to 47+8+4+3+5+4+4 = 75 not 60. Spec says "adjust so total active = 60"
-- So: Engineering=47, Finance=3, HR=2, Procurement=1, Marketing=3, Sales=2, Operations=2 = 60
-- ────────────────────────────────────────

-- Engineering (47 active)
INSERT INTO hcm_employees (full_name, department, job_title, grade_level, salary, hire_date, termination_date, employment_status, location, manager_id) VALUES
('James Okonkwo', 'Engineering', 'VP of Engineering', 'G8', 118000.00, '2019-03-15', NULL, 'ACTIVE', 'London', NULL),
('Sarah Chen', 'Engineering', 'Engineering Director', 'G8', 112000.00, '2019-06-01', NULL, 'ACTIVE', 'London', 1),
('Priya Sharma', 'Engineering', 'Senior Staff Engineer', 'G7', 102000.00, '2019-09-12', NULL, 'ACTIVE', 'London', 1),
('David Williams', 'Engineering', 'Staff Engineer', 'G7', 96000.00, '2020-01-20', NULL, 'ACTIVE', 'Manchester', 1),
('Fatima Al-Hassan', 'Engineering', 'Staff Engineer', 'G7', 94000.00, '2020-03-10', NULL, 'ACTIVE', 'London', 1),
('Michael Brown', 'Engineering', 'Senior Engineer', 'G6', 82000.00, '2020-05-18', NULL, 'ACTIVE', 'Remote', 2),
('Aisha Patel', 'Engineering', 'Senior Engineer', 'G6', 79000.00, '2020-06-22', NULL, 'ACTIVE', 'London', 2),
('Tom Richardson', 'Engineering', 'Senior Engineer', 'G6', 76000.00, '2020-08-03', NULL, 'ACTIVE', 'Manchester', 2),
('Elena Kowalski', 'Engineering', 'Senior Engineer', 'G6', 74000.00, '2020-09-14', NULL, 'ACTIVE', 'Birmingham', 2),
('Raj Gupta', 'Engineering', 'Senior Engineer', 'G6', 72000.00, '2020-11-01', NULL, 'ACTIVE', 'London', 3),
('Hannah Taylor', 'Engineering', 'Engineer', 'G5', 62000.00, '2021-01-15', NULL, 'ACTIVE', 'Remote', 6),
('Kwame Asante', 'Engineering', 'Engineer', 'G5', 60000.00, '2021-02-20', NULL, 'ACTIVE', 'London', 6),
('Sophie Martin', 'Engineering', 'Engineer', 'G5', 58000.00, '2021-04-05', NULL, 'ACTIVE', 'Manchester', 7),
('Omar Hussain', 'Engineering', 'Engineer', 'G5', 56000.00, '2021-05-10', NULL, 'ACTIVE', 'London', 7),
('Charlotte Evans', 'Engineering', 'Engineer', 'G5', 55000.00, '2021-06-14', NULL, 'ACTIVE', 'Remote', 8),
('Yuki Tanaka', 'Engineering', 'Engineer', 'G5', 54000.00, '2021-07-19', NULL, 'ACTIVE', 'Birmingham', 8),
('Daniel Murphy', 'Engineering', 'Engineer', 'G5', 52000.00, '2021-08-23', NULL, 'ACTIVE', 'London', 9),
('Blessing Obi', 'Engineering', 'Engineer', 'G5', 51000.00, '2021-10-01', NULL, 'ACTIVE', 'Remote', 9),
('Liam O''Brien', 'Engineering', 'Engineer', 'G5', 50000.00, '2021-11-15', NULL, 'ACTIVE', 'Manchester', 10),
('Anya Petrova', 'Engineering', 'Engineer', 'G5', 49000.00, '2022-01-10', NULL, 'ACTIVE', 'London', 10),
('Jack Hughes', 'Engineering', 'Junior Engineer', 'G4', 45000.00, '2022-03-01', NULL, 'ACTIVE', 'London', 11),
('Mei Lin', 'Engineering', 'Junior Engineer', 'G4', 44000.00, '2022-04-15', NULL, 'ACTIVE', 'Remote', 11),
('Ryan Kelly', 'Engineering', 'Junior Engineer', 'G4', 43000.00, '2022-05-20', NULL, 'ACTIVE', 'Birmingham', 12),
('Zara Khan', 'Engineering', 'Junior Engineer', 'G4', 42000.00, '2022-07-01', NULL, 'ACTIVE', 'London', 12),
('Oliver Wood', 'Engineering', 'Junior Engineer', 'G4', 41000.00, '2022-08-15', NULL, 'ACTIVE', 'Manchester', 13),
('Nkechi Eze', 'Engineering', 'Junior Engineer', 'G4', 40000.00, '2022-09-20', NULL, 'ACTIVE', 'London', 13),
('Isla Campbell', 'Engineering', 'Junior Engineer', 'G4', 39000.00, '2022-11-01', NULL, 'ACTIVE', 'Remote', 14),
('Arjun Singh', 'Engineering', 'Junior Engineer', 'G4', 38000.00, '2023-01-10', NULL, 'ACTIVE', 'London', 14),
('Emily Watson', 'Engineering', 'Junior Engineer', 'G4', 37000.00, '2023-02-20', NULL, 'ACTIVE', 'Manchester', 15),
('Kofi Mensah', 'Engineering', 'Junior Engineer', 'G4', 36000.00, '2023-04-01', NULL, 'ACTIVE', 'Birmingham', 15),
('Grace Liu', 'Engineering', 'Graduate Engineer', 'G3', 34000.00, '2023-06-15', NULL, 'ACTIVE', 'London', 16),
('Nathan Clarke', 'Engineering', 'Graduate Engineer', 'G3', 33000.00, '2023-07-20', NULL, 'ACTIVE', 'Remote', 16),
('Amara Diallo', 'Engineering', 'Graduate Engineer', 'G3', 32000.00, '2023-09-01', NULL, 'ACTIVE', 'London', 17),
('Harry Thompson', 'Engineering', 'Graduate Engineer', 'G3', 31000.00, '2023-10-15', NULL, 'ACTIVE', 'Manchester', 17),
('Suki Nakamura', 'Engineering', 'Graduate Engineer', 'G3', 30000.00, '2023-11-20', NULL, 'ACTIVE', 'London', 18),
('Ben Carter', 'Engineering', 'Graduate Engineer', 'G3', 29000.00, '2024-01-08', NULL, 'ACTIVE', 'Remote', 18),
('Rosa Fernandez', 'Engineering', 'Graduate Engineer', 'G3', 28500.00, '2024-02-15', NULL, 'ACTIVE', 'Birmingham', 19),
('Callum Stewart', 'Engineering', 'Graduate Engineer', 'G3', 28000.00, '2024-03-20', NULL, 'ACTIVE', 'London', 19),
('Adaeze Nwankwo', 'Engineering', 'DevOps Engineer', 'G5', 63000.00, '2021-03-10', NULL, 'ACTIVE', 'London', 3),
('Marcus Johnson', 'Engineering', 'DevOps Engineer', 'G5', 61000.00, '2021-12-01', NULL, 'ACTIVE', 'Remote', 3),
('Freya Nielsen', 'Engineering', 'QA Engineer', 'G5', 57000.00, '2022-02-14', NULL, 'ACTIVE', 'Manchester', 4),
('Ibrahim Yusuf', 'Engineering', 'QA Engineer', 'G4', 46000.00, '2022-06-01', NULL, 'ACTIVE', 'London', 4),
('Lucy Adams', 'Engineering', 'Data Engineer', 'G6', 78000.00, '2020-07-15', NULL, 'ACTIVE', 'London', 3),
('Tomasz Nowak', 'Engineering', 'Data Engineer', 'G5', 59000.00, '2021-09-20', NULL, 'ACTIVE', 'Remote', 43),
('Chloe Baker', 'Engineering', 'Platform Engineer', 'G6', 80000.00, '2020-04-01', NULL, 'ACTIVE', 'London', 2),
('Ravi Krishnan', 'Engineering', 'Platform Engineer', 'G5', 64000.00, '2022-01-15', NULL, 'ACTIVE', 'Birmingham', 45),
('Olivia Scott', 'Engineering', 'Security Engineer', 'G6', 83000.00, '2020-10-01', NULL, 'ACTIVE', 'London', 1);

-- Finance (3 active)
INSERT INTO hcm_employees (full_name, department, job_title, grade_level, salary, hire_date, termination_date, employment_status, location, manager_id) VALUES
('Victoria Chang', 'Finance', 'Finance Director', 'G8', 115000.00, '2019-04-01', NULL, 'ACTIVE', 'London', NULL),
('George Whitfield', 'Finance', 'Senior Accountant', 'G6', 75000.00, '2020-02-15', NULL, 'ACTIVE', 'London', 48),
('Amina Begum', 'Finance', 'Financial Analyst', 'G5', 58000.00, '2021-05-20', NULL, 'ACTIVE', 'Manchester', 48);

-- HR (2 active)
INSERT INTO hcm_employees (full_name, department, job_title, grade_level, salary, hire_date, termination_date, employment_status, location, manager_id) VALUES
('Patricia Okafor', 'HR', 'HR Director', 'G8', 110000.00, '2019-07-10', NULL, 'ACTIVE', 'London', NULL),
('Simon Gallagher', 'HR', 'HR Business Partner', 'G6', 71000.00, '2020-11-20', NULL, 'ACTIVE', 'Remote', 51);

-- Procurement (1 active)
INSERT INTO hcm_employees (full_name, department, job_title, grade_level, salary, hire_date, termination_date, employment_status, location, manager_id) VALUES
('Henry Osei', 'Procurement', 'Procurement Manager', 'G7', 88000.00, '2019-11-01', NULL, 'ACTIVE', 'London', NULL);

-- Marketing (3 active)
INSERT INTO hcm_employees (full_name, department, job_title, grade_level, salary, hire_date, termination_date, employment_status, location, manager_id) VALUES
('Jessica Park', 'Marketing', 'Marketing Director', 'G8', 108000.00, '2019-08-15', NULL, 'ACTIVE', 'London', NULL),
('Tariq Ali', 'Marketing', 'Marketing Manager', 'G6', 70000.00, '2021-01-10', NULL, 'ACTIVE', 'Remote', 54),
('Fiona McLeod', 'Marketing', 'Content Specialist', 'G4', 42000.00, '2023-03-15', NULL, 'ACTIVE', 'Manchester', 54);

-- Sales (2 active)
INSERT INTO hcm_employees (full_name, department, job_title, grade_level, salary, hire_date, termination_date, employment_status, location, manager_id) VALUES
('Robert Achebe', 'Sales', 'Sales Director', 'G8', 116000.00, '2019-05-20', NULL, 'ACTIVE', 'London', NULL),
('Natasha Volkov', 'Sales', 'Account Executive', 'G5', 55000.00, '2022-04-01', NULL, 'ACTIVE', 'Birmingham', 57);

-- Operations (2 active)
INSERT INTO hcm_employees (full_name, department, job_title, grade_level, salary, hire_date, termination_date, employment_status, location, manager_id) VALUES
('William Nkomo', 'Operations', 'Operations Director', 'G8', 109000.00, '2019-10-10', NULL, 'ACTIVE', 'London', NULL),
('Catherine Doyle', 'Operations', 'Operations Analyst', 'G5', 53000.00, '2022-08-01', NULL, 'ACTIVE', 'Remote', 59);

-- TERMINATED employees (20)
INSERT INTO hcm_employees (full_name, department, job_title, grade_level, salary, hire_date, termination_date, employment_status, location, manager_id) VALUES
('Peter Nowak', 'Engineering', 'Engineer', 'G5', 55000.00, '2021-03-15', '2025-03-01', 'TERMINATED', 'London', 6),
('Sandra Kim', 'Engineering', 'Junior Engineer', 'G4', 40000.00, '2022-09-01', '2025-04-15', 'TERMINATED', 'Remote', 11),
('Derek Shaw', 'Engineering', 'Graduate Engineer', 'G3', 30000.00, '2023-06-01', '2025-05-20', 'TERMINATED', 'Manchester', 16),
('Monica Reyes', 'Engineering', 'Engineer', 'G5', 54000.00, '2021-07-10', '2025-06-10', 'TERMINATED', 'Birmingham', 7),
('Alan Foster', 'Engineering', 'Junior Engineer', 'G4', 41000.00, '2022-11-15', '2025-07-01', 'TERMINATED', 'London', 12),
('Ingrid Larsen', 'Engineering', 'DevOps Engineer', 'G5', 58000.00, '2021-04-01', '2025-08-15', 'TERMINATED', 'Remote', 3),
('Chidi Okonkwo', 'Engineering', 'QA Engineer', 'G4', 44000.00, '2022-05-10', '2025-09-01', 'TERMINATED', 'London', 4),
('Karen Mitchell', 'Engineering', 'Data Engineer', 'G5', 57000.00, '2021-08-20', '2025-10-15', 'TERMINATED', 'Manchester', 43),
('Youssef El-Amin', 'Engineering', 'Platform Engineer', 'G5', 60000.00, '2021-11-05', '2025-11-20', 'TERMINATED', 'London', 45),
('Lisa Zhang', 'Engineering', 'Engineer', 'G5', 53000.00, '2022-01-20', '2025-12-01', 'TERMINATED', 'Remote', 8),
('Paul Bennett', 'Finance', 'Accountant', 'G5', 52000.00, '2021-06-15', '2025-04-01', 'TERMINATED', 'London', 48),
('Diana Rossi', 'Finance', 'Financial Analyst', 'G4', 45000.00, '2022-03-10', '2025-07-15', 'TERMINATED', 'Manchester', 48),
('Trevor Grant', 'HR', 'HR Coordinator', 'G4', 40000.00, '2022-08-01', '2025-05-01', 'TERMINATED', 'Birmingham', 51),
('Nina Johansson', 'HR', 'Recruiter', 'G4', 42000.00, '2022-10-20', '2025-09-15', 'TERMINATED', 'London', 51),
('Samuel Obeng', 'Procurement', 'Procurement Analyst', 'G4', 43000.00, '2022-07-15', '2025-06-20', 'TERMINATED', 'Remote', 53),
('Rachel Cooper', 'Procurement', 'Buyer', 'G4', 41000.00, '2023-01-10', '2025-10-01', 'TERMINATED', 'London', 53),
('Ahmed Hassan', 'Marketing', 'Digital Marketer', 'G4', 39000.00, '2023-02-15', '2025-08-01', 'TERMINATED', 'Manchester', 54),
('Wendy Griffiths', 'Marketing', 'Marketing Analyst', 'G4', 38000.00, '2023-05-01', '2025-11-15', 'TERMINATED', 'London', 54),
('Ian Wallace', 'Sales', 'Sales Rep', 'G4', 40000.00, '2023-01-20', '2025-07-20', 'TERMINATED', 'Remote', 57),
('Joanna Price', 'Operations', 'Ops Coordinator', 'G3', 30000.00, '2023-08-10', '2025-12-15', 'TERMINATED', 'Birmingham', 59);


-- ────────────────────────────────────────
-- finance_gl_balances: 130 rows (10 CCs × 13 periods)
-- CC003 Marketing Q4 2025 is OVER BUDGET (critical)
-- ────────────────────────────────────────

INSERT INTO finance_gl_balances (cost_centre, cost_centre_name, account_code, account_name, period_name, actual_amount, budget_amount, currency, fiscal_year, fiscal_quarter) VALUES
-- CC001 Engineering
('CC001','Engineering','5001','Salaries & Wages','JAN-2025',420000,430000,'GBP',2025,1),
('CC001','Engineering','5001','Salaries & Wages','FEB-2025',418000,430000,'GBP',2025,1),
('CC001','Engineering','5001','Salaries & Wages','MAR-2025',425000,430000,'GBP',2025,1),
('CC001','Engineering','5001','Salaries & Wages','APR-2025',432000,435000,'GBP',2025,2),
('CC001','Engineering','5001','Salaries & Wages','MAY-2025',428000,435000,'GBP',2025,2),
('CC001','Engineering','5001','Salaries & Wages','JUN-2025',436000,435000,'GBP',2025,2),
('CC001','Engineering','5001','Salaries & Wages','JUL-2025',440000,440000,'GBP',2025,3),
('CC001','Engineering','5001','Salaries & Wages','AUG-2025',438000,440000,'GBP',2025,3),
('CC001','Engineering','5001','Salaries & Wages','SEP-2025',442000,440000,'GBP',2025,3),
('CC001','Engineering','5001','Salaries & Wages','OCT-2025',445000,445000,'GBP',2025,4),
('CC001','Engineering','5001','Salaries & Wages','NOV-2025',443000,445000,'GBP',2025,4),
('CC001','Engineering','5001','Salaries & Wages','DEC-2025',448000,450000,'GBP',2025,4),
('CC001','Engineering','5001','Salaries & Wages','JAN-2026',450000,450000,'GBP',2026,1),
-- CC002 Finance
('CC002','Finance','5002','Finance Operations','JAN-2025',85000,90000,'GBP',2025,1),
('CC002','Finance','5002','Finance Operations','FEB-2025',87000,90000,'GBP',2025,1),
('CC002','Finance','5002','Finance Operations','MAR-2025',88000,90000,'GBP',2025,1),
('CC002','Finance','5002','Finance Operations','APR-2025',89000,90000,'GBP',2025,2),
('CC002','Finance','5002','Finance Operations','MAY-2025',86000,90000,'GBP',2025,2),
('CC002','Finance','5002','Finance Operations','JUN-2025',91000,90000,'GBP',2025,2),
('CC002','Finance','5002','Finance Operations','JUL-2025',88000,90000,'GBP',2025,3),
('CC002','Finance','5002','Finance Operations','AUG-2025',87000,90000,'GBP',2025,3),
('CC002','Finance','5002','Finance Operations','SEP-2025',90000,90000,'GBP',2025,3),
('CC002','Finance','5002','Finance Operations','OCT-2025',89000,90000,'GBP',2025,4),
('CC002','Finance','5002','Finance Operations','NOV-2025',88000,90000,'GBP',2025,4),
('CC002','Finance','5002','Finance Operations','DEC-2025',92000,90000,'GBP',2025,4),
('CC002','Finance','5002','Finance Operations','JAN-2026',90000,92000,'GBP',2026,1),
-- CC003 Marketing — CRITICAL: OVER BUDGET in Q4 2025
('CC003','Marketing','5003','Marketing Spend','JAN-2025',140000,150000,'GBP',2025,1),
('CC003','Marketing','5003','Marketing Spend','FEB-2025',142000,150000,'GBP',2025,1),
('CC003','Marketing','5003','Marketing Spend','MAR-2025',145000,150000,'GBP',2025,1),
('CC003','Marketing','5003','Marketing Spend','APR-2025',148000,150000,'GBP',2025,2),
('CC003','Marketing','5003','Marketing Spend','MAY-2025',147000,150000,'GBP',2025,2),
('CC003','Marketing','5003','Marketing Spend','JUN-2025',149000,150000,'GBP',2025,2),
('CC003','Marketing','5003','Marketing Spend','JUL-2025',151000,150000,'GBP',2025,3),
('CC003','Marketing','5003','Marketing Spend','AUG-2025',148000,150000,'GBP',2025,3),
('CC003','Marketing','5003','Marketing Spend','SEP-2025',152000,150000,'GBP',2025,3),
('CC003','Marketing','5003','Marketing Spend','OCT-2025',162000,150000,'GBP',2025,4),
('CC003','Marketing','5003','Marketing Spend','NOV-2025',158000,150000,'GBP',2025,4),
('CC003','Marketing','5003','Marketing Spend','DEC-2025',171000,155000,'GBP',2025,4),
('CC003','Marketing','5003','Marketing Spend','JAN-2026',155000,155000,'GBP',2026,1),
-- CC004 HR
('CC004','HR','5004','HR Services','JAN-2025',60000,65000,'GBP',2025,1),
('CC004','HR','5004','HR Services','FEB-2025',62000,65000,'GBP',2025,1),
('CC004','HR','5004','HR Services','MAR-2025',63000,65000,'GBP',2025,1),
('CC004','HR','5004','HR Services','APR-2025',64000,65000,'GBP',2025,2),
('CC004','HR','5004','HR Services','MAY-2025',61000,65000,'GBP',2025,2),
('CC004','HR','5004','HR Services','JUN-2025',66000,65000,'GBP',2025,2),
('CC004','HR','5004','HR Services','JUL-2025',63000,65000,'GBP',2025,3),
('CC004','HR','5004','HR Services','AUG-2025',64000,65000,'GBP',2025,3),
('CC004','HR','5004','HR Services','SEP-2025',65000,65000,'GBP',2025,3),
('CC004','HR','5004','HR Services','OCT-2025',66000,65000,'GBP',2025,4),
('CC004','HR','5004','HR Services','NOV-2025',64000,65000,'GBP',2025,4),
('CC004','HR','5004','HR Services','DEC-2025',67000,65000,'GBP',2025,4),
('CC004','HR','5004','HR Services','JAN-2026',65000,66000,'GBP',2026,1),
-- CC005 Procurement
('CC005','Procurement','5005','Procurement Ops','JAN-2025',50000,55000,'GBP',2025,1),
('CC005','Procurement','5005','Procurement Ops','FEB-2025',51000,55000,'GBP',2025,1),
('CC005','Procurement','5005','Procurement Ops','MAR-2025',53000,55000,'GBP',2025,1),
('CC005','Procurement','5005','Procurement Ops','APR-2025',54000,55000,'GBP',2025,2),
('CC005','Procurement','5005','Procurement Ops','MAY-2025',52000,55000,'GBP',2025,2),
('CC005','Procurement','5005','Procurement Ops','JUN-2025',55000,55000,'GBP',2025,2),
('CC005','Procurement','5005','Procurement Ops','JUL-2025',53000,55000,'GBP',2025,3),
('CC005','Procurement','5005','Procurement Ops','AUG-2025',54000,55000,'GBP',2025,3),
('CC005','Procurement','5005','Procurement Ops','SEP-2025',56000,55000,'GBP',2025,3),
('CC005','Procurement','5005','Procurement Ops','OCT-2025',55000,55000,'GBP',2025,4),
('CC005','Procurement','5005','Procurement Ops','NOV-2025',54000,55000,'GBP',2025,4),
('CC005','Procurement','5005','Procurement Ops','DEC-2025',57000,55000,'GBP',2025,4),
('CC005','Procurement','5005','Procurement Ops','JAN-2026',55000,56000,'GBP',2026,1),
-- CC006 Sales
('CC006','Sales','5006','Sales Costs','JAN-2025',180000,185000,'GBP',2025,1),
('CC006','Sales','5006','Sales Costs','FEB-2025',182000,185000,'GBP',2025,1),
('CC006','Sales','5006','Sales Costs','MAR-2025',184000,185000,'GBP',2025,1),
('CC006','Sales','5006','Sales Costs','APR-2025',183000,185000,'GBP',2025,2),
('CC006','Sales','5006','Sales Costs','MAY-2025',186000,185000,'GBP',2025,2),
('CC006','Sales','5006','Sales Costs','JUN-2025',181000,185000,'GBP',2025,2),
('CC006','Sales','5006','Sales Costs','JUL-2025',185000,185000,'GBP',2025,3),
('CC006','Sales','5006','Sales Costs','AUG-2025',184000,185000,'GBP',2025,3),
('CC006','Sales','5006','Sales Costs','SEP-2025',187000,185000,'GBP',2025,3),
('CC006','Sales','5006','Sales Costs','OCT-2025',186000,188000,'GBP',2025,4),
('CC006','Sales','5006','Sales Costs','NOV-2025',185000,188000,'GBP',2025,4),
('CC006','Sales','5006','Sales Costs','DEC-2025',189000,190000,'GBP',2025,4),
('CC006','Sales','5006','Sales Costs','JAN-2026',187000,190000,'GBP',2026,1),
-- CC007 Operations
('CC007','Operations','5007','Operations','JAN-2025',95000,100000,'GBP',2025,1),
('CC007','Operations','5007','Operations','FEB-2025',97000,100000,'GBP',2025,1),
('CC007','Operations','5007','Operations','MAR-2025',98000,100000,'GBP',2025,1),
('CC007','Operations','5007','Operations','APR-2025',99000,100000,'GBP',2025,2),
('CC007','Operations','5007','Operations','MAY-2025',96000,100000,'GBP',2025,2),
('CC007','Operations','5007','Operations','JUN-2025',101000,100000,'GBP',2025,2),
('CC007','Operations','5007','Operations','JUL-2025',98000,100000,'GBP',2025,3),
('CC007','Operations','5007','Operations','AUG-2025',99000,100000,'GBP',2025,3),
('CC007','Operations','5007','Operations','SEP-2025',100000,100000,'GBP',2025,3),
('CC007','Operations','5007','Operations','OCT-2025',102000,100000,'GBP',2025,4),
('CC007','Operations','5007','Operations','NOV-2025',99000,100000,'GBP',2025,4),
('CC007','Operations','5007','Operations','DEC-2025',103000,100000,'GBP',2025,4),
('CC007','Operations','5007','Operations','JAN-2026',100000,102000,'GBP',2026,1),
-- CC008 IT
('CC008','IT','5008','IT Infrastructure','JAN-2025',200000,210000,'GBP',2025,1),
('CC008','IT','5008','IT Infrastructure','FEB-2025',205000,210000,'GBP',2025,1),
('CC008','IT','5008','IT Infrastructure','MAR-2025',208000,210000,'GBP',2025,1),
('CC008','IT','5008','IT Infrastructure','APR-2025',210000,215000,'GBP',2025,2),
('CC008','IT','5008','IT Infrastructure','MAY-2025',207000,215000,'GBP',2025,2),
('CC008','IT','5008','IT Infrastructure','JUN-2025',212000,215000,'GBP',2025,2),
('CC008','IT','5008','IT Infrastructure','JUL-2025',209000,215000,'GBP',2025,3),
('CC008','IT','5008','IT Infrastructure','AUG-2025',211000,215000,'GBP',2025,3),
('CC008','IT','5008','IT Infrastructure','SEP-2025',214000,215000,'GBP',2025,3),
('CC008','IT','5008','IT Infrastructure','OCT-2025',216000,215000,'GBP',2025,4),
('CC008','IT','5008','IT Infrastructure','NOV-2025',213000,215000,'GBP',2025,4),
('CC008','IT','5008','IT Infrastructure','DEC-2025',218000,220000,'GBP',2025,4),
('CC008','IT','5008','IT Infrastructure','JAN-2026',215000,220000,'GBP',2026,1),
-- CC009 Legal
('CC009','Legal','5009','Legal Services','JAN-2025',70000,75000,'GBP',2025,1),
('CC009','Legal','5009','Legal Services','FEB-2025',72000,75000,'GBP',2025,1),
('CC009','Legal','5009','Legal Services','MAR-2025',74000,75000,'GBP',2025,1),
('CC009','Legal','5009','Legal Services','APR-2025',73000,75000,'GBP',2025,2),
('CC009','Legal','5009','Legal Services','MAY-2025',71000,75000,'GBP',2025,2),
('CC009','Legal','5009','Legal Services','JUN-2025',76000,75000,'GBP',2025,2),
('CC009','Legal','5009','Legal Services','JUL-2025',74000,75000,'GBP',2025,3),
('CC009','Legal','5009','Legal Services','AUG-2025',73000,75000,'GBP',2025,3),
('CC009','Legal','5009','Legal Services','SEP-2025',75000,75000,'GBP',2025,3),
('CC009','Legal','5009','Legal Services','OCT-2025',76000,75000,'GBP',2025,4),
('CC009','Legal','5009','Legal Services','NOV-2025',74000,75000,'GBP',2025,4),
('CC009','Legal','5009','Legal Services','DEC-2025',77000,75000,'GBP',2025,4),
('CC009','Legal','5009','Legal Services','JAN-2026',75000,76000,'GBP',2026,1),
-- CC010 Executive
('CC010','Executive','5010','Executive Office','JAN-2025',300000,320000,'GBP',2025,1),
('CC010','Executive','5010','Executive Office','FEB-2025',305000,320000,'GBP',2025,1),
('CC010','Executive','5010','Executive Office','MAR-2025',310000,320000,'GBP',2025,1),
('CC010','Executive','5010','Executive Office','APR-2025',315000,320000,'GBP',2025,2),
('CC010','Executive','5010','Executive Office','MAY-2025',312000,320000,'GBP',2025,2),
('CC010','Executive','5010','Executive Office','JUN-2025',318000,320000,'GBP',2025,2),
('CC010','Executive','5010','Executive Office','JUL-2025',310000,320000,'GBP',2025,3),
('CC010','Executive','5010','Executive Office','AUG-2025',316000,320000,'GBP',2025,3),
('CC010','Executive','5010','Executive Office','SEP-2025',320000,320000,'GBP',2025,3),
('CC010','Executive','5010','Executive Office','OCT-2025',322000,325000,'GBP',2025,4),
('CC010','Executive','5010','Executive Office','NOV-2025',318000,325000,'GBP',2025,4),
('CC010','Executive','5010','Executive Office','DEC-2025',328000,330000,'GBP',2025,4),
('CC010','Executive','5010','Executive Office','JAN-2026',325000,330000,'GBP',2026,1);


-- ────────────────────────────────────────
-- finance_ap_invoices: 50 rows
-- ────────────────────────────────────────

INSERT INTO finance_ap_invoices (invoice_number, supplier_id, supplier_name, invoice_date, due_date, invoice_amount, paid_amount, outstanding_amount, status, cost_centre) VALUES
-- PAID (15)
('INV-2025-001',1,'Capita Solutions Ltd','2025-01-10','2025-02-10',25000.00,25000.00,0.00,'PAID','CC001'),
('INV-2025-002',2,'Serco Group plc','2025-01-15','2025-02-15',18500.00,18500.00,0.00,'PAID','CC001'),
('INV-2025-003',3,'Computacenter UK','2025-02-01','2025-03-01',42000.00,42000.00,0.00,'PAID','CC008'),
('INV-2025-004',4,'BT Business','2025-02-10','2025-03-10',8500.00,8500.00,0.00,'PAID','CC008'),
('INV-2025-005',5,'Vodafone UK Ltd','2025-03-01','2025-04-01',12000.00,12000.00,0.00,'PAID','CC008'),
('INV-2025-006',6,'Lloyds Banking Group','2025-03-15','2025-04-15',3200.00,3200.00,0.00,'PAID','CC002'),
('INV-2025-007',7,'Deloitte UK','2025-04-01','2025-05-01',65000.00,65000.00,0.00,'PAID','CC009'),
('INV-2025-008',8,'PwC UK','2025-04-15','2025-05-15',48000.00,48000.00,0.00,'PAID','CC002'),
('INV-2025-009',9,'KPMG UK','2025-05-01','2025-06-01',35000.00,35000.00,0.00,'PAID','CC009'),
('INV-2025-010',10,'Ernst & Young LLP','2025-05-15','2025-06-15',28000.00,28000.00,0.00,'PAID','CC002'),
('INV-2025-011',1,'Capita Solutions Ltd','2025-06-01','2025-07-01',15000.00,15000.00,0.00,'PAID','CC001'),
('INV-2025-012',11,'Accenture UK','2025-06-15','2025-07-15',72000.00,72000.00,0.00,'PAID','CC008'),
('INV-2025-013',12,'Wipro UK','2025-07-01','2025-08-01',22000.00,22000.00,0.00,'PAID','CC001'),
('INV-2025-014',13,'Tata Consultancy Services','2025-07-15','2025-08-15',55000.00,55000.00,0.00,'PAID','CC001'),
('INV-2025-015',14,'Infosys BPM UK','2025-08-01','2025-09-01',31000.00,31000.00,0.00,'PAID','CC008'),
-- APPROVED (12)
('INV-2025-016',15,'Mace Group','2025-09-01','2025-10-01',19500.00,0.00,19500.00,'APPROVED','CC007'),
('INV-2025-017',2,'Serco Group plc','2025-09-10','2025-10-10',24000.00,0.00,24000.00,'APPROVED','CC001'),
('INV-2025-018',3,'Computacenter UK','2025-09-15','2025-10-15',38000.00,0.00,38000.00,'APPROVED','CC008'),
('INV-2025-019',16,'G4S UK','2025-09-20','2025-10-20',7800.00,0.00,7800.00,'APPROVED','CC007'),
('INV-2025-020',4,'BT Business','2025-10-01','2025-11-01',14200.00,0.00,14200.00,'APPROVED','CC008'),
('INV-2025-021',17,'Balfour Beatty','2025-10-05','2025-11-05',85000.00,0.00,85000.00,'APPROVED','CC007'),
('INV-2025-022',5,'Vodafone UK Ltd','2025-10-10','2025-11-10',9800.00,0.00,9800.00,'APPROVED','CC008'),
('INV-2025-023',18,'Amey plc','2025-10-15','2025-11-15',16500.00,0.00,16500.00,'APPROVED','CC007'),
('INV-2025-024',6,'Lloyds Banking Group','2025-10-20','2025-11-20',4500.00,0.00,4500.00,'APPROVED','CC002'),
('INV-2025-025',19,'Mitie Group','2025-11-01','2025-12-01',21000.00,0.00,21000.00,'APPROVED','CC007'),
('INV-2025-026',7,'Deloitte UK','2025-11-10','2025-12-10',58000.00,0.00,58000.00,'APPROVED','CC009'),
('INV-2025-027',20,'Sodexo UK','2025-11-15','2025-12-15',11200.00,0.00,11200.00,'APPROVED','CC007'),
-- PENDING (15)
('INV-2025-028',8,'PwC UK','2025-11-20','2026-01-20',45000.00,0.00,45000.00,'PENDING','CC002'),
('INV-2025-029',9,'KPMG UK','2025-11-25','2026-01-25',33000.00,0.00,33000.00,'PENDING','CC009'),
('INV-2025-030',10,'Ernst & Young LLP','2025-12-01','2026-02-01',27500.00,0.00,27500.00,'PENDING','CC002'),
('INV-2025-031',11,'Accenture UK','2025-12-05','2026-02-05',62000.00,0.00,62000.00,'PENDING','CC008'),
('INV-2025-032',12,'Wipro UK','2025-12-10','2026-02-10',18000.00,0.00,18000.00,'PENDING','CC001'),
('INV-2025-033',13,'Tata Consultancy Services','2025-12-15','2026-02-15',41000.00,0.00,41000.00,'PENDING','CC001'),
('INV-2025-034',14,'Infosys BPM UK','2025-12-18','2026-02-18',26000.00,0.00,26000.00,'PENDING','CC008'),
('INV-2025-035',1,'Capita Solutions Ltd','2025-12-20','2026-02-20',1200.00,0.00,1200.00,'PENDING','CC001'),
('INV-2025-036',15,'Mace Group','2025-12-22','2026-02-22',14800.00,0.00,14800.00,'PENDING','CC007'),
('INV-2025-037',16,'G4S UK','2025-12-25','2026-02-25',5600.00,0.00,5600.00,'PENDING','CC007'),
('INV-2025-038',17,'Balfour Beatty','2026-01-05','2026-03-05',78000.00,0.00,78000.00,'PENDING','CC007'),
('INV-2025-039',18,'Amey plc','2026-01-10','2026-03-10',9200.00,0.00,9200.00,'PENDING','CC007'),
('INV-2025-040',19,'Mitie Group','2026-01-12','2026-03-12',17500.00,0.00,17500.00,'PENDING','CC007'),
('INV-2025-041',20,'Sodexo UK','2026-01-15','2026-03-15',6800.00,0.00,6800.00,'PENDING','CC007'),
('INV-2025-042',2,'Serco Group plc','2026-01-18','2026-03-18',23000.00,0.00,23000.00,'PENDING','CC001'),
-- OVERDUE (8) — due_date 65–120 days before current date
('INV-2025-043',3,'Computacenter UK','2025-06-20',CURRENT_DATE - INTERVAL '120 days',52000.00,0.00,52000.00,'OVERDUE','CC008'),
('INV-2025-044',4,'BT Business','2025-07-01',CURRENT_DATE - INTERVAL '110 days',11500.00,0.00,11500.00,'OVERDUE','CC008'),
('INV-2025-045',5,'Vodafone UK Ltd','2025-07-10',CURRENT_DATE - INTERVAL '100 days',8900.00,0.00,8900.00,'OVERDUE','CC008'),
('INV-2025-046',7,'Deloitte UK','2025-07-20',CURRENT_DATE - INTERVAL '90 days',43000.00,0.00,43000.00,'OVERDUE','CC009'),
('INV-2025-047',8,'PwC UK','2025-08-01',CURRENT_DATE - INTERVAL '85 days',37500.00,0.00,37500.00,'OVERDUE','CC002'),
('INV-2025-048',11,'Accenture UK','2025-08-10',CURRENT_DATE - INTERVAL '80 days',68000.00,0.00,68000.00,'OVERDUE','CC008'),
('INV-2025-049',13,'Tata Consultancy Services','2025-08-20',CURRENT_DATE - INTERVAL '70 days',29000.00,0.00,29000.00,'OVERDUE','CC001'),
('INV-2025-050',14,'Infosys BPM UK','2025-09-01',CURRENT_DATE - INTERVAL '65 days',16500.00,0.00,16500.00,'OVERDUE','CC008');


-- ────────────────────────────────────────
-- procurement_quotations: 30 rows (15 engagements × 2 versions)
-- E-205 is CRITICAL: delta = 12.4%
-- ────────────────────────────────────────

INSERT INTO procurement_quotations (engagement_id, engagement_name, supplier_name, original_amount, revised_amount, quotation_version, status, submission_date, category) VALUES
('E-201','SAP S/4HANA Upgrade','Accenture UK',150000.00,NULL,1,'SUBMITTED','2025-06-01','IT Services'),
('E-201','SAP S/4HANA Upgrade','Accenture UK',150000.00,165000.00,2,'APPROVED','2025-07-15','IT Services'),
('E-202','Annual Audit Services','Deloitte UK',95000.00,NULL,1,'SUBMITTED','2025-05-15','Consulting'),
('E-202','Annual Audit Services','Deloitte UK',95000.00,98500.00,2,'APPROVED','2025-06-20','Consulting'),
('E-203','Office Refurbishment Phase 1','Mace Group',220000.00,NULL,1,'SUBMITTED','2025-04-01','Facilities'),
('E-203','Office Refurbishment Phase 1','Mace Group',220000.00,245000.00,2,'APPROVED','2025-05-10','Facilities'),
('E-204','Network Security Assessment','BT Business',45000.00,NULL,1,'SUBMITTED','2025-08-01','IT Services'),
('E-204','Network Security Assessment','BT Business',45000.00,48200.00,2,'APPROVED','2025-09-15','IT Services'),
('E-205','Cloud Infrastructure Migration Phase 2','Computacenter UK',82000.00,NULL,1,'SUBMITTED','2025-10-01','IT Services'),
('E-205','Cloud Infrastructure Migration Phase 2','Computacenter UK',82000.00,92180.00,2,'APPROVED','2025-11-15','IT Services'),
('E-206','HR System Implementation','Wipro UK',180000.00,NULL,1,'SUBMITTED','2025-03-10','IT Services'),
('E-206','HR System Implementation','Wipro UK',180000.00,175000.00,2,'APPROVED','2025-04-20','IT Services'),
('E-207','Data Centre Consolidation','Tata Consultancy Services',250000.00,NULL,1,'SUBMITTED','2025-07-01','IT Services'),
('E-207','Data Centre Consolidation','Tata Consultancy Services',250000.00,262000.00,2,'APPROVED','2025-08-15','IT Services'),
('E-208','Cybersecurity Training Programme','Infosys BPM UK',35000.00,NULL,1,'SUBMITTED','2025-09-01','Consulting'),
('E-208','Cybersecurity Training Programme','Infosys BPM UK',35000.00,NULL,2,'REJECTED','2025-10-10','Consulting'),
('E-209','Facilities Management Contract','Sodexo UK',120000.00,NULL,1,'SUBMITTED','2025-05-01','Facilities'),
('E-209','Facilities Management Contract','Sodexo UK',120000.00,125000.00,2,'APPROVED','2025-06-15','Facilities'),
('E-210','ERP Data Migration','KPMG UK',78000.00,NULL,1,'SUBMITTED','2025-08-15','Consulting'),
('E-210','ERP Data Migration','KPMG UK',78000.00,82000.00,2,'APPROVED','2025-09-20','Consulting'),
('E-211','Desktop Hardware Refresh','Computacenter UK',65000.00,NULL,1,'SUBMITTED','2025-10-01','Hardware'),
('E-211','Desktop Hardware Refresh','Computacenter UK',65000.00,62500.00,2,'APPROVED','2025-11-01','Hardware'),
('E-212','Legal Advisory Services','Ernst & Young LLP',55000.00,NULL,1,'SUBMITTED','2025-06-15','Consulting'),
('E-212','Legal Advisory Services','Ernst & Young LLP',55000.00,57500.00,2,'APPROVED','2025-07-20','Consulting'),
('E-213','Cloud Telephony Migration','Vodafone UK Ltd',42000.00,NULL,1,'SUBMITTED','2025-09-10','IT Services'),
('E-213','Cloud Telephony Migration','Vodafone UK Ltd',42000.00,44100.00,2,'APPROVED','2025-10-20','IT Services'),
('E-214','Security Guard Services','G4S UK',28000.00,NULL,1,'SUBMITTED','2025-07-01','Facilities'),
('E-214','Security Guard Services','G4S UK',28000.00,29400.00,2,'APPROVED','2025-08-10','Facilities'),
('E-215','Payroll Processing Outsource','Capita Solutions Ltd',15000.00,NULL,1,'DRAFT','2025-11-01','Consulting'),
('E-215','Payroll Processing Outsource','Capita Solutions Ltd',15000.00,NULL,2,'DRAFT','2025-12-01','Consulting');


-- ────────────────────────────────────────
-- procurement_purchase_orders: 40 rows
-- ────────────────────────────────────────

INSERT INTO procurement_purchase_orders (po_number, supplier_name, total_amount, approved_amount, status, created_date, approved_date, cost_centre, category) VALUES
-- PENDING (10) — created 20+ days ago
('PO-2025-001','Accenture UK',85000.00,0.00,'PENDING',CURRENT_DATE - INTERVAL '45 days',NULL,'CC008','IT Services'),
('PO-2025-002','Deloitte UK',42000.00,0.00,'PENDING',CURRENT_DATE - INTERVAL '38 days',NULL,'CC009','Consulting'),
('PO-2025-003','Computacenter UK',120000.00,0.00,'PENDING',CURRENT_DATE - INTERVAL '35 days',NULL,'CC008','Hardware'),
('PO-2025-004','BT Business',28000.00,0.00,'PENDING',CURRENT_DATE - INTERVAL '30 days',NULL,'CC008','IT Services'),
('PO-2025-005','Mace Group',95000.00,0.00,'PENDING',CURRENT_DATE - INTERVAL '28 days',NULL,'CC007','Facilities'),
('PO-2025-006','Vodafone UK Ltd',18500.00,0.00,'PENDING',CURRENT_DATE - INTERVAL '25 days',NULL,'CC008','IT Services'),
('PO-2025-007','Sodexo UK',35000.00,0.00,'PENDING',CURRENT_DATE - INTERVAL '23 days',NULL,'CC007','Facilities'),
('PO-2025-008','G4S UK',12000.00,0.00,'PENDING',CURRENT_DATE - INTERVAL '22 days',NULL,'CC007','Facilities'),
('PO-2025-009','Wipro UK',65000.00,0.00,'PENDING',CURRENT_DATE - INTERVAL '21 days',NULL,'CC001','IT Services'),
('PO-2025-010','Mitie Group',22000.00,0.00,'PENDING',CURRENT_DATE - INTERVAL '20 days',NULL,'CC007','Facilities'),
-- APPROVED (18)
('PO-2025-011','Tata Consultancy Services',150000.00,150000.00,'APPROVED','2025-03-01','2025-03-10','CC001','IT Services'),
('PO-2025-012','Infosys BPM UK',48000.00,48000.00,'APPROVED','2025-03-15','2025-03-25','CC008','IT Services'),
('PO-2025-013','KPMG UK',72000.00,72000.00,'APPROVED','2025-04-01','2025-04-12','CC009','Consulting'),
('PO-2025-014','Ernst & Young LLP',55000.00,55000.00,'APPROVED','2025-04-15','2025-04-25','CC009','Consulting'),
('PO-2025-015','PwC UK',88000.00,88000.00,'APPROVED','2025-05-01','2025-05-10','CC002','Consulting'),
('PO-2025-016','Capita Solutions Ltd',15000.00,15000.00,'APPROVED','2025-05-15','2025-05-22','CC004','Consulting'),
('PO-2025-017','Serco Group plc',32000.00,32000.00,'APPROVED','2025-06-01','2025-06-10','CC001','IT Services'),
('PO-2025-018','Accenture UK',110000.00,110000.00,'APPROVED','2025-06-15','2025-06-25','CC008','IT Services'),
('PO-2025-019','Computacenter UK',82000.00,82000.00,'APPROVED','2025-07-01','2025-07-12','CC008','Hardware'),
('PO-2025-020','BT Business',24000.00,24000.00,'APPROVED','2025-07-15','2025-07-22','CC008','IT Services'),
('PO-2025-021','Deloitte UK',95000.00,95000.00,'APPROVED','2025-08-01','2025-08-10','CC009','Consulting'),
('PO-2025-022','Mace Group',140000.00,140000.00,'APPROVED','2025-08-15','2025-08-25','CC007','Facilities'),
('PO-2025-023','Vodafone UK Ltd',42000.00,42000.00,'APPROVED','2025-09-01','2025-09-10','CC008','IT Services'),
('PO-2025-024','Wipro UK',58000.00,58000.00,'APPROVED','2025-09-15','2025-09-22','CC001','IT Services'),
('PO-2025-025','Sodexo UK',25000.00,25000.00,'APPROVED','2025-10-01','2025-10-08','CC007','Facilities'),
('PO-2025-026','Lloyds Banking Group',5000.00,5000.00,'APPROVED','2025-10-10','2025-10-15','CC002','Consulting'),
('PO-2025-027','Balfour Beatty',130000.00,130000.00,'APPROVED','2025-10-20','2025-10-30','CC007','Facilities'),
('PO-2025-028','Amey plc',18000.00,18000.00,'APPROVED','2025-11-01','2025-11-08','CC007','Facilities'),
-- REJECTED (5)
('PO-2025-029','G4S UK',45000.00,0.00,'REJECTED','2025-06-01','2025-06-15','CC007','Facilities'),
('PO-2025-030','Mitie Group',38000.00,0.00,'REJECTED','2025-07-01','2025-07-12','CC007','Facilities'),
('PO-2025-031','Tata Consultancy Services',200000.00,0.00,'REJECTED','2025-08-15','2025-08-28','CC001','IT Services'),
('PO-2025-032','Infosys BPM UK',75000.00,0.00,'REJECTED','2025-09-01','2025-09-15','CC008','IT Services'),
('PO-2025-033','Capita Solutions Ltd',52000.00,0.00,'REJECTED','2025-10-01','2025-10-12','CC004','Consulting'),
-- PARTIALLY_APPROVED (7)
('PO-2025-034','Serco Group plc',48000.00,35000.00,'PARTIALLY_APPROVED','2025-05-01','2025-05-15','CC001','IT Services'),
('PO-2025-035','Computacenter UK',92000.00,75000.00,'PARTIALLY_APPROVED','2025-06-15','2025-06-28','CC008','Hardware'),
('PO-2025-036','BT Business',62000.00,50000.00,'PARTIALLY_APPROVED','2025-07-01','2025-07-15','CC008','IT Services'),
('PO-2025-037','Accenture UK',145000.00,120000.00,'PARTIALLY_APPROVED','2025-08-01','2025-08-18','CC008','IT Services'),
('PO-2025-038','Deloitte UK',78000.00,65000.00,'PARTIALLY_APPROVED','2025-09-01','2025-09-12','CC009','Consulting'),
('PO-2025-039','Mace Group',110000.00,90000.00,'PARTIALLY_APPROVED','2025-10-01','2025-10-15','CC007','Facilities'),
('PO-2025-040','KPMG UK',55000.00,42000.00,'PARTIALLY_APPROVED','2025-11-01','2025-11-12','CC009','Consulting');
