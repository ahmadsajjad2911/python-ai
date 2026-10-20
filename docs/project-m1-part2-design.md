# Module 1 Checkpoint 2 Project: Design (Sweet Crumbs bakery)

## Intents (rules are checked in this order)

| # | Intent | Keywords | Reply |
|---|--------|----------|-------|
| 1 | Human handover | human, agent | Connecting you to a human... (chat ends) |
| 2 | Complaint | refund, complaint, late | A manager will call you within 1 hour. |
| 3 | Exit | bye | Goodbye, <name>! (then the session report) |
| 4 | Greeting | hi, hello, hey (exact match / startswith, never `in`) | Hello <name>! Ask about hours, location, delivery or our menu. |
| 5 | Quote | /quote | Asks item and quantity, then prints subtotal, discount, delivery, total |
| 6 | Hours | hours, open, timing | We are open 9 am to 10 pm, every day. |
| 7 | Location | where, location, your address | We are at Main Market, Lahore. |
| 8 | Delivery | delivery, deliver | Delivery is 200 PKR, free from 3,000 PKR. |
| 9 | Menu / prices | menu, price, cost, how much | Cupcake 250, brownie 300, chocolate cake 1,500 PKR. |
| 10 | Fallback | (anything else) | Cleaned, sliced to 150 chars, token estimate, routed to local or cloud model, AI prompt printed |

Why this order: complaints and handover come first so an unhappy customer always reaches a human. The greeting uses `==` / `startswith()` because "hi" hides inside "which". The word "late" is matched with a space before it, so "chocolate" is not treated as a complaint.

## Business rules

| Rule | Value |
|------|-------|
| Item prices | cupcake 250 PKR, brownie 300 PKR, chocolate cake 1,500 PKR |
| Bulk discount | 10% off for 10 or more items |
| Delivery | 200 PKR, free from 3,000 PKR (checked after the discount) |
| Private words | phone, cnic, my address (routed to the local model, cost 0) |
| Example cloud price | 0.1 PKR per 1K tokens |

## Rule tests

| You type | Expected | Pass? |
|----------|----------|-------|
| `WHAT are your hours` | Hours (capitals and spaces handled) | Pass |
| `which cake is best?` | Fallback, not a greeting | Pass |
| `my order is late` | Manager reply (complaint rule first) | Pass |
| `/quote`, 1 chocolate cake | Delivery fee charged (1,500 + 200 = 1,700) | Pass |
| `/quote`, 20 cupcakes | Delivery free (5,000 - 500 = 4,500) | Pass |
| `/quote`, 10 brownies | Discount applied (-300 PKR) | Pass |
| `/quote`, pizza | "Not on our menu", no crash | Pass |
| `can I change my phone number?` | Routed to the local model, cost 0 | Pass |
| Press Enter with no text | Asks again | Pass |
| `BYE` | Goodbye + session report | Pass |
| `do you have chocolate cake?` (extra) | Fallback, not a complaint | Pass |
| `/quote`, cupcake, `abc` (bonus) | Polite message, no crash | Pass |
| `I want a human` (bonus) | Connecting you to a human... + report | Pass |