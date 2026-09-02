from datetime import datetime

def parse_time(ts):
    """Parse an ISO timestamp string, return None if empty."""
    if not ts:
        return None
    return datetime.fromisoformat(ts)


def classify_transaction(row):
    """
    Takes one transaction dict (from the CSV) and returns a cause label.
    Causes: success, otp_timeout, bank_timeout, insufficient_funds,
            method_mismatch, network_drop, unknown
    """
    status = row.get("status", "")
    error_code = row.get("error_code", "") or ""
    otp_sent = parse_time(row.get("timestamp_otp_sent", ""))
    next_event = parse_time(row.get("timestamp_next_event", ""))
    amount = float(row.get("amount", 0) or 0)
    method = row.get("payment_method", "")

    if status == "success":
        return "success"

    # Rule 1: OTP timeout — otp was sent, but gap to next event > 90s
    if otp_sent and next_event:
        gap_seconds = (next_event - otp_sent).total_seconds()
        if gap_seconds > 90:
            return "otp_timeout"

    # Rule 2: explicit bank/gateway timeout error code
    if error_code == "TIMED_OUT":
        return "bank_timeout"

    # Rule 3: explicit insufficient funds decline
    if error_code == "INSUFFICIENT_FUNDS":
        return "insufficient_funds"

    # Rule 4: method mismatch — card used on a high ticket size, declined
    if method == "card" and amount >= 20000 and error_code == "CARD_DECLINED":
        return "method_mismatch"

    # Rule 5: network drop — no otp timestamp, no next event, no error code, abandoned
    if status == "abandoned" and not otp_sent and not next_event and not error_code:
        return "network_drop"

    return "unknown"