from rules import apply_rules
import json
import anthropic

client = anthropic.Anthropic()

with open("prompts/system_prompt.md") as f:
    system_prompt = f.read()


def triage_concern(scenario):
    prompt = f"Compliance concern: {scenario}"
    response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=500,
        messages=[{"role": "user", "content": prompt}],
        system=system_prompt,
    )
    raw = response.content[0].text
    cleaned = raw.strip().removeprefix("```json").removesuffix("```").strip()
    result = json.loads(cleaned)
    final = apply_rules(result)
    result["route"] = final["route"]
    result["severity"] = final["severity"]
    result["overrides"] = final["overrides"]
    result["raw"] = raw
    return result
