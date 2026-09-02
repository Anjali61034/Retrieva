from collections import defaultdict
from pipeline import run_pipeline


def compute_metrics(results):
    total_by_cause = defaultdict(int)
    recovered_by_cause = defaultdict(int)
    amount_recovered_by_cause = defaultdict(float)
    capped_by_cause = defaultdict(int)
    not_recovered_by_cause = defaultdict(int)

    total_amount_at_risk = 0.0
    total_amount_recovered = 0.0

    for r in results:
        cause = r["cause"]
        if cause in ("success",):
            continue  # not a failure, skip from recovery stats

        total_by_cause[cause] += 1
        total_amount_at_risk += r["amount"]

        if r["outcome"] == "recovered":
            recovered_by_cause[cause] += 1
            amount_recovered_by_cause[cause] += r["amount"]
            total_amount_recovered += r["amount"]
        elif r["outcome"] == "capped":
            capped_by_cause[cause] += 1
        elif r["outcome"] == "not_recovered":
            not_recovered_by_cause[cause] += 1

    print("=" * 60)
    print("RECOVERY METRICS")
    print("=" * 60)

    for cause in sorted(total_by_cause.keys()):
        total = total_by_cause[cause]
        recovered = recovered_by_cause[cause]
        capped = capped_by_cause[cause]
        not_rec = not_recovered_by_cause[cause]
        rate = (recovered / total * 100) if total else 0
        print(f"\n{cause}:")
        print(f"  Total failed transactions : {total}")
        print(f"  Recovered                 : {recovered}  ({rate:.1f}%)")
        print(f"  Not recovered             : {not_rec}")
        print(f"  Blocked by cap            : {capped}")
        print(f"  Amount recovered (₹)      : {amount_recovered_by_cause[cause]:,.2f}")

    print("\n" + "-" * 60)
    print(f"TOTAL amount at risk     : ₹{total_amount_at_risk:,.2f}")
    print(f"TOTAL amount recovered   : ₹{total_amount_recovered:,.2f}")
    overall_rate = (total_amount_recovered / total_amount_at_risk * 100) if total_amount_at_risk else 0
    print(f"Overall recovery rate    : {overall_rate:.1f}%")
    print("=" * 60)


if __name__ == "__main__":
    results = run_pipeline()
    compute_metrics(results)