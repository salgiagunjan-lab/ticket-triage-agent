"""Command line entry point."""
import argparse
import json

from triage.loader import load_tickets, get_ticket
from triage.classifier import classify_ticket
from triage.providers.openai_provider import OpenAIProvider


def main():
    parser = argparse.ArgumentParser(prog="triage")
    sub = parser.add_subparsers(dest="command", required=True)

    triage_cmd = sub.add_parser("triage", help="Triage one ticket")
    triage_cmd.add_argument("--ticket", required=True, help="Ticket ID to triage")
    triage_cmd.add_argument("--file", default="data/tickets.json", help="Path to the tickets file")

    args = parser.parse_args()

    if args.command == "triage":
        tickets = load_tickets(args.file)
        ticket = get_ticket(tickets, args.ticket)
        result = classify_ticket(ticket, OpenAIProvider())
        print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()