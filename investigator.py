import pandas as pd
import numpy as np


def investigate_transaction(transaction_id, df):
    """
    Investigate one transaction using:
    - transaction amount
    - customer history
    - device history
    - region history
    """

    transaction_id = str(transaction_id)

    tx = df[df["transaction_id"].astype(str) == transaction_id]

    if tx.empty:
        return {
            "status": "error",
            "message": "Transaction not found"
        }

    tx = tx.iloc[0]

    customer_id = str(tx["customer_id"])
    device_id = str(tx["device_id"])

    amount = float(tx["amount"])

    # Customer history before current transaction
    history = df[
        (df["customer_id"].astype(str) == customer_id) &
        (df["transaction_id"].astype(str) != transaction_id)
    ]

    # Amount baseline
    if len(history) > 0:
        median_amount = history["amount"].median()
    else:
        median_amount = amount

    # Amount anomaly
    unusual_amount = amount > (median_amount * 2)

    # Device history
    device_transactions = df[
        df["device_id"].astype(str) == device_id
    ]

    new_device = len(device_transactions) <= 1

    # Region history
    if len(history) > 0:
        known_regions = set(history["region"].astype(str))
    else:
        known_regions = set()

    unseen_region = str(tx["region"]) not in known_regions

    # Simple risk score
    risk_score = 0

    if unusual_amount:
        risk_score += 0.30

    if new_device:
        risk_score += 0.25

    if unseen_region:
        risk_score += 0.20

    if len(history) < 5:
        risk_score += 0.10

    risk_score = min(risk_score, 1.0)

    if risk_score >= 0.70:
        verdict = "high_risk"
    elif risk_score >= 0.40:
        verdict = "review"
    else:
        verdict = "uncertain"

    return {
        "status": "success",
        "transaction_id": transaction_id,
        "customer_id": customer_id,
        "amount": amount,
        "device_id": device_id,
        "region": str(tx["region"]),

        "customer_transaction_count": len(history),
        "baseline_median_amount": round(float(median_amount), 2),

        "signals": {
            "unusual_amount": unusual_amount,
            "new_device": new_device,
            "unseen_region": unseen_region
        },

        "risk_score": round(risk_score, 2),
        "verdict": verdict
    }