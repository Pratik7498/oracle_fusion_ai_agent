import sys
sys.path.insert(0, '.')
from backend.query_intent_parser import parse_intent
from backend.query_planner import build_query_plan

passed = 0
failed = 0

def check(name, cond, got=''):
    global passed, failed
    if cond:
        print('  PASS:', name)
        passed += 1
    else:
        print('  FAIL:', name, '-- got:', got)
        failed += 1

# Test cost_centre dimension
i = parse_intent('actual vs budget variance by cost centre')
check('cost_centre dimension', i['dimension'] == 'cost_centre', i['dimension'])
check('variance metric', i['metric'] in ('gl_variance','gl_actual','budget'), i['metric'])

# Test payment vs supplier
i2 = parse_intent('which suppliers received highest payments')
check('payment metric detected', i2['metric'] in ('payment','supplier'), i2['metric'])

p = build_query_plan('which suppliers received highest payments', domain='FINANCE')
check('payment table is fin_ap_payments', p['metric_table'] == 'fin_ap_payments', p['metric_table'])

print()
print('=== QUICK RESULTS:', passed, 'passed,', failed, 'failed ===')
sys.exit(0 if failed == 0 else 1)
