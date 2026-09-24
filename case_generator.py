import json


def generate_case(result, patterns, connected_customers):

    case = {
        "case_id": "CUSTOM-" + str(result["transaction_id"]),

        "status": "open",

        "verdict": str(result["verdict"]),

        "fraud_probability": float(
            result["risk_score"]
        ),

        "affected_txn_ids": [
            str(result["transaction_id"])
        ],

        "first_suspicious_txn_id":
            str(result["transaction_id"]),

        "exposure_usd": float(
            result["amount"]
        ),

        "customer_id":
            str(result["customer_id"]),

        "device_id":
            str(result["device_id"]),

        "evidence": [

            {
                "type": "transaction",

                "description":
                    "Transaction amount: $"
                    + str(result["amount"]),

                "transaction_id":
                    str(result["transaction_id"])
            },

            {
                "type": "customer_history",

                "description":
                    "Customer has "
                    + str(
                        result[
                            "customer_transaction_count"
                        ]
                    )
                    + " historical transactions.",

                "customer_id":
                    str(result["customer_id"])
            },

            {
                "type": "suspicious_patterns",

                "description":
                    "Patterns identified during investigation.",

                "patterns":
                    [str(p) for p in patterns]
            },

            {
                "type": "device_relationship",

                "description":
                    "Customers connected to the device.",

                "connected_customers":
                    [
                        str(c)
                        for c in connected_customers
                    ]
            }
        ]
    }

    return case


def case_to_json(case):

    return json.dumps(
        case,
        indent=4
    )