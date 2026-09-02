import csv
import random
import uuid
from datetime import datetime, timedelta

random.seed(42)  # reproducible results

MERCHANTS = ["merch_01", "merch_02", "merch_03", "merch_04", "merch_05"]
METHODS = ["card", "upi", "netbanking", "wallet"]

# 5 failure cause buckets we're targeting, plus successful transactions
CAUSES = [
    "success",
    "otp_timeout",
    "bank_timeout",
    "insufficient_funds",
    "method_mismatch",
    "network_drop",
]

# rough distribution — success is common, each failure type has enough rows to be visible
WEIGHTS = [55, 9, 9, 9, 9, 9]

def random_time(base, max_offset_sec=120):
    return base + timedelta(seconds=random.randint(1, max_offset_sec))

def generate_transaction(txn_num, cause):
    txn_id = f"txn_{txn_num:05d}"
    merchant_id = random.choice(MERCHANTS)
    user_id = f"user_{random.randint(1, 80):03d}"
    amount = round(random.uniform(50, 50000), 2)
    method = random.choice(METHODS)
    t_init = datetime(2026, 9, 1, 10, 0, 0) + timedelta(minutes=txn_num)

    row = {
        "transaction_id": txn_id,
        "merchant_id": merchant_id,
        "user_id": user_id,
        "amount": amount,
        "payment_method": method,
        "timestamp_initiated": t_init.isoformat(),
        "timestamp_otp_sent": "",
        "timestamp_next_event": "",
        "error_code": "",
        "status": "",
    }

    if cause == "success":
        row["timestamp_otp_sent"] = random_time(t_init, 20).isoformat()
        row["timestamp_next_event"] = random_time(t_init, 40).isoformat()
        row["status"] = "success"

    elif cause == "otp_timeout":
        otp_time = random_time(t_init, 20)
        row["timestamp_otp_sent"] = otp_time.isoformat()
        # gap > 90s with no completion -> otp timeout signal
        row["timestamp_next_event"] = (otp_time + timedelta(seconds=random.randint(95, 180))).isoformat()
        row["status"] = "abandoned"

    elif cause == "bank_timeout":
        row["timestamp_otp_sent"] = random_time(t_init, 20).isoformat()
        row["error_code"] = "TIMED_OUT"
        row["status"] = "failed"

    elif cause == "insufficient_funds":
        row["timestamp_otp_sent"] = random_time(t_init, 20).isoformat()
        row["error_code"] = "INSUFFICIENT_FUNDS"
        row["status"] = "failed"

    elif cause == "method_mismatch":
        row["payment_method"] = "card"
        row["amount"] = round(random.uniform(20000, 50000), 2)  # high ticket size
        row["error_code"] = "CARD_DECLINED"
        row["status"] = "failed"

    elif cause == "network_drop":
        # no otp timestamp, no next event, no error code -> silent death
        row["status"] = "abandoned"

    return row


def main():
    rows = []
    total = 300
    for i in range(1, total + 1):
        cause = random.choices(CAUSES, weights=WEIGHTS, k=1)[0]
        rows.append(generate_transaction(i, cause))

    fieldnames = list(rows[0].keys())
    with open("data/synthetic_transactions.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Generated {total} transactions -> data/synthetic_transactions.csv")


if __name__ == "__main__":
    main()