import csv
import sys
sys.path.append("../core")
from classifier import classify_transaction

HOLDOUT_PATH = "../data/holdout_transactions.csv"

def main():
    with open(HOLDOUT_PATH, "r") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    causes = sorted(set(row["true_cause"] for row in rows))
    stats = {c: {"tp": 0, "fp": 0, "fn": 0} for c in causes}

    for row in rows:
        true_cause = row["true_cause"]
        predicted = classify_transaction(row)

        if predicted == true_cause:
            stats[true_cause]["tp"] += 1
        else:
            stats[true_cause]["fn"] += 1
            if predicted in stats:
                stats[predicted]["fp"] += 1

    print("=" * 60)
    print(f"PRECISION / RECALL ON HELD-OUT SET (n={len(rows)})")
    print("=" * 60)

    total_correct = 0
    for cause in causes:
        tp = stats[cause]["tp"]
        fp = stats[cause]["fp"]
        fn = stats[cause]["fn"]
        precision = tp / (tp + fp) if (tp + fp) else 0
        recall = tp / (tp + fn) if (tp + fn) else 0
        total_correct += tp
        print(f"\n{cause}:")
        print(f"  Precision: {precision:.2f}")
        print(f"  Recall:    {recall:.2f}")
        print(f"  (tp={tp}, fp={fp}, fn={fn})")

    overall_accuracy = total_correct / len(rows)
    print("\n" + "-" * 60)
    print(f"Overall accuracy: {overall_accuracy:.2%}")
    print("=" * 60)

if __name__ == "__main__":
    main()