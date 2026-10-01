import json
import anthropic

client = anthropic.Anthropic()

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
    print(case["id"])
    print(response.content[0].text)
