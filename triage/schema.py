"""Check the model's answer against the output schema."""

CATEGORIES = {   
    "card_auth_decline",
    "webhook_delivery_failure",
    "api_auth_integration_error",
    "stablecoin_transfer_settlement_delay",
    "platform_outage_latency",
    "kyc_compliance_hold",
    "how_to_feature_request",
} # the seven strings from taxonomy.md
PRIORITIES = {"P1", "P2", "P3", "P4"}
REQUIRED_KEYS = ["category", "priority", "confidence", "reasoning", "extracted", "first_step"]
EXTRACTED_KEYS = ["http_status", "endpoint", "error_code", "request_id", "event_ids"]


def validate(result):
    """Return a list of problems with the answer; an empty list means valid."""
    problems = []
    if not isinstance(result, dict):
        return ["answer is not a JSON object"]

    for key in REQUIRED_KEYS:
        if key not in result:
            problems.append(f"missing key: {key}")

    if not isinstance(result.get("category"), str): 
        problems.append("category is not a string")
    elif result.get("category") not in CATEGORIES:
        problems.append(f"unknown category: {result.get('category')!r}")
    

    if not isinstance(result.get("priority"), str): 
        problems.append("priority is not a string")    
    elif result.get("priority") not in PRIORITIES:
        problems.append(f"unknown priority: {result.get('priority')!r}")
     
    # confidence: must be a number, 0 <= value <= 1
    confidence = result.get("confidence")
    if not isinstance(confidence, (int, float)):
        problems.append(f"confidence is not a number: {result.get('confidence')!r}")
    elif not (0 <= confidence <= 1):
        problems.append(f"confidence is not between 0 and 1: {confidence}")

    # extracted: must be a dict with EXTRACTED_KEYS; event_ids must be a list
    extracted = result.get("extracted")
    if not isinstance(extracted, dict):
        problems.append(f"extracted is not a JSON object: {extracted!r}")
    else:
        for key in EXTRACTED_KEYS:
            if key not in extracted:
                problems.append(f"missing key in extracted: {key}")
        if not isinstance(extracted.get("event_ids"), list):
            problems.append(f"event_ids is not a list: {extracted.get('event_ids')!r}")
    return problems