from backend.db.connection import execute_query
import json

df1 = execute_query('SELECT DISTINCT fiscal_year, period_name FROM fin_gl_balances ORDER BY fiscal_year, period_name')
periods = df1.to_dict('records')

df2 = execute_query('''
SELECT cc.cost_centre_name, COUNT(gb.balance_id) as rows
FROM fin_cost_centres cc
LEFT JOIN fin_gl_balances gb ON gb.cost_centre_id = cc.cost_centre_id
GROUP BY cc.cost_centre_name
ORDER BY cc.cost_centre_name
''')
centres = df2.to_dict('records')

with open('db_gl_dump.json', 'w') as f:
    json.dump({'periods': periods, 'centres': centres}, f, indent=2)
