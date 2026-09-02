import csv
import random

random.seed(99)

SOURCE = "../data/synthetic_transactions.csv"
TRAIN_OUT = "../data/train_transactions.csv"
HOLDOUT_OUT = "../data/holdout_transactions.csv"

def main():
    with open(SOURCE, "r") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    random.shuffle(rows)
    split_idx = int(len(rows) * 0.7)
    train_rows = rows[:split_idx]
    holdout_rows = rows[split_idx:]

    fieldnames = list(rows[0].keys())

    with open(TRAIN_OUT, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(train_rows)

    with open(HOLDOUT_OUT, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(holdout_rows)

    print(f"Train set: {len(train_rows)} rows -> {TRAIN_OUT}")
    print(f"Holdout set: {len(holdout_rows)} rows -> {HOLDOUT_OUT}")

if __name__ == "__main__":
    main()