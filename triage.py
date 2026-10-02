import json
import anthropic

client = anthropic.Anthropic()

passed = 0
total = 0

with open("tests/test_cases.json") as f:
    cases = json.load(f)

with open("prompts/system_prompt.md") as f:
    system_prompt = f.read()

for case in cases:
    prompt = f"Compliance concern: {case['scenario']}"
    response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=500,
        messages=[{"role": "user", "content": prompt}],
        system=system_prompt,
    )
    raw = response.content[0].text
    cleaned = raw.strip().removeprefix("```json").removesuffix("```").strip()
    result = json.loads(cleaned)

    print(case["id"])

    for field in ["route", "impact", "likelihood", "severity"]:
        total += 1
        if case[field] == result[field]:
            passed += 1
            print("     PASS", field)
        else:
            print(f"        FAIL {field} expected: {case[field]} got: {result[field]}")
print(f"Score: {passed}/{total}")
