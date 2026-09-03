import json
from pipeline import run_pipeline
from metrics import compute_metrics
from collections import defaultdict

def export():
    results = run_pipeline()

    total_by_cause = defaultdict(int)
    recovered_by_cause = defaultdict(int)
    amount_recovered_by_cause = defaultdict(float)
    amount_at_risk_by_cause = defaultdict(float)

    total_amount_at_risk = 0.0
    total_amount_recovered = 0.0

    for r in results:
        cause = r["cause"]
        if cause == "success":
            continue
        total_by_cause[cause] += 1
        amount_at_risk_by_cause[cause] += r["amount"]
        total_amount_at_risk += r["amount"]
        if r["outcome"] == "recovered":
            recovered_by_cause[cause] += 1
            amount_recovered_by_cause[cause] += r["amount"]
            total_amount_recovered += r["amount"]

    causes = sorted(total_by_cause.keys())
    dashboard_data = {
        "total_transactions": len(results),
        "total_amount_at_risk": round(total_amount_at_risk, 2),
        "total_amount_recovered": round(total_amount_recovered, 2),
        "overall_recovery_rate": round(
            (total_amount_recovered / total_amount_at_risk * 100) if total_amount_at_risk else 0, 1
        ),
        "by_cause": [
            {
                "cause": cause,
                "total": total_by_cause[cause],
                "recovered": recovered_by_cause[cause],
                "recovery_rate": round(
                    (recovered_by_cause[cause] / total_by_cause[cause] * 100) if total_by_cause[cause] else 0, 1
                ),
                "amount_at_risk": round(amount_at_risk_by_cause[cause], 2),
                "amount_recovered": round(amount_recovered_by_cause[cause], 2),
            }
            for cause in causes
        ],
    }

    with open("../dashboard/data.json", "w") as f:
        json.dump(dashboard_data, f, indent=2)

    print("Dashboard data exported -> dashboard/data.json")


if __name__ == "__main__":
    export()