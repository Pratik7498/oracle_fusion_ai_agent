import sys, os
sys.path.insert(0, '.')
import psycopg2
from dotenv import load_dotenv
load_dotenv()
url = os.environ.get('POSTGRES_URL', 'postgresql://poc_user:poc_pass_2025@localhost:5432/oracle_fusion_poc')
conn = psycopg2.connect(url)
cur = conn.cursor()

def show_cols(tname):
    cur.execute(
        "SELECT column_name, data_type FROM information_schema.columns "
        "WHERE table_name=%s AND table_schema='public' ORDER BY ordinal_position",
        (tname,)
    )
    print(tname + ":", cur.fetchall())

show_cols('fin_budget_lines')
show_cols('fin_gl_balances')
show_cols('fin_budget_headers')
show_cols('proc_po_distributions')
show_cols('proc_po_headers')

# Test the problematic queries
def safe(sql):
    try:
        cur.execute(sql)
        return cur.fetchall()
    except Exception as e:
        conn.rollback()
        return [("ERR: " + str(e),)]

print("budget_lines start_date range:", safe("SELECT MIN(start_date), MAX(start_date) FROM fin_budget_lines"))
print("gl_balances period_date range:", safe("SELECT MIN(period_date), MAX(period_date) FROM fin_gl_balances"))
print("budget_headers fiscal_year:", safe("SELECT DISTINCT fiscal_year FROM fin_budget_headers ORDER BY fiscal_year"))
print("budget_headers columns:", safe("SELECT period_name FROM fin_budget_headers LIMIT 3"))

conn.close()
