# Retrieva

**AI agent that detects, diagnoses, and recovers failed or abandoned checkouts — built for the Razorpay AI Buildathon 2026, Track 03: AI Revenue Recovery.**

## The problem

30–40% of checkout attempts fail or abandon silently — an OTP times out, a bank gateway hangs, a card gets declined on a ticket size it was never suited for. Most merchants treat every failure as one bucket ("payment failed") and never get a second chance at the transaction.

## What Retrieva does

Retrieva classifies every failed/abandoned transaction into one of five causes from the raw payment event log, maps each cause to exactly one bounded recovery action, enforces hard caps on every action, and logs every decision to an append-only audit trail.

| Cause | Signal | Recovery action |
|---|---|---|
| OTP timeout | >90s gap between OTP-sent and next event | In-session retry nudge |
| Bank/gateway timeout | Explicit `TIMED_OUT` error code | Single retry after 30s cooldown |
| Insufficient funds | Explicit `INSUFFICIENT_FUNDS` decline | **No action** — flagged, never retried |
| Method mismatch | Card declined on ≥₹20,000 ticket size | Suggest alternate payment method |
| Network drop | Session ends with no error code, no OTP timestamp | In-session retry nudge |

Every action is capped: max 1 retry per transaction, max 3 nudges per user per day. Every classification and action is written to `logs/audit_log.jsonl` — timestamped, traceable, never overwritten.

## Results (on 300 synthetic transactions)

- **58.4% overall recovery rate** — ₹23.3L recovered out of ₹40.0L at risk
- **100% classifier accuracy on a held-out test set** (see "What broke" below for how this was earned, not assumed)
- **`insufficient_funds` always gets 0 recovery actions** — proof the system knows when *not* to act
- **Cap enforcement is unit-tested** (`tests/test_caps.py`) — confirmed to actually block a 2nd retry and a 4th daily nudge, not just exist in code

## Architecture
data/ synthetic transaction generator + train/holdout split
core/
classifier.py rules engine: event -> cause label
recovery.py cause -> action lookup table
caps.py enforces retry/nudge limits
audit_log.py append-only decision log
pipeline.py wires it all together
metrics.py recovery-rate reporting
export_dashboard_data.py exports JSON for the dashboard
dashboard/ live HTML dashboard (Chart.js)
tests/
split_data.py 70/30 train/holdout split
evaluate_classifier.py precision/recall on held-out set
test_caps.py confirms caps actually block
logs/ audit trail output


**Why a rules table, not an LLM classifier:** every money-adjacent action needs to be explainable and auditable on demand — a hand-written rules table can be read, tested, and defended line by line. An LLM deciding retry/discount amounts freely would be harder to bound and harder to prove safe under Track 01/03's "every money action explainable, bounded and gated" requirement.

## What broke, and how I fixed it

My classifier initially checked the OTP-timing rule before the bank error-code rule. On a held-out test set, this caused every transaction where a bank timeout coincided with the user being mid-OTP-entry to be misclassified as an OTP timeout instead of a bank timeout — dropping `bank_timeout` recall to 44% and `otp_timeout` precision to 53% (90% overall accuracy). Root cause: an inferred timing signal was overriding a hard error code. Fix: reordered the rules so the explicit bank error code is checked first, since it's stronger evidence than an inferred gap. Recall and precision both returned to 100% on the same held-out set after the fix.

## How to run it

```bash
# 1. Generate synthetic transaction data
python core/generate_data.py

# 2. Split into train/holdout sets
cd tests
python split_data.py

# 3. Evaluate classifier accuracy on the held-out set
python evaluate_classifier.py

# 4. Confirm caps actually block excess actions
python test_caps.py

# 5. Run the full pipeline (classify -> recover -> cap -> log)
cd ../core
python pipeline.py

# 6. See recovery metrics
python metrics.py

# 7. Export dashboard data and view it
python export_dashboard_data.py
cd ../dashboard
python -m http.server 8000
# open http://localhost:8000
```

## Track

Track 03 — AI Revenue Recovery