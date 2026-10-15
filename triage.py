from rules import apply_rules
import json
import boto3

MODEL = "us.anthropic.claude-haiku-4-5-20251001-v1:0"

bedrock_client = boto3.client(service_name='bedrock-runtime',
                              region_name='us-west-2')


with open("prompts/system_prompt.md") as f:
    system_prompt = f.read()


def triage_concern(scenario):
    prompt = f"Compliance concern: {scenario}"
    response = bedrock_client.converse(
        modelId=MODEL,
        messages=[{"role": "user", "content": [{"text": prompt}]}],
        system=[{"text": system_prompt}],
        inferenceConfig={"maxTokens" : 1000},
    )
    raw = response["output"]["message"]["content"][0]["text"]
    cleaned = raw.strip().removeprefix("```json").removesuffix("```").strip()
    try:
        result = json.loads(cleaned)
        if result["route"] not in ["Escalate", "Review", "Close"]:
            raise KeyError("route")
        final = apply_rules(result)
    except (json.JSONDecodeError, KeyError, TypeError):
        print("WARNING: model output was missing or invalid. Raw output:")
        print(raw)
        result = {
            "route": "Review",
            "impact": "High",
            "likelihood": "Moderate",
            "controls": [],
            "reasoning": "Model output could not be parsed or was invalid. Manual triage required.",
            "recommended_action": "Triage this concern manually.",
        }
        final = apply_rules(result)
    result["route"] = final["route"]
    result["severity"] = final["severity"]
    result["overrides"] = final["overrides"]
    result["raw"] = raw
    return result