import json

with open("tests/test_cases.json") as f:
    cases = json.load(f)

for case in cases:
    print(case["id"],case["scenario"])