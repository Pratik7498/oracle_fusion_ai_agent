import requests

tests = [
    ('Q1', 'what is the budget amount for january 2025 for cost centre id 1'),
    ('Q2', 'what was the last year budget amount for engineering cost centre'),
    ('Q3', 'what was the last year budget amount'),
    ('Q4', 'what was the last year budget amount for marketing cost centre')
]

print("=== Testing Budget Queries ===")
for label, q in tests:
    try:
        r = requests.post('http://localhost:8000/chat', json={'query': q, 'session_id': 'budget2'})
        d = r.json()
        print(f"[{label}] {q}")
        print(f"Rows: {d.get('row_count')}, Error: {d.get('error')}")
        print(f"SQL : {d.get('sql_used')}")
        print(f"Data: {d.get('data')[:2] if d.get('data') else []}\n")
    except Exception as e:
         print(f"[{label}] EXCEPTION {e}\n")
