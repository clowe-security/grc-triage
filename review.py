from triage import triage_concern, MODEL
import json
from datetime import datetime, timezone

scenario = input("Describe the compliance concern: ")

result = triage_concern(scenario)
print("Route:", result["route"])
print("Impact:", result["impact"])
print("Likelihood:", result["likelihood"])
print("Severity:", result["severity"])
print("Controls:", result["controls"])
print("Reasoning:", result["reasoning"])
print("Recommended Action:", result["recommended_action"])
print("Guardrail Override:", result["overrides"])

reviewer = ""
while reviewer == "":
    reviewer = input("Reviewer name: ").strip()
decision = ""
while decision not in ["y", "n"]:
    decision = input("Approve this route? (y/n): ").strip().lower()
if decision == "n":
    allowed = ["Escalate", "Review", "Close"]
    if result["severity"] == "High":
        allowed = ["Escalate", "Review"]
    final_route = ""
    while final_route not in allowed:
        final_route = input(f"Choose a route {allowed}: ").strip()
    reason = ""
    while reason == "":
        reason = input("Why?: ").strip()
else:
    final_route = result["route"]
    reason = None

record = {
    "prompt_version": "v3",
    "timestamp": datetime.now(timezone.utc).isoformat(),
    "scenario": scenario,
    "model": MODEL,
    "model_raw_output": result["raw"],
    "recommended_route": result["route"],
    "guardrail_overrides": result["overrides"],
    "severity": result["severity"],
    "reviewer": reviewer,
    "decision": decision,
    "final_route": final_route,
    "reviewer_reason": reason,
}

with open("audit_log.jsonl", "a") as f:
    f.write(json.dumps(record) + "\n")
