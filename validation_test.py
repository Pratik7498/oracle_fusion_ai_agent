import sys
sys.path.insert(0, '.')

from backend.query_intent_parser import parse_intent
from backend.query_planner import build_query_plan, format_plan_for_prompt

tests_passed = 0
tests_failed = 0

def check(name, cond, info=''):
    global tests_passed, tests_failed
    if cond:
        print(f'  PASS: {name}')
        tests_passed += 1
    else:
        print(f'  FAIL: {name} -- got: {info}')
        tests_failed += 1

# --- Intent Parser ---
print('=== Intent Parser Tests ===')

i = parse_intent('what was the last year budget amount')
check('budget metric', i['metric'] == 'budget', i['metric'])
check('last_year time filter', i['time_filter'] == 'last_year', i['time_filter'])

i = parse_intent('how many employees are active')
check('headcount metric', i['metric'] in ('headcount','employee'), i['metric'])
check('COUNT aggregation', i['aggregation'] == 'COUNT', i['aggregation'])

i = parse_intent('total spend by department')
check('spend metric', i['metric'] == 'spend', i['metric'])
check('SUM aggregation', i['aggregation'] == 'SUM', i['aggregation'])
check('department dimension', i['dimension'] == 'department', i['dimension'])

i = parse_intent('salary range for software engineer')
check('salary metric', i['metric'] == 'salary', i['metric'])

i = parse_intent('which suppliers received highest payments')
check('payment or supplier metric', i['metric'] in ('payment','supplier'), i['metric'])

i = parse_intent('show total expenditure by department this year')
check('expenditure->spend synonym', i['metric'] == 'spend', i['metric'])
check('current_year time filter', i['time_filter'] == 'current_year', i['time_filter'])

i = parse_intent('how many staff are in Engineering')
check('staff synonym resolved', any('staff' in s for s in i['synonyms_resolved']), str(i['synonyms_resolved']))

i = parse_intent('actual vs budget variance by cost centre')
check('variance metric detected', i['metric'] in ('gl_variance','gl_actual','budget'), i['metric'])
check('cost_centre dimension', i['dimension'] == 'cost_centre', i['dimension'])

print()
print('=== Query Planner Tests ===')

p = build_query_plan('what was the last year budget amount', domain='FINANCE')
check('budget->fin_budget_lines', p['metric_table'] == 'fin_budget_lines', p['metric_table'])
check('budget->amount column', p['metric_column'] == 'amount', p['metric_column'])
check('time_filter=last_year', p['time_filter'] == 'last_year', p['time_filter'])
check('time_filter_sql not None', p['time_filter_sql'] is not None, str(p['time_filter_sql']))

p = build_query_plan('show actual spend for engineering', domain='FINANCE')
check('actual->fin_gl_balances', p['metric_table'] == 'fin_gl_balances', p['metric_table'])
check('actual->actual_amount', p['metric_column'] == 'actual_amount', p['metric_column'])

p = build_query_plan('total spend by department', domain='PROCUREMENT')
check('spend->proc_po_distributions', p['metric_table'] == 'proc_po_distributions', p['metric_table'])
check('spend->amount', p['metric_column'] == 'amount', p['metric_column'])
check('dimension=department', p['dimension'] == 'department', p['dimension'])
check('group_by has dept_name', p['group_by'] and 'dept_name' in p['group_by'], str(p['group_by']))

p = build_query_plan('salary range for software engineer', domain='HCM')
check('salary->hcm_assignments', p['metric_table'] == 'hcm_assignments', p['metric_table'])
check('salary->salary col', p['metric_column'] == 'salary', p['metric_column'])

p = build_query_plan('which suppliers received highest payments', domain='FINANCE')
check('payment->fin_ap_payments', p['metric_table'] == 'fin_ap_payments', p['metric_table'])

p = build_query_plan('which departments have highest spend and most employees', domain='CROSS_DOMAIN')
check('cross-domain detected', p['is_cross_domain'] is True, str(p['is_cross_domain']))
check('cte_domains>=2', len(p['cte_domains']) >= 2, str(p['cte_domains']))

p = build_query_plan('budget for engineering department last year', domain='FINANCE')
check('budget plan has fin_budget_lines note', any('fin_budget_lines' in n for n in p['plan_notes']), str(p['plan_notes']))

p = build_query_plan('total spend by supplier', domain='PROCUREMENT')
check('spend plan has proc_po_distributions note', any('proc_po_distributions' in n for n in p['plan_notes']), str(p['plan_notes']))

p = build_query_plan('total budget last year', domain='FINANCE')
s = format_plan_for_prompt(p)
check('prompt has fin_budget_lines', 'fin_budget_lines' in s, s[:300] if s else '(empty)')
check('prompt non-empty', len(s) > 0, '(empty string)')

print()
print(f'=== RESULTS: {tests_passed} passed, {tests_failed} failed ===')
sys.exit(0 if tests_failed == 0 else 1)
