import csv
import random
from classifier import classify_transaction
from recovery import get_recovery_action, RECOVERY_SUCCESS_RATE
from caps import CapTracker
from audit_log import log_event

random.seed(7)  # reproducible "did the retry succeed" simulation

DATA_PATH = "../data/synthetic_transactions.csv"


def simulate_outcome(action):
    """Simulates whether a recovery action succeeds, based on RECOVERY_SUCCESS_RATE."""
    rate = RECOVERY_SUCCESS_RATE.get(action, 0.0)
    return random.random() < rate


def run_pipeline():
    with open(DATA_PATH, "r") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    tracker = CapTracker()
    results = []

    for row in rows:
        txn_id = row["transaction_id"]
        user_id = row["user_id"]
        amount = float(row["amount"])
        cause = classify_transaction(row)
        action = get_recovery_action(cause)

        capped = False
        outcome = "no_action"

        if action == "no_action":
            outcome = "no_action"

        elif action in ("retry_nudge", "retry_after_cooldown"):
            if tracker.can_retry(txn_id):
                tracker.record_retry(txn_id)
                success = simulate_outcome(action)
                outcome = "recovered" if success else "not_recovered"
            else:
                capped = True
                outcome = "capped"

        elif action == "suggest_alt_method":
            if tracker.can_nudge(user_id):
                tracker.record_nudge(user_id)
                success = simulate_outcome(action)
                outcome = "recovered" if success else "not_recovered"
            else:
                capped = True
                outcome = "capped"

        log_event(txn_id, cause, action, capped, outcome)
        results.append({
            "transaction_id": txn_id,
            "amount": amount,
            "cause": cause,
            "action": action,
            "capped": capped,
            "outcome": outcome,
        })

    return results


if __name__ == "__main__":
    results = run_pipeline()
    print(f"Processed {len(results)} transactions.")
    print(f"Audit log written to logs/audit_log.jsonl")