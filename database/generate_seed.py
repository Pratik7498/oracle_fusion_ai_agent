"""Generate seed data SQL for all 62+ tables. Run: python database/generate_seed.py"""
import os, random, datetime as dt
random.seed(42)
D = dt.date

DEPTS = [
    ("D001","Engineering","ORG001","CC001"),("D002","Finance","ORG001","CC002"),
    ("D003","HR","ORG001","CC004"),("D004","Procurement","ORG001","CC005"),
    ("D005","Marketing","ORG001","CC003"),("D006","Sales","ORG001","CC006"),
    ("D007","Operations","ORG001","CC007"),("D008","IT","ORG001","CC008"),
    ("D009","Legal","ORG001","CC009"),("D010","Executive","ORG001","CC010"),
]

LOCATIONS = [
    ("LOC001","London HQ","1 Canary Wharf","London","E14 5AB","South East"),
    ("LOC002","Manchester Office","2 Piccadilly","Manchester","M1 1AG","North West"),
    ("LOC003","Birmingham Office","3 Broad St","Birmingham","B1 2HP","West Midlands"),
    ("LOC004","Remote","N/A","N/A","N/A","Remote"),
]

GRADES = [
    ("G3","Graduate",25000,30000,35000),("G4","Junior",35000,40000,48000),
    ("G5","Mid-Level",48000,58000,68000),("G6","Senior",68000,78000,90000),
    ("G7","Staff/Lead",85000,95000,110000),("G8","Director",100000,115000,140000),
]

JOBS = [
    ("JOB001","Software Engineer","Engineering","Mid"),
    ("JOB002","Senior Engineer","Engineering","Senior"),
    ("JOB003","Staff Engineer","Engineering","Lead"),
    ("JOB004","Engineering Director","Engineering","Director"),
    ("JOB005","Financial Analyst","Finance","Mid"),
    ("JOB006","Senior Accountant","Finance","Senior"),
    ("JOB007","HR Business Partner","HR","Senior"),
    ("JOB008","Procurement Manager","Procurement","Senior"),
    ("JOB009","Marketing Manager","Marketing","Senior"),
    ("JOB010","Sales Executive","Sales","Mid"),
    ("JOB011","Operations Analyst","Operations","Mid"),
    ("JOB012","DevOps Engineer","Engineering","Mid"),
    ("JOB013","QA Engineer","Engineering","Mid"),
    ("JOB014","Data Engineer","Engineering","Senior"),
    ("JOB015","Platform Engineer","Engineering","Senior"),
    ("JOB016","Security Engineer","Engineering","Senior"),
    ("JOB017","VP of Engineering","Engineering","Director"),
    ("JOB018","Graduate Engineer","Engineering","Junior"),
    ("JOB019","Junior Engineer","Engineering","Junior"),
    ("JOB020","Content Specialist","Marketing","Junior"),
]

# 80 persons: same names as original seed data
ENG_ACTIVE = [
    ("James Okonkwo","VP of Engineering","G8",118000,"2019-03-15","London",None),
    ("Sarah Chen","Engineering Director","G8",112000,"2019-06-01","London",1),
    ("Priya Sharma","Senior Staff Engineer","G7",102000,"2019-09-12","London",1),
    ("David Williams","Staff Engineer","G7",96000,"2020-01-20","Manchester",1),
    ("Fatima Al-Hassan","Staff Engineer","G7",94000,"2020-03-10","London",1),
    ("Michael Brown","Senior Engineer","G6",82000,"2020-05-18","Remote",2),
    ("Aisha Patel","Senior Engineer","G6",79000,"2020-06-22","London",2),
    ("Tom Richardson","Senior Engineer","G6",76000,"2020-08-03","Manchester",2),
    ("Elena Kowalski","Senior Engineer","G6",74000,"2020-09-14","Birmingham",2),
    ("Raj Gupta","Senior Engineer","G6",72000,"2020-11-01","London",3),
    ("Hannah Taylor","Engineer","G5",62000,"2021-01-15","Remote",6),
    ("Kwame Asante","Engineer","G5",60000,"2021-02-20","London",6),
    ("Sophie Martin","Engineer","G5",58000,"2021-04-05","Manchester",7),
    ("Omar Hussain","Engineer","G5",56000,"2021-05-10","London",7),
    ("Charlotte Evans","Engineer","G5",55000,"2021-06-14","Remote",8),
    ("Yuki Tanaka","Engineer","G5",54000,"2021-07-19","Birmingham",8),
    ("Daniel Murphy","Engineer","G5",52000,"2021-08-23","London",9),
    ("Blessing Obi","Engineer","G5",51000,"2021-10-01","Remote",9),
    ("Liam O'Brien","Engineer","G5",50000,"2021-11-15","Manchester",10),
    ("Anya Petrova","Engineer","G5",49000,"2022-01-10","London",10),
    ("Jack Hughes","Junior Engineer","G4",45000,"2022-03-01","London",11),
    ("Mei Lin","Junior Engineer","G4",44000,"2022-04-15","Remote",11),
    ("Ryan Kelly","Junior Engineer","G4",43000,"2022-05-20","Birmingham",12),
    ("Zara Khan","Junior Engineer","G4",42000,"2022-07-01","London",12),
    ("Oliver Wood","Junior Engineer","G4",41000,"2022-08-15","Manchester",13),
    ("Nkechi Eze","Junior Engineer","G4",40000,"2022-09-20","London",13),
    ("Isla Campbell","Junior Engineer","G4",39000,"2022-11-01","Remote",14),
    ("Arjun Singh","Junior Engineer","G4",38000,"2023-01-10","London",14),
    ("Emily Watson","Junior Engineer","G4",37000,"2023-02-20","Manchester",15),
    ("Kofi Mensah","Junior Engineer","G4",36000,"2023-04-01","Birmingham",15),
    ("Grace Liu","Graduate Engineer","G3",34000,"2023-06-15","London",16),
    ("Nathan Clarke","Graduate Engineer","G3",33000,"2023-07-20","Remote",16),
    ("Amara Diallo","Graduate Engineer","G3",32000,"2023-09-01","London",17),
    ("Harry Thompson","Graduate Engineer","G3",31000,"2023-10-15","Manchester",17),
    ("Suki Nakamura","Graduate Engineer","G3",30000,"2023-11-20","London",18),
    ("Ben Carter","Graduate Engineer","G3",29000,"2024-01-08","Remote",18),
    ("Rosa Fernandez","Graduate Engineer","G3",28500,"2024-02-15","Birmingham",19),
    ("Callum Stewart","Graduate Engineer","G3",28000,"2024-03-20","London",19),
    ("Adaeze Nwankwo","DevOps Engineer","G5",63000,"2021-03-10","London",3),
    ("Marcus Johnson","DevOps Engineer","G5",61000,"2021-12-01","Remote",3),
    ("Freya Nielsen","QA Engineer","G5",57000,"2022-02-14","Manchester",4),
    ("Ibrahim Yusuf","QA Engineer","G4",46000,"2022-06-01","London",4),
    ("Lucy Adams","Data Engineer","G6",78000,"2020-07-15","London",3),
    ("Tomasz Nowak","Data Engineer","G5",59000,"2021-09-20","Remote",43),
    ("Chloe Baker","Platform Engineer","G6",80000,"2020-04-01","London",2),
    ("Ravi Krishnan","Platform Engineer","G5",64000,"2022-01-15","Birmingham",45),
    ("Olivia Scott","Security Engineer","G6",83000,"2020-10-01","London",1),
]
OTHER_ACTIVE = [
    ("Victoria Chang","Finance","Finance Director","G8",115000,"2019-04-01","London",None),
    ("George Whitfield","Finance","Senior Accountant","G6",75000,"2020-02-15","London",48),
    ("Amina Begum","Finance","Financial Analyst","G5",58000,"2021-05-20","Manchester",48),
    ("Patricia Okafor","HR","HR Director","G8",110000,"2019-07-10","London",None),
    ("Simon Gallagher","HR","HR Business Partner","G6",71000,"2020-11-20","Remote",51),
    ("Henry Osei","Procurement","Procurement Manager","G7",88000,"2019-11-01","London",None),
    ("Jessica Park","Marketing","Marketing Director","G8",108000,"2019-08-15","London",None),
    ("Tariq Ali","Marketing","Marketing Manager","G6",70000,"2021-01-10","Remote",54),
    ("Fiona McLeod","Marketing","Content Specialist","G4",42000,"2023-03-15","Manchester",54),
    ("Robert Achebe","Sales","Sales Director","G8",116000,"2019-05-20","London",None),
    ("Natasha Volkov","Sales","Account Executive","G5",55000,"2022-04-01","Birmingham",57),
    ("William Nkomo","Operations","Operations Director","G8",109000,"2019-10-10","London",None),
    ("Catherine Doyle","Operations","Operations Analyst","G5",53000,"2022-08-01","Remote",59),
]
TERMINATED = [
    ("Peter Nowak","Engineering","Engineer","G5",55000,"2021-03-15","2025-03-01","London",6),
    ("Sandra Kim","Engineering","Junior Engineer","G4",40000,"2022-09-01","2025-04-15","Remote",11),
    ("Derek Shaw","Engineering","Graduate Engineer","G3",30000,"2023-06-01","2025-05-20","Manchester",16),
    ("Monica Reyes","Engineering","Engineer","G5",54000,"2021-07-10","2025-06-10","Birmingham",7),
    ("Alan Foster","Engineering","Junior Engineer","G4",41000,"2022-11-15","2025-07-01","London",12),
    ("Ingrid Larsen","Engineering","DevOps Engineer","G5",58000,"2021-04-01","2025-08-15","Remote",3),
    ("Chidi Okonkwo","Engineering","QA Engineer","G4",44000,"2022-05-10","2025-09-01","London",4),
    ("Karen Mitchell","Engineering","Data Engineer","G5",57000,"2021-08-20","2025-10-15","Manchester",43),
    ("Youssef El-Amin","Engineering","Platform Engineer","G5",60000,"2021-11-05","2025-11-20","London",45),
    ("Lisa Zhang","Engineering","Engineer","G5",53000,"2022-01-20","2025-12-01","Remote",8),
    ("Paul Bennett","Finance","Accountant","G5",52000,"2021-06-15","2025-04-01","London",48),
    ("Diana Rossi","Finance","Financial Analyst","G4",45000,"2022-03-10","2025-07-15","Manchester",48),
    ("Trevor Grant","HR","HR Coordinator","G4",40000,"2022-08-01","2025-05-01","Birmingham",51),
    ("Nina Johansson","HR","Recruiter","G4",42000,"2022-10-20","2025-09-15","London",51),
    ("Samuel Obeng","Procurement","Procurement Analyst","G4",43000,"2022-07-15","2025-06-20","Remote",53),
    ("Rachel Cooper","Procurement","Buyer","G4",41000,"2023-01-10","2025-10-01","London",53),
    ("Ahmed Hassan","Marketing","Digital Marketer","G4",39000,"2023-02-15","2025-08-01","Manchester",54),
    ("Wendy Griffiths","Marketing","Marketing Analyst","G4",38000,"2023-05-01","2025-11-15","London",54),
    ("Ian Wallace","Sales","Sales Rep","G4",40000,"2023-01-20","2025-07-20","Remote",57),
    ("Joanna Price","Operations","Ops Coordinator","G3",30000,"2023-08-10","2025-12-15","Birmingham",59),
]

LOC_MAP = {"London":"LOC001","Manchester":"LOC002","Birmingham":"LOC003","Remote":"LOC004"}
GRADE_MAP = {g[0]:i+1 for i,g in enumerate(GRADES)}

SUPPLIERS = [
    ("SUP001","Capita Solutions Ltd","IT_SERVICES","NET30","LOW"),
    ("SUP002","Serco Group plc","IT_SERVICES","NET30","LOW"),
    ("SUP003","Computacenter UK","HARDWARE","NET30","LOW"),
    ("SUP004","BT Business","TELECOM","NET30","LOW"),
    ("SUP005","Vodafone UK Ltd","TELECOM","NET30","LOW"),
    ("SUP006","Lloyds Banking Group","FINANCIAL","NET30","LOW"),
    ("SUP007","Deloitte UK","CONSULTING","NET30","LOW"),
    ("SUP008","PwC UK","CONSULTING","NET30","LOW"),
    ("SUP009","KPMG UK","CONSULTING","NET30","MEDIUM"),
    ("SUP010","Ernst & Young LLP","CONSULTING","NET30","LOW"),
    ("SUP011","Accenture UK","IT_SERVICES","NET45","LOW"),
    ("SUP012","Wipro UK","IT_SERVICES","NET30","MEDIUM"),
    ("SUP013","Tata Consultancy Services","IT_SERVICES","NET30","LOW"),
    ("SUP014","Infosys BPM UK","IT_SERVICES","NET30","MEDIUM"),
    ("SUP015","Mace Group","FACILITIES","NET30","LOW"),
    ("SUP016","G4S UK","FACILITIES","NET30","HIGH"),
    ("SUP017","Balfour Beatty","CONSTRUCTION","NET45","LOW"),
    ("SUP018","Amey plc","FACILITIES","NET30","MEDIUM"),
    ("SUP019","Mitie Group","FACILITIES","NET30","LOW"),
    ("SUP020","Sodexo UK","FACILITIES","NET30","LOW"),
]

def esc(s):return s.replace("'","''")
def val(v):
    if v is None: return "NULL"
    if isinstance(v,bool): return "TRUE" if v else "FALSE"
    if isinstance(v,(int,float)): return str(v)
    return f"'{esc(str(v))}'"
def ins(table,cols,rows):
    lines = [f"INSERT INTO {table} ({','.join(cols)}) VALUES"]
    for i,r in enumerate(rows):
        sep = "," if i < len(rows)-1 else ";"
        lines.append(f"  ({','.join(val(v) for v in r)}){sep}")
    return "\n".join(lines)+"\n\n"

def generate():
    S = []
    S.append("-- ================================================================\n")
    S.append("-- Oracle Fusion AI Agent -- Seed Data for 62-table schema\n")
    S.append("-- ================================================================\n\n")

    # HCM Organizations
    S.append(ins("hcm_organizations",["org_code","org_name","org_type","parent_org_id","country","status"],[
        ("ORG001","Oracle Fusion UK Ltd","LEGAL_ENTITY",None,"United Kingdom","ACTIVE"),
        ("ORG002","Engineering Division","BUSINESS_UNIT",1,"United Kingdom","ACTIVE"),
        ("ORG003","Finance Division","BUSINESS_UNIT",1,"United Kingdom","ACTIVE"),
        ("ORG004","Commercial Division","BUSINESS_UNIT",1,"United Kingdom","ACTIVE"),
    ]))

    # Locations
    S.append(ins("hcm_locations",["location_code","location_name","address_line1","city","postal_code","region","status"],
        [(l[0],l[1],l[2],l[3],l[4],l[5],"ACTIVE") for l in LOCATIONS]))

    # Jobs
    S.append(ins("hcm_jobs",["job_code","job_name","job_family","job_level","min_salary","max_salary","status"],
        [(j[0],j[1],j[2],j[3],30000,120000,"ACTIVE") for j in JOBS]))

    # Grades
    S.append(ins("hcm_grades",["grade_code","grade_name","min_salary","mid_salary","max_salary","currency"],
        [(g[0],g[1],g[2],g[3],g[4],"GBP") for g in GRADES]))

    # Departments
    S.append(ins("hcm_departments",["dept_code","dept_name","org_id","cost_centre_code","status"],
        [(d[0],d[1],1,d[3],"ACTIVE") for d in DEPTS]))

    # Positions (1 per dept for simplicity, more for Eng)
    positions = []
    pid=0
    for d in DEPTS:
        pid+=1
        positions.append((f"POS{pid:03d}",f"{d[1]} Lead",pid if pid<=10 else 1,1,
                          LOC_MAP.get("London"),None,"ACTIVE"))
    S.append(ins("hcm_positions",["position_code","position_name","dept_id","job_id","location_id","grade_id","status"],
        [(p[0],p[1],p[2],p[3],1,None,"ACTIVE") for p in positions]))

    # Persons + Names + Emails + Employment Periods + Assignments
    persons, names, emails, periods, assignments = [],[],[],[],[]
    person_id = 0

    def add_person(full_name, dept, title, grade, salary, hire, loc, mgr, term_date=None, status="ACTIVE"):
        nonlocal person_id
        person_id += 1
        fn = full_name.split(" ",1)
        first,last = fn[0],fn[1] if len(fn)>1 else fn[0]
        pnum = f"EMP{person_id:04d}"
        persons.append((pnum,first,last,None,"M" if person_id%3!=0 else "F","British",None,None,"EMPLOYEE",status))
        names.append((person_id,"GLOBAL",None,first,None,last,None,hire,term_date))
        email = f"{first.lower()}.{last.lower().replace(' ','').replace(chr(39),'')}@oraclefusion.co.uk"
        emails.append((person_id,"WORK",email,True))
        periods.append((person_id,"EMPLOYEE",hire,term_date,status))
        dept_idx = next((i+1 for i,d in enumerate(DEPTS) if d[1]==dept),1)
        loc_idx = LOC_MAP.get(loc,LOC_MAP["London"])
        loc_id = list(LOC_MAP.values()).index(loc_idx)+1
        grade_id = GRADE_MAP.get(grade,1)
        assignments.append((f"ASN{person_id:04d}",person_id,None,dept_idx,1,grade_id,None,loc_id,
                           "PRIMARY",status if term_date is None else "INACTIVE",
                           "ACTIVE" if term_date is None else "TERMINATED",
                           title,salary,"GBP",mgr,hire,term_date))

    for e in ENG_ACTIVE:
        add_person(e[0],"Engineering",e[1],e[2],e[3],e[4],e[5],e[6])
    for e in OTHER_ACTIVE:
        add_person(e[0],e[1],e[2],e[3],e[4],e[5],e[6],e[7])
    for e in TERMINATED:
        add_person(e[0],e[1],e[2],e[3],e[4],e[5],e[7],e[8],term_date=e[6],status="INACTIVE")

    S.append(ins("hcm_persons",["person_number","first_name","last_name","date_of_birth","gender","nationality",
        "national_id","marital_status","person_type","status"], persons))
    S.append(ins("hcm_person_names",["person_id","name_type","title","first_name","middle_name","last_name",
        "suffix","effective_from","effective_to"], names))
    S.append(ins("hcm_person_emails",["person_id","email_type","email_address","is_primary"], emails))
    S.append(ins("hcm_employment_periods",["person_id","period_type","start_date","end_date","status"], periods))
    S.append(ins("hcm_assignments",["assignment_number","person_id","position_id","dept_id","org_id","grade_id",
        "job_id","location_id","assignment_type","assignment_status","employment_status","job_title","salary",
        "salary_currency","manager_person_id","effective_from","effective_to"], assignments))

    # Termination reasons
    S.append(ins("hcm_termination_reasons",["reason_code","reason_name","reason_category","is_voluntary"],[
        ("VOL_RES","Voluntary Resignation","VOLUNTARY",True),
        ("REDUNDANCY","Redundancy","INVOLUNTARY",False),
        ("RETIREMENT","Retirement","VOLUNTARY",True),
        ("END_CONTRACT","End of Contract","INVOLUNTARY",False),
        ("MISCONDUCT","Gross Misconduct","INVOLUNTARY",False),
    ]))

    # Workforce actions for terminated employees
    wa = []
    for i,e in enumerate(TERMINATED):
        pid = 47+13+i+1  # offset
        wa.append((pid,pid,"HIRE",None,e[5],None,None,None,None))
        wa.append((pid,pid,"TERMINATE","Voluntary",e[6],1,None,None,None))
    S.append(ins("hcm_workforce_actions",["person_id","assignment_id","action_type","action_reason",
        "effective_date","reason_id","old_value","new_value","processed_by"], wa))

    # Salary history (sample for first 10 eng)
    sh = []
    for i in range(1,11):
        sh.append((i,None,ENG_ACTIVE[i-1][3],"HIRE",ENG_ACTIVE[i-1][4],"GBP",None))
    S.append(ins("hcm_salary_history",["assignment_id","old_salary","new_salary","change_reason",
        "effective_date","currency","approved_by"], sh))

    # Performance reviews (sample)
    pr = []
    for i in range(1,21):
        pr.append((i,1 if i>1 else None,"FY2025","ANNUAL","Exceeds Expectations",4.2,88.5,None,"COMPLETED","2025-06-15"))
    S.append(ins("hcm_performance_reviews",["person_id","reviewer_person_id","review_period","review_type",
        "overall_rating","rating_score","goals_met_pct","comments","status","review_date"], pr))

    # Training records (sample)
    tr = []
    for i in range(1,16):
        tr.append((i,"Cloud Architecture Fundamentals","Technical","AWS","2025-03-15",92.5,"COMPLETED",f"CERT-{i:04d}"))
    S.append(ins("hcm_training_records",["person_id","course_name","course_category","provider",
        "completion_date","score","status","certificate_id"], tr))

    # Payroll runs
    S.append(ins("hcm_payroll_runs",["run_name","period_name","run_date","status","total_gross",
        "total_deductions","total_net","employee_count"],[
        ("January 2025 Payroll","JAN-2025","2025-01-28","COMPLETED",420000,126000,294000,60),
        ("February 2025 Payroll","FEB-2025","2025-02-28","COMPLETED",420000,126000,294000,60),
    ]))

    # Compensation elements (sample)
    ce = []
    for i in range(1,11):
        ce.append((i,"BASE_SALARY","Base Pay",ENG_ACTIVE[i-1][3],"MONTHLY","GBP","2025-01-01",None))
    S.append(ins("hcm_compensation_elements",["assignment_id","element_type","element_name","amount",
        "frequency","currency","effective_from","effective_to"], ce))

    # ---- FINANCE ----
    S.append("\n-- ================================================================\n")
    S.append("-- FINANCE SEED DATA\n")
    S.append("-- ================================================================\n\n")

    # Ledger
    S.append(ins("fin_ledgers",["ledger_code","ledger_name","currency","calendar_type","status"],[
        ("LED001","UK Primary Ledger","GBP","FISCAL","ACTIVE"),
    ]))

    # COA
    S.append(ins("fin_chart_of_accounts",["coa_code","coa_name","ledger_id","status"],[
        ("COA001","UK Standard COA",1,"ACTIVE"),
    ]))

    # COA Segments
    S.append(ins("fin_coa_segments",["coa_id","segment_name","segment_number","segment_type","value_set"],[
        (1,"Company",1,"BALANCING","COMPANY_VS"),
        (1,"Cost Centre",2,"COST_CENTER","CC_VS"),
        (1,"Account",3,"NATURAL_ACCOUNT","ACCT_VS"),
        (1,"Project",4,"OPTIONAL","PROJ_VS"),
    ]))

    # Cost Centres
    S.append(ins("fin_cost_centres",["cost_centre_code","cost_centre_name","dept_id","manager_person_id","status"],
        [(d[3],d[1],i+1,None,"ACTIVE") for i,d in enumerate(DEPTS)]))

    # Account Codes
    accts = [
        ("5001","Salaries & Wages","EXPENSE",1),("5002","Benefits","EXPENSE",1),
        ("5003","Travel & Entertainment","EXPENSE",1),("5004","Software Licenses","EXPENSE",1),
        ("5005","Hardware","EXPENSE",1),("5006","Consulting Fees","EXPENSE",1),
        ("5007","Facilities","EXPENSE",1),("5008","Marketing Spend","EXPENSE",1),
        ("5009","Legal Fees","EXPENSE",1),("5010","Depreciation","EXPENSE",1),
        ("4001","Product Revenue","REVENUE",1),("4002","Service Revenue","REVENUE",1),
        ("1001","Cash & Bank","ASSET",1),("1002","Accounts Receivable","ASSET",1),
        ("2001","Accounts Payable","LIABILITY",1),("2002","Accrued Expenses","LIABILITY",1),
    ]
    S.append(ins("fin_account_codes",["account_code","account_name","account_type","coa_id"],
        [(a[0],a[1],a[2],a[3]) for a in accts]))

    # Reporting periods
    rp = []
    months = ["JAN","FEB","MAR","APR","MAY","JUN","JUL","AUG","SEP","OCT","NOV","DEC"]
    for yr in [2025,2026]:
        for mi,m in enumerate(months):
            q = mi//3+1
            sd = D(yr,mi+1,1)
            ed = D(yr,mi+1,28)
            rp.append((f"{m}-{yr}",yr,q,mi+1,sd,ed,"OPEN" if yr==2026 else "CLOSED"))
            if yr==2026 and mi>=0: break
    S.append(ins("fin_reporting_periods",["period_name","fiscal_year","fiscal_quarter","period_number",
        "start_date","end_date","status"], rp))

    # Currency rates
    S.append(ins("fin_currency_rates",["from_currency","to_currency","exchange_rate","rate_type","effective_date"],[
        ("GBP","USD",1.27,"SPOT","2025-01-01"),("GBP","EUR",1.16,"SPOT","2025-01-01"),
        ("USD","GBP",0.79,"SPOT","2025-01-01"),("EUR","GBP",0.86,"SPOT","2025-01-01"),
    ]))

    # GL Balances (same 130 rows as original but adapted)
    cc_data = [
        ("CC001","Engineering","5001","Salaries & Wages",
         [420000,418000,425000,432000,428000,436000,440000,438000,442000,445000,443000,448000,450000],
         [430000,430000,430000,435000,435000,435000,440000,440000,440000,445000,445000,450000,450000]),
        ("CC002","Finance","5002","Finance Operations",
         [85000,87000,88000,89000,86000,91000,88000,87000,90000,89000,88000,92000,90000],
         [90000,90000,90000,90000,90000,90000,90000,90000,90000,90000,90000,90000,92000]),
        ("CC003","Marketing","5008","Marketing Spend",
         [140000,142000,145000,148000,147000,149000,151000,148000,152000,162000,158000,171000,155000],
         [150000,150000,150000,150000,150000,150000,150000,150000,150000,150000,150000,155000,155000]),
        ("CC004","HR","5002","HR Services",
         [60000,62000,63000,64000,61000,66000,63000,64000,65000,66000,64000,67000,65000],
         [65000,65000,65000,65000,65000,65000,65000,65000,65000,65000,65000,65000,66000]),
        ("CC005","Procurement","5006","Procurement Ops",
         [50000,51000,53000,54000,52000,55000,53000,54000,56000,55000,54000,57000,55000],
         [55000,55000,55000,55000,55000,55000,55000,55000,55000,55000,55000,55000,56000]),
        ("CC006","Sales","5001","Sales Costs",
         [180000,182000,184000,183000,186000,181000,185000,184000,187000,186000,185000,189000,187000],
         [185000,185000,185000,185000,185000,185000,185000,185000,185000,188000,188000,190000,190000]),
        ("CC007","Operations","5007","Operations",
         [95000,97000,98000,99000,96000,101000,98000,99000,100000,102000,99000,103000,100000],
         [100000,100000,100000,100000,100000,100000,100000,100000,100000,100000,100000,100000,102000]),
        ("CC008","IT","5004","IT Infrastructure",
         [200000,205000,208000,210000,207000,212000,209000,211000,214000,216000,213000,218000,215000],
         [210000,210000,210000,215000,215000,215000,215000,215000,215000,215000,215000,220000,220000]),
        ("CC009","Legal","5009","Legal Services",
         [70000,72000,74000,73000,71000,76000,74000,73000,75000,76000,74000,77000,75000],
         [75000,75000,75000,75000,75000,75000,75000,75000,75000,75000,75000,75000,76000]),
        ("CC010","Executive","5001","Executive Office",
         [300000,305000,310000,315000,312000,318000,310000,316000,320000,322000,318000,328000,325000],
         [320000,320000,320000,320000,320000,320000,320000,320000,320000,325000,325000,330000,330000]),
    ]
    pnames = [f"{m}-2025" for m in months]+["JAN-2026"]
    gl_rows = []
    cc_id_map = {d[3]:i+1 for i,d in enumerate(DEPTS)}
    ac_code_map = {a[0]:i+1 for i,a in enumerate(accts)}
    for cc in cc_data:
        cc_id = cc_id_map.get(cc[0],1)
        ac_id = ac_code_map.get(cc[2],1)
        for pi in range(13):
            yr = 2025 if pi<12 else 2026
            q = pi//3+1 if pi<12 else 1
            actual = cc[4][pi]
            budget = cc[5][pi]
            gl_rows.append((cc_id,ac_id,pnames[pi],yr,q,actual,0,actual,budget,actual,actual,"GBP"))
    S.append(ins("fin_gl_balances",["cost_centre_id","account_code_id","period_name","fiscal_year",
        "fiscal_quarter","period_debit","period_credit","period_net","begin_balance","end_balance",
        "outstanding" if False else "end_balance","currency"],
        # Simplify: just use the adapted structure
        []))  # Will generate inline

    # Actually let me do GL balances properly
    S.pop()  # remove empty one
    gl_rows2 = []
    for cc in cc_data:
        cc_id = cc_id_map.get(cc[0],1)
        ac_id = ac_code_map.get(cc[2],1)
        for pi in range(13):
            yr = 2025 if pi<12 else 2026
            q = pi//3+1 if pi<12 else 1
            actual = cc[4][pi]
            budget = cc[5][pi]
            gl_rows2.append((cc_id,ac_id,pnames[pi],yr,q,actual,0,actual,0,actual,"GBP"))
    S.append(ins("fin_gl_balances",["cost_centre_id","account_code_id","period_name","fiscal_year",
        "fiscal_quarter","period_debit","period_credit","period_net","begin_balance","end_balance","currency"], gl_rows2))

    # Budget versions
    S.append(ins("fin_budget_versions",["version_name","version_type","fiscal_year","status"],[
        ("FY2025 Original","ORIGINAL",2025,"APPROVED"),
        ("FY2025 Revised Q3","REVISED",2025,"APPROVED"),
        ("FY2026 Original","ORIGINAL",2026,"DRAFT"),
    ]))

    # Budget headers
    S.append(ins("fin_budget_headers",["budget_name","ledger_id","budget_version_id","fiscal_year","total_amount","status"],[
        ("FY2025 Operating Budget",1,1,2025,25000000,"APPROVED"),
        ("FY2026 Operating Budget",1,3,2026,27000000,"DRAFT"),
    ]))

    # Budget lines (sample per CC)
    bl = []
    for i,d in enumerate(DEPTS):
        cc_id = i+1
        bl.append((1,cc_id,1,"JAN-2025",cc_data[i][5][0]))
    S.append(ins("fin_budget_lines",["budget_header_id","cost_centre_id","account_code_id","period_name","amount"], bl))

    # ---- SUPPLIERS (UNIFIED) ----
    S.append("\n-- UNIFIED SUPPLIER MASTER\n")
    S.append(ins("sup_suppliers",["supplier_number","supplier_name","tax_registration","payment_terms",
        "supplier_type","risk_rating","qualification_status","status","country"],
        [(s[0],s[1],f"GB{100000000+i}",s[3],s[2],s[4],"QUALIFIED","ACTIVE","United Kingdom") for i,s in enumerate(SUPPLIERS)]))

    # Supplier sites
    ss = []
    for i,s in enumerate(SUPPLIERS):
        ss.append((i+1,f"SITE-{s[0]}",f"{s[1]} Main Office",f"{i+1} Business Park","London","EC1A 1BB","United Kingdom",True,"ACTIVE"))
    S.append(ins("sup_supplier_sites",["supplier_id","site_code","site_name","address_line1","city","postal_code","country","is_primary","status"], ss))

    # Supplier contacts
    sc = []
    fnames = ["John","Jane","Mark","Sarah","David","Emma","Robert","Lisa","James","Anna",
              "Michael","Kate","Thomas","Rachel","Andrew","Helen","Peter","Susan","Paul","Lucy"]
    for i,s in enumerate(SUPPLIERS):
        sc.append((i+1,f"{fnames[i]} Smith","Account Manager",f"{fnames[i].lower()}.smith@{s[1].split()[0].lower()}.co.uk","+44 20 7946 0958",True))
    S.append(ins("sup_supplier_contacts",["supplier_id","contact_name","job_title","email","phone","is_primary"], sc))

    # ---- AP INVOICES ----
    S.append("\n-- AP INVOICES\n")
    inv_data = [
        ("INV-2025-001",1,"2025-01-10","2025-02-10",25000,25000,0,"PAID"),
        ("INV-2025-002",2,"2025-01-15","2025-02-15",18500,18500,0,"PAID"),
        ("INV-2025-003",3,"2025-02-01","2025-03-01",42000,42000,0,"PAID"),
        ("INV-2025-004",4,"2025-02-10","2025-03-10",8500,8500,0,"PAID"),
        ("INV-2025-005",5,"2025-03-01","2025-04-01",12000,12000,0,"PAID"),
        ("INV-2025-006",6,"2025-03-15","2025-04-15",3200,3200,0,"PAID"),
        ("INV-2025-007",7,"2025-04-01","2025-05-01",65000,65000,0,"PAID"),
        ("INV-2025-008",8,"2025-04-15","2025-05-15",48000,48000,0,"PAID"),
        ("INV-2025-009",9,"2025-05-01","2025-06-01",35000,35000,0,"PAID"),
        ("INV-2025-010",10,"2025-05-15","2025-06-15",28000,28000,0,"PAID"),
        ("INV-2025-011",1,"2025-06-01","2025-07-01",15000,15000,0,"PAID"),
        ("INV-2025-012",11,"2025-06-15","2025-07-15",72000,72000,0,"PAID"),
        ("INV-2025-013",12,"2025-07-01","2025-08-01",22000,22000,0,"PAID"),
        ("INV-2025-014",13,"2025-07-15","2025-08-15",55000,55000,0,"PAID"),
        ("INV-2025-015",14,"2025-08-01","2025-09-01",31000,31000,0,"PAID"),
        ("INV-2025-016",15,"2025-09-01","2025-10-01",19500,0,19500,"APPROVED"),
        ("INV-2025-017",2,"2025-09-10","2025-10-10",24000,0,24000,"APPROVED"),
        ("INV-2025-018",3,"2025-09-15","2025-10-15",38000,0,38000,"APPROVED"),
        ("INV-2025-019",16,"2025-09-20","2025-10-20",7800,0,7800,"APPROVED"),
        ("INV-2025-020",4,"2025-10-01","2025-11-01",14200,0,14200,"APPROVED"),
        ("INV-2025-021",17,"2025-10-05","2025-11-05",85000,0,85000,"APPROVED"),
        ("INV-2025-022",5,"2025-10-10","2025-11-10",9800,0,9800,"APPROVED"),
        ("INV-2025-023",18,"2025-10-15","2025-11-15",16500,0,16500,"APPROVED"),
        ("INV-2025-024",6,"2025-10-20","2025-11-20",4500,0,4500,"APPROVED"),
        ("INV-2025-025",19,"2025-11-01","2025-12-01",21000,0,21000,"APPROVED"),
        ("INV-2025-026",7,"2025-11-10","2025-12-10",58000,0,58000,"APPROVED"),
        ("INV-2025-027",20,"2025-11-15","2025-12-15",11200,0,11200,"APPROVED"),
        ("INV-2025-028",8,"2025-11-20","2026-01-20",45000,0,45000,"PENDING"),
        ("INV-2025-029",9,"2025-11-25","2026-01-25",33000,0,33000,"PENDING"),
        ("INV-2025-030",10,"2025-12-01","2026-02-01",27500,0,27500,"PENDING"),
    ]
    S.append(ins("fin_ap_invoices",["invoice_number","supplier_id","ledger_id","invoice_date","due_date",
        "invoice_amount","paid_amount","outstanding_amount","currency","status"],
        [(d[0],d[1],1,d[2],d[3],d[4],d[5],d[6],"GBP",d[7]) for d in inv_data]))

    # AP invoice lines (1 line per invoice)
    ail = []
    for i,d in enumerate(inv_data):
        ail.append((i+1,1,f"Services - {d[0]}",1,d[4],d[4],None))
    S.append(ins("fin_ap_invoice_lines",["invoice_id","line_number","description","quantity","unit_price","line_amount","po_line_id"], ail))

    # AP payments (for PAID invoices)
    ap_pay = []
    for i in range(15):
        ap_pay.append((f"PAY-2025-{i+1:03d}",inv_data[i][1],inv_data[i][3],inv_data[i][4],"BACS",f"BACS-{i+1:04d}","COMPLETED"))
    S.append(ins("fin_ap_payments",["payment_number","supplier_id","payment_date","payment_amount","payment_method","reference","status"], ap_pay))

    # AR Customers
    S.append(ins("fin_ar_customers",["customer_number","customer_name","customer_type","payment_terms","credit_limit","status"],[
        ("CUST001","British Airways plc","ENTERPRISE","NET30",500000,"ACTIVE"),
        ("CUST002","Tesco plc","ENTERPRISE","NET30",300000,"ACTIVE"),
        ("CUST003","HSBC Holdings","ENTERPRISE","NET30",750000,"ACTIVE"),
        ("CUST004","National Grid","ENTERPRISE","NET45",400000,"ACTIVE"),
        ("CUST005","GlaxoSmithKline","ENTERPRISE","NET30",600000,"ACTIVE"),
    ]))

    # AR Invoices
    S.append(ins("fin_ar_invoices",["invoice_number","customer_id","invoice_date","due_date","invoice_amount","paid_amount","outstanding","currency","status"],[
        ("AR-2025-001",1,"2025-03-01","2025-04-01",120000,120000,0,"GBP","CLOSED"),
        ("AR-2025-002",2,"2025-04-15","2025-05-15",85000,85000,0,"GBP","CLOSED"),
        ("AR-2025-003",3,"2025-06-01","2025-07-01",200000,150000,50000,"GBP","OPEN"),
        ("AR-2025-004",4,"2025-08-01","2025-09-01",95000,0,95000,"GBP","OPEN"),
        ("AR-2025-005",5,"2025-10-01","2025-11-01",175000,0,175000,"GBP","OPEN"),
    ]))

    # AR Receipts
    S.append(ins("fin_ar_receipts",["receipt_number","ar_invoice_id","receipt_date","receipt_amount","payment_method","status"],[
        ("RCT-001",1,"2025-03-28",120000,"BACS","APPLIED"),
        ("RCT-002",2,"2025-05-10",85000,"BACS","APPLIED"),
        ("RCT-003",3,"2025-06-28",150000,"CHAPS","APPLIED"),
    ]))

    # ---- PROCUREMENT ----
    S.append("\n-- ================================================================\n")
    S.append("-- PROCUREMENT SEED DATA\n")
    S.append("-- ================================================================\n\n")

    # Item categories
    S.append(ins("proc_item_categories",["category_code","category_name","parent_category_id","status"],[
        ("CAT001","IT Services",None,"ACTIVE"),("CAT002","Hardware",None,"ACTIVE"),
        ("CAT003","Consulting",None,"ACTIVE"),("CAT004","Facilities",None,"ACTIVE"),
        ("CAT005","Telecom",None,"ACTIVE"),("CAT006","Software",1,"ACTIVE"),
        ("CAT007","Cloud Services",1,"ACTIVE"),("CAT008","Server Hardware",2,"ACTIVE"),
    ]))

    # Items
    S.append(ins("proc_items",["item_code","item_name","description","category_id","unit_of_measure","unit_price","item_type","status"],[
        ("ITM001","Cloud Migration Service","AWS/Azure migration consulting",1,"EACH",50000,"SERVICE","ACTIVE"),
        ("ITM002","Desktop PC","Dell OptiPlex workstation",2,"EACH",1200,"GOODS","ACTIVE"),
        ("ITM003","Audit Services","Annual external audit",3,"EACH",95000,"SERVICE","ACTIVE"),
        ("ITM004","Office Refurbishment","Workspace renovation",4,"EACH",220000,"SERVICE","ACTIVE"),
        ("ITM005","Network Assessment","Security assessment service",5,"EACH",45000,"SERVICE","ACTIVE"),
        ("ITM006","Software License","Enterprise license pack",6,"EACH",15000,"SERVICE","ACTIVE"),
        ("ITM007","Cloud Hosting","Monthly cloud compute",7,"MONTH",8000,"SERVICE","ACTIVE"),
        ("ITM008","Server","Dell PowerEdge R750",8,"EACH",12000,"GOODS","ACTIVE"),
    ]))

    # Requisitions
    S.append(ins("proc_requisition_headers",["requisition_number","requester_id","dept_id","description","total_amount","status","submitted_date","approved_date","approved_by"],[
        ("REQ-2025-001",1,1,"Cloud infrastructure upgrade",82000,"APPROVED","2025-09-01","2025-09-05",1),
        ("REQ-2025-002",48,2,"Annual audit services",95000,"APPROVED","2025-04-01","2025-04-05",48),
        ("REQ-2025-003",1,1,"SAP upgrade project",150000,"APPROVED","2025-05-01","2025-05-10",1),
        ("REQ-2025-004",59,7,"Office refurbishment",220000,"APPROVED","2025-03-01","2025-03-10",59),
        ("REQ-2025-005",53,4,"Desktop hardware refresh",65000,"APPROVED","2025-09-15","2025-09-20",53),
    ]))

    # Requisition lines
    S.append(ins("proc_requisition_lines",["requisition_id","line_number","item_id","description","quantity","unit_price","line_amount","need_by_date"],[
        (1,1,1,"Cloud Migration Phase 2",1,82000,82000,"2025-12-31"),
        (2,1,3,"FY2025 External Audit",1,95000,95000,"2025-06-30"),
        (3,1,1,"SAP S/4HANA Upgrade",1,150000,150000,"2025-12-31"),
        (4,1,4,"Office Refurb Phase 1",1,220000,220000,"2025-09-30"),
        (5,1,2,"50x Desktop PCs",50,1200,60000,"2025-12-31"),
    ]))

    # Quotation headers (E-201 to E-215 same as original but using supplier IDs)
    quot_data = [
        ("QH001","E-201","SAP S/4HANA Upgrade",11,150000,165000,"APPROVED","2025-06-01","IT Services"),
        ("QH002","E-202","Annual Audit Services",7,95000,98500,"APPROVED","2025-05-15","Consulting"),
        ("QH003","E-203","Office Refurbishment Phase 1",15,220000,245000,"APPROVED","2025-04-01","Facilities"),
        ("QH004","E-204","Network Security Assessment",4,45000,48200,"APPROVED","2025-08-01","IT Services"),
        ("QH005","E-205","Cloud Infrastructure Migration Phase 2",3,82000,92180,"APPROVED","2025-10-01","IT Services"),
        ("QH006","E-206","HR System Implementation",12,180000,175000,"APPROVED","2025-03-10","IT Services"),
        ("QH007","E-207","Data Centre Consolidation",13,250000,262000,"APPROVED","2025-07-01","IT Services"),
        ("QH008","E-208","Cybersecurity Training Programme",14,35000,None,"REJECTED","2025-09-01","Consulting"),
        ("QH009","E-209","Facilities Management Contract",20,120000,125000,"APPROVED","2025-05-01","Facilities"),
        ("QH010","E-210","ERP Data Migration",9,78000,82000,"APPROVED","2025-08-15","Consulting"),
        ("QH011","E-211","Desktop Hardware Refresh",3,65000,62500,"APPROVED","2025-10-01","Hardware"),
        ("QH012","E-212","Legal Advisory Services",10,55000,57500,"APPROVED","2025-06-15","Consulting"),
        ("QH013","E-213","Cloud Telephony Migration",5,42000,44100,"APPROVED","2025-09-10","IT Services"),
        ("QH014","E-214","Security Guard Services",16,28000,29400,"APPROVED","2025-07-01","Facilities"),
        ("QH015","E-215","Payroll Processing Outsource",1,15000,None,"DRAFT","2025-11-01","Consulting"),
    ]
    S.append(ins("proc_quotation_headers",["quotation_number","engagement_id","engagement_name","supplier_id",
        "original_amount","revised_amount","status","submission_date","category"],
        [(q[0],q[1],q[2],q[3],q[4],q[5],q[6],q[7],q[8]) for q in quot_data]))

    # Quote versions (2 per quotation to preserve E-205 delta = 12.4%)
    qv = []
    for i,q in enumerate(quot_data):
        qv.append((i+1,1,q[4],q[7],"SUBMITTED",None))
        rev = q[5] if q[5] else q[4]
        qv.append((i+1,2,rev,q[7],q[6],None))
    S.append(ins("proc_quote_versions",["quotation_header_id","version_number","version_amount","submitted_date","status","change_notes"], qv))

    # PO Headers
    po_data = [
        ("PO-2025-001",11,None,53,85000,0,"PENDING",None,"IT Services"),
        ("PO-2025-002",7,None,53,42000,0,"PENDING",None,"Consulting"),
        ("PO-2025-003",3,None,53,120000,0,"PENDING",None,"Hardware"),
        ("PO-2025-011",13,None,53,150000,150000,"APPROVED","2025-03-10","IT Services"),
        ("PO-2025-012",14,None,53,48000,48000,"APPROVED","2025-03-25","IT Services"),
        ("PO-2025-013",9,None,53,72000,72000,"APPROVED","2025-04-12","Consulting"),
        ("PO-2025-014",10,None,53,55000,55000,"APPROVED","2025-04-25","Consulting"),
        ("PO-2025-015",8,None,53,88000,88000,"APPROVED","2025-05-10","Consulting"),
        ("PO-2025-029",16,None,53,45000,0,"REJECTED","2025-06-15","Facilities"),
        ("PO-2025-030",19,None,53,38000,0,"REJECTED","2025-07-12","Facilities"),
    ]
    S.append(ins("proc_po_headers",["po_number","supplier_id","requisition_id","buyer_id","total_amount",
        "approved_amount","status","approved_date","category"],
        [(p[0],p[1],p[2],p[3],p[4],p[5],p[6],p[7],p[8]) for p in po_data]))

    # PO Lines
    pol = []
    for i,p in enumerate(po_data):
        pol.append((i+1,1,1,f"Services - {p[0]}",1,p[4],p[4],"OPEN" if p[6]!="REJECTED" else "CANCELLED"))
    S.append(ins("proc_po_lines",["po_header_id","line_number","item_id","description","quantity","unit_price","line_amount","status"], pol))

    # PO Distributions
    pod = []
    for i in range(len(po_data)):
        pod.append((i+1,1,1,100.00,po_data[i][4]))
    S.append(ins("proc_po_distributions",["po_line_id","cost_centre_id","account_code_id","distribution_pct","amount"], pod))

    # PO Approvals
    poa = []
    for i,p in enumerate(po_data):
        if p[6] in ("APPROVED","REJECTED"):
            poa.append((i+1,53,1,p[6],None,p[7] if p[7] else "2025-06-01","COMPLETED"))
    S.append(ins("proc_po_approvals",["po_header_id","approver_id","approval_level","action","comments","action_date","status"], poa))

    # Contracts
    S.append(ins("proc_contract_headers",["contract_number","contract_name","supplier_id","contract_type",
        "start_date","end_date","total_value","released_amount","status","owner_id"],[
        ("CON-2025-001","IT Managed Services",11,"BLANKET","2025-01-01","2026-12-31",500000,195000,"ACTIVE",53),
        ("CON-2025-002","Facilities Management",20,"BLANKET","2025-01-01","2025-12-31",250000,120000,"ACTIVE",53),
        ("CON-2025-003","Consulting Framework",7,"BLANKET","2025-01-01","2026-06-30",300000,158000,"ACTIVE",53),
    ]))

    S.append(ins("proc_contract_lines",["contract_header_id","line_number","item_id","description","quantity","unit_price","line_amount","released_amount"],[
        (1,1,1,"Cloud services",1,250000,250000,110000),
        (1,2,6,"Software licenses",10,15000,150000,85000),
        (2,1,4,"FM services",1,250000,250000,120000),
        (3,1,3,"Audit & advisory",1,150000,150000,95000),
        (3,2,6,"ERP consulting",1,150000,150000,63000),
    ]))

    # Receipt headers + lines (for APPROVED POs)
    S.append(ins("proc_receipt_headers",["receipt_number","po_header_id","received_by","receipt_date","status","comments"],[
        ("RCV-2025-001",4,53,"2025-03-15","RECEIVED","Full delivery"),
        ("RCV-2025-002",5,53,"2025-03-30","RECEIVED","Full delivery"),
        ("RCV-2025-003",6,53,"2025-04-15","RECEIVED","Full delivery"),
    ]))

    S.append(ins("proc_receipt_lines",["receipt_header_id","po_line_id","quantity_received","quantity_accepted","quantity_rejected","inspection_status"],[
        (1,4,1,1,0,"ACCEPTED"),
        (2,5,1,1,0,"ACCEPTED"),
        (3,6,1,1,0,"ACCEPTED"),
    ]))

    return "".join(S)


if __name__ == "__main__":
    sql = generate()
    outpath = os.path.join(os.path.dirname(__file__), "seed_data.sql")
    with open(outpath, "w", encoding="utf-8") as f:
        f.write(sql)
    row_count = sql.count("\n  (")
    print(f"Generated seed_data.sql:")
    print(f"  Approx rows: {row_count}")
    print(f"  Size: {len(sql):,} bytes")
