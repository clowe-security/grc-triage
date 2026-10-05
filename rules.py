SEVERITY_MATRIX = {
    ("High", "High"): "High",
    ("High", "Moderate"): "High",
    ("High", "Low"): "Moderate",
    ("Moderate", "High"): "High",
    ("Moderate", "Moderate"): "Moderate",
    ("Moderate", "Low"): "Low",
    ("Low", "High"): "Moderate",
    ("Low", "Moderate"): "Low",
    ("Low", "Low"): "Low"
}
def compute_severity(impact,likelihood):
    return SEVERITY_MATRIX[(impact, likelihood)]

def apply_rules(result):
    route = result["route"]
    severity = compute_severity(result["impact"], result["likelihood"])
    overrides = []

    if severity == "High" and route == "Close":
        route = "Review"
        overrides.append("Rule 1: High severity cannot Close; changed to Review")

    if result["likelihood"] == "High" and route != "Escalate":
        route = "Escalate"
        overrides.append("Rule 2: High likelihood (evidence of use) always Escalates")

    return {"route": route, "severity": severity, "overrides": overrides}


if __name__=="__main__":
    print(compute_severity("High","Low"))
    print(compute_severity("Low", "High"))
    print(compute_severity("Moderate", "Moderate"))
    print(compute_severity("High", "High"))    
    print(compute_severity("Low", "Low"))
    bad_result = {"route": "Close", "impact": "High", "likelihood": "Moderate"}
    print(apply_rules(bad_result))      
    print(apply_rules({"route": "Review", "impact": "High", "likelihood": "High"}))
    print(apply_rules({"route": "Close", "impact": "High", "likelihood": "High"}))
    print(apply_rules({"route": "Review", "impact": "Moderate", "likelihood": "Moderate"}))