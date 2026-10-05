import json
from triage import triage_concern

passed = 0
total = 0
with open("tests/test_cases.json") as f:
    cases = json.load(f)

for case in cases:
    result = triage_concern(case["scenario"])
    print(case["id"])

    for field in ["route", "impact", "likelihood", "severity"]:
        total += 1
        if case[field] == result[field]:
            passed += 1
            print("     PASS", field)
        else:
            print(f"        FAIL {field} expected: {case[field]} got: {result[field]}")
            print(result["reasoning"])

    for override in result["overrides"]:
        print("     OVERRIDE:", override)

print(f"Score: {passed}/{total}")
