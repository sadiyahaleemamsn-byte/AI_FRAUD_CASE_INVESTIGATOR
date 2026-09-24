import json


def generate_case(result, patterns=None, connected_customers=None):
    if patterns is None:
        patterns = []

    if connected_customers is None:
        connected_customers = []

    case = {
        "case_id": "CUSTOM-" + str(result["transaction_id"]),
        "status": "open",
        "verdict": str(result["verdict"]),
        "fraud_probability": float(result["risk_score"]),

        "affected_txn_ids": [
            str(result["transaction_id"])
        ],

        "first_suspicious_txn_id":
            str(result["transaction_id"]),

        "exposure_usd":
            float(result["amount"]),

        "customer_id":
            str(result["customer_id"]),

        "device_id":
            str(result["device_id"]),

        "evidence": [
            {
                "type": "transaction",
                "description":
                    "Transaction amount: $" + str(result["amount"]),
                "transaction_id":
                    str(result["transaction_id"])
            },

            {
                "type": "customer_history",
                "description":
                    "Customer has "
                    + str(result["customer_transaction_count"])
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
                    [str(c) for c in connected_customers]
            }
        ]
    }

    return case


def case_to_json(case):
    return json.dumps(case, indent=4)


# -------------------------------------------------
# REFERENCE CASE LOADER
# -------------------------------------------------

def load_case(case_id):
    """
    Loads a built-in reference case.
    """

    reference_cases = {

        "HHG-008": {
            "case_id": "HHG-008",
            "status": "open",
            "verdict": "Suspicious",
            "fraud_probability": 0.87,

            "affected_txn_ids": [
                "TXN-HHG-008"
            ],

            "first_suspicious_txn_id":
                "TXN-HHG-008",

            "exposure_usd": 1250.00,

            "customer_id": "CUST-008",

            "device_id": "DEV-008",

            "evidence": [
                {
                    "type": "transaction",
                    "description":
                        "Suspicious transaction amount: $1250.00",
                    "transaction_id":
                        "TXN-HHG-008"
                },

                {
                    "type": "customer_history",
                    "description":
                        "Customer has 18 historical transactions.",
                    "customer_id":
                        "CUST-008"
                },

                {
                    "type": "suspicious_patterns",
                    "description":
                        "Patterns identified during investigation.",
                    "patterns": [
                        "Unusual transaction amount",
                        "High-risk transaction pattern"
                    ]
                },

                {
                    "type": "device_relationship",
                    "description":
                        "Customers connected to the device.",
                    "connected_customers": [
                        "CUST-008",
                        "CUST-014"
                    ]
                }
            ]
        }
    }

    return reference_cases.get(case_id)