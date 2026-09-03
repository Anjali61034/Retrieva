import sys
sys.path.append("../core")
from caps import CapTracker

def test_retry_cap():
    tracker = CapTracker()
    txn_id = "txn_TEST_001"

    # First retry should be allowed
    assert tracker.can_retry(txn_id) == True
    tracker.record_retry(txn_id)

    # Second retry on the SAME transaction should now be blocked
    assert tracker.can_retry(txn_id) == False

    print("PASS: retry cap correctly blocks a 2nd retry on the same transaction")


def test_nudge_cap():
    tracker = CapTracker()
    user_id = "user_TEST_001"

    # First 3 nudges should be allowed (max_nudges_per_user_per_day = 3)
    for i in range(3):
        assert tracker.can_nudge(user_id) == True
        tracker.record_nudge(user_id)

    # 4th nudge for the same user should now be blocked
    assert tracker.can_nudge(user_id) == False

    print("PASS: nudge cap correctly blocks the 4th nudge for the same user in a day")


if __name__ == "__main__":
    test_retry_cap()
    test_nudge_cap()
    print("\nAll cap tests passed.")