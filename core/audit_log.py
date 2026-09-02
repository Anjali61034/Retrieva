import json
from datetime import datetime

LOG_PATH = "../logs/audit_log.jsonl"


def log_event(transaction_id, cause, action, capped, outcome):
    """
    Appends one JSON line to the audit log. Never overwrites — append-only.
    """
    entry = {
        "timestamp": datetime.now().isoformat(),
        "transaction_id": transaction_id,
        "cause_code": cause,
        "action_taken": action,
        "capped": capped,     # True if the action was blocked by a cap
        "outcome": outcome,   # "recovered", "not_recovered", "no_action", "capped"
    }
    with open(LOG_PATH, "a") as f:
        f.write(json.dumps(entry) + "\n")