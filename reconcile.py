#!/usr/bin/env python3
"""Payment reconciliation.

Reads payments.jsonl and works out how much money we actually collected.
Run:  python3 reconcile.py
"""
import json

# Keep only the latest attempt for each transaction.
latest = {}
with open("payments.jsonl", encoding="utf-8") as f:
    for line in f:
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue  # skip lines that can't be read

        if not isinstance(event, dict) or not event.get("txn_id"):
            continue  # skip events without a transaction id

        if event["txn_id"] not in latest or event["ts"] >= latest[event["txn_id"]]["ts"]:
            latest[event["txn_id"]] = event

# A payment counts only if its latest attempt succeeded.
total = 0.0
count = 0
for event in latest.values():
    if event["status"] == "success":
        total += float(str(event["amount"]).replace(",", ""))
        count += 1

with open("expected.txt", encoding="utf-8") as f:
    expected = int(f.read().strip())

if count != expected:
    print(f"Check failed: counted {count} successful payments, expected {expected}.")
    print("Something in the data isn't being handled the way the README describes.")
else:
    print(f"Check passed: {count} successful payments.")
    print(f"Your code: KOYA-{round(total)}")
