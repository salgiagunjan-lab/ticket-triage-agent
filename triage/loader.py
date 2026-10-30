"""TODO: Read tickets from JSON or CSV. Day 2."""
import json

def load_tickets(path):
    """Return a list of ticket dicts read from a JSON file."""
    with open(path, encoding="utf-8") as f:
        tickets = json.load(f)
    return tickets

def get_ticket(tickets, ticket_id): 
    """Return a ticket dict from a list of tickets by ticket_id."""
    for ticket in tickets:
        if ticket["id"] == ticket_id:
            return ticket
    raise KeyError("Ticket not found: " + str(ticket_id))