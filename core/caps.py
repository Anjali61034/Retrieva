class CapTracker:
    """
    Tracks recovery actions already taken, to enforce caps.
    In-memory for now (dict-based) — good enough for a batch run.
    """

    def __init__(self):
        self.retry_count = {}       # transaction_id -> count
        self.nudge_count_by_user = {}  # user_id -> count (per run, simulating "per day")
        self.max_retries_per_txn = 1
        self.max_nudges_per_user_per_day = 3

    def can_retry(self, transaction_id):
        return self.retry_count.get(transaction_id, 0) < self.max_retries_per_txn

    def record_retry(self, transaction_id):
        self.retry_count[transaction_id] = self.retry_count.get(transaction_id, 0) + 1

    def can_nudge(self, user_id):
        return self.nudge_count_by_user.get(user_id, 0) < self.max_nudges_per_user_per_day

    def record_nudge(self, user_id):
        self.nudge_count_by_user[user_id] = self.nudge_count_by_user.get(user_id, 0) + 1