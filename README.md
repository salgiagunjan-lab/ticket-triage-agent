# Partner Ticket Triage Agent

> Status: in progress

A command-line agent that triages partner support tickets for a card issuing and stablecoin payments platform. It classifies each ticket, extracts technical details, runs a live health check, applies rule-based escalation, and recommends an owner and a first step.

All tickets are synthetic. No real customer data is used.

## The problem

TODO: 3 sentences from the PRD problem statement.

## Sample run

TODO: one raw ticket in, the triage JSON out.

## How it works

TODO: architecture diagram and design decisions (rules plus LLM, swappable providers, schema validation, incident detection).

## Results

TODO: accuracy per provider, P1 recall, and where it failed.

## Setup

```
git clone https://github.com/<your-username>/ticket-triage-agent.git
cd ticket-triage-agent
python -m venv .venv
.venv\Scripts\activate        # Windows  (Mac/Linux: source .venv/bin/activate)
pip install -r requirements.txt
copy .env.example .env        # then add your API key(s)
python -m triage.cli --file data/tickets.json --provider openai
```

## What I'd build next

TODO
