import csv
from collections import Counter
from classifier import classify_transaction

def main():
    with open("../data/synthetic_transactions.csv", "r") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    results = []
    for row in rows:
        cause = classify_transaction(row)
        results.append((row["transaction_id"], cause))

    # print first 15 as a sanity check
    print("Sample classifications:")
    for txn_id, cause in results[:15]:
        print(f"  {txn_id}: {cause}")

    # print distribution
    counts = Counter(cause for _, cause in results)
    print("\nCause distribution across all transactions:")
    for cause, count in counts.most_common():
        print(f"  {cause}: {count}")

if __name__ == "__main__":
    main()