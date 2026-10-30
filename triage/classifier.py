"""Build the prompt and call the chosen provider. Day 2."""
import json
from pathlib import Path

TAXONOMY_PATH = Path(__file__).resolve().parent.parent / "data" / "taxonomy.md"

def build_prompt(ticket):
    """Build the prompt for the ticket classification."""
    with open(TAXONOMY_PATH, encoding="utf-8") as f:
        taxonomy = f.read()
    return f"""
    You are customer support agent expert at classifying tickets. 
    Look at the following ticket {ticket} and classify it into a JSON object. Format is below. 
    Return ONE JSON object and nothing else, with exactly these keys:
    {{
        "category": "<one category name, exactly as written in the taxonomy>",
        "priority": "<P1, P2, P3 or P4>",
        "confidence": <number between 0 and 1>,
        "reasoning": "<one sentence>",
        "extracted": {{
            "http_status": <integer or null>,
            "endpoint": "<string or null>",
            "error_code": "<string or null>",
            "request_id": "<string or null>"
        }},
        "first_step": "<one recommended troubleshooting step>"
    }}
    The category should be one of the categories defined in the Triage taxonomy table below.
    The priority should be one of the priorities defined in the Priority Definitions table below.
    
    Rules: 
    The most severe matching priority wins. 
    For classification, judge by impact, not by tone. 
    If there are two problems, classify the more urgent one.

    TAXONOMY AND PRIORITY RULES
    {taxonomy}

    """

def classify_ticket(ticket, provider):
    """Classify a ticket using the given provider."""
    prompt = build_prompt(ticket)
    raw = provider.classify(prompt)        # the model's text answer
    result = json.loads(raw)            # text -> Python dict
    result["ticket_id"] = ticket["id"]           # which ticket this answer belongs to
    return result