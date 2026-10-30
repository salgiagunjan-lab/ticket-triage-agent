"""Check data/labels.json against data/tickets.json.

Run from the repo root:  python validate_labels.py
Optional paths:          python validate_labels.py data/tickets.json data/labels.json
"""
import json
import sys

CATEGORIES = {
    "card_auth_decline",
    "webhook_delivery_failure",
    "api_auth_integration_error",
    "stablecoin_transfer_settlement_delay",
    "platform_outage_latency",
    "kyc_compliance_hold",
    "how_to_feature_request",
}
PRIORITIES = {"P1", "P2", "P3", "P4"}
QUEUES = {
    "customer_engineering_oncall",
    "tech_support_engr_oncall",
    "plat_eng_oncall",
    "payments_ops",
    "compliance",
    "product_oncall",
}
# First queue wins for the "TSE (then ...)" categories.
DEFAULT_QUEUE = {
    "card_auth_decline": "customer_engineering_oncall",
    "webhook_delivery_failure": "customer_engineering_oncall",
    "api_auth_integration_error": "tech_support_engr_oncall",
    "stablecoin_transfer_settlement_delay": "payments_ops",
    "platform_outage_latency": "plat_eng_oncall",
    "kyc_compliance_hold": "compliance",
    "how_to_feature_request": "tech_support_engr_oncall",
}


def main(tickets_path, labels_path):
    with open(tickets_path, encoding="utf-8") as f:
        tickets = json.load(f)
    with open(labels_path, encoding="utf-8") as f:
        labels = json.load(f)

    problems = []
    ticket_ids = [t["id"] for t in tickets]

    if len(set(ticket_ids)) != len(ticket_ids):
        problems.append("duplicate ticket ids in tickets file")
    for tid in ticket_ids:
        if tid not in labels:
            problems.append(f"{tid}: no label")
    for tid in labels:
        if tid not in ticket_ids:
            problems.append(f"{tid}: label has no matching ticket")

    for tid, lab in labels.items():
        if set(lab) != {"category", "priority", "owner_queue"}:
            problems.append(f"{tid}: fields are {sorted(lab)}")
            continue
        if lab["category"] not in CATEGORIES:
            problems.append(f"{tid}: unknown category {lab['category']!r}")
        if lab["priority"] not in PRIORITIES:
            problems.append(f"{tid}: unknown priority {lab['priority']!r}")
        if lab["owner_queue"] not in QUEUES:
            problems.append(f"{tid}: unknown owner_queue {lab['owner_queue']!r}")
        elif lab["category"] in DEFAULT_QUEUE and lab["owner_queue"] != DEFAULT_QUEUE[lab["category"]]:
            problems.append(
                f"{tid}: queue {lab['owner_queue']} differs from the default "
                f"{DEFAULT_QUEUE[lab['category']]} for {lab['category']}"
            )

    print(f"{len(ticket_ids)} tickets, {len(labels)} labels")
    if problems:
        print(f"{len(problems)} problem(s):")
        for p in problems:
            print("  -", p)
        return 1
    print("OK: every ticket has a valid label")
    return 0


if __name__ == "__main__":
    args = sys.argv[1:]
    paths = (args[0], args[1]) if len(args) == 2 else ("data/tickets.json", "data/labels.json")
    sys.exit(main(*paths))
