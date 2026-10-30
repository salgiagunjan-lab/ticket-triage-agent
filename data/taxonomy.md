# Taxonomy for Ticket Triage Agent

All tickets are synthetic. No real customer data is used.

## Triage taxonomy 

| Category | Category Description | Typical Signals | Default Owner |
| -------- | -------------------- | --------------- | ------------- |
| card_auth_decline | Card authorization decline | "card declined", decline reason codes | Customer engineering |
| webhook_delivery_failure | Webhook delivery failure | Missing events, retries, partner endpoint returning 4xx/5xx | Customer engineering | 
| api_auth_integration_error | API authentication or integration error | 401/403, invalid signature, 400 bad request, SDK errors | TSE (then Customer Engineering)| 
| stablecoin_transfer_settlement_delay | Stablecoin transfer or settlement delay | On/offramp stuck in pending, balance mismatch, missing transaction hash | Payments operations | 
| platform_outage_latency | Platform outage or latency | 5xx across endpoints, timeouts, several partners at once | Platform engineering on-call | 
| kyc_compliance_hold | KYC or compliance hold | User verification stuck, account frozen, document requests | Compliance | 
| how_to_feature_request | How-to or feature request | "How do I…", "Can you support…" | TSE (then Product)| 


## Priority Definitions

Note: If a ticket matches multiple priorities, the most severe wins (P1 over P2 over P3 over P4).  
Money movement “blocked” includes delayed beyond the expected settlement time.

| Priority | Description | 
| -------- | ----------- | 
   | P1 | Money movement blocked for most of one customer's end users, or the same problem reported by 3+ customers within 30 minutes, or a platform-wide outage |
   | P2 | Money movement blocked for 3+ end users, or one customer's production integration broken, or a single flow over 1,000 USDC failing. USDC and USD count at par |
   | P3 | Degraded with a workaround, a sandbox issue, or 1-2 end users affected with no broken integration |
   | P4 | How-to questions and feature requests |


## Owner Queues

| Default Owner | Owner Queue Name |
| ------------- | ---------------- |
| Customer Engineering | customer_engineering_oncall |
| TSE | tech_support_engr_oncall |
| Platform engineering on-call | plat_eng_oncall |
| Payments operations | payments_ops |
| Compliance | compliance |
| Product | product_oncall |



## Additional Questions

Q: Where does a ticket with two problems go? 
Answer: The usual choice is to label the more urgent problem and drop the second one.
