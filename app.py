import json
import pandas as pd
import streamlit as st

from investigator import investigate_transaction
from case_generator import generate_case, case_to_json,load_case



# -----------------------------
# Page Configuration
# -----------------------------

st.set_page_config(
    page_title="AI Fraud Case Investigator",
    page_icon="🔎",
    layout="wide"
)


# -----------------------------
# Application Title
# -----------------------------

st.title("🔎 AI Fraud Case Investigator")

st.write(
    "Investigate suspicious transactions using customer "
    "history, device relationships, and transaction patterns."
)


# -----------------------------
# Load Dataset
# -----------------------------

@st.cache_data
def load_data():

    df = pd.read_csv("data/transactions.csv")

    required_columns = [
        "transaction_id",
        "customer_id",
        "amount",
        "device_id",
        "region"
    ]

    missing_columns = [
        column
        for column in required_columns
        if column not in df.columns
    ]

    if missing_columns:

        st.error(
            f"Missing columns: {missing_columns}"
        )

        st.stop()

    return df


df = load_data()


# -----------------------------
# Transaction Investigation
# -----------------------------

st.subheader("🔍 Transaction Investigation")

transaction_id = st.text_input(
    "Enter Transaction ID",
    placeholder="Example: 3558054"
)


if st.button("🔍 Investigate"):

    if not transaction_id:

        st.warning(
            "Please enter a transaction ID."
        )

    else:

        result = investigate_transaction(
            transaction_id,
            df
        )

        if result["status"] == "error":

            st.error(
                result["message"]
            )

        else:

            st.success(
                "Investigation completed successfully."
            )


            # -----------------------------
            # Basic Information
            # -----------------------------

            st.subheader(
                "📌 Transaction Information"
            )

            col1, col2, col3, col4 = st.columns(4)

            col1.metric(
                "Transaction",
                result["transaction_id"]
            )

            col2.metric(
                "Customer",
                result["customer_id"]
            )

            col3.metric(
                "Amount",
                f"${result['amount']:.2f}"
            )

            col4.metric(
                "Risk Score",
                result["risk_score"]
            )


            # -----------------------------
            # Investigation Result
            # -----------------------------

            st.subheader(
                "⚠️ Investigation Result"
            )

            st.write(
                f"**Verdict:** "
                f"{result['verdict'].upper()}"
            )

            st.write(
                f"**Customer transactions:** "
                f"{result['customer_transaction_count']}"
            )

            st.write(
                f"**Historical median amount:** "
                f"${result['baseline_median_amount']:.2f}"
            )


            # -----------------------------
            # Risk Signals
            # -----------------------------

            st.subheader(
                "🚨 Detected Signals"
            )

            signals = result["signals"]

            col1, col2, col3 = st.columns(3)

            col1.metric(
                "Unusual Amount",
                "YES"
                if bool(signals["unusual_amount"])
                else "NO"
            )

            col2.metric(
                "New Device",
                "YES"
                if bool(signals["new_device"])
                else "NO"
            )

            col3.metric(
                "Unseen Region",
                "YES"
                if bool(signals["unseen_region"])
                else "NO"
            )


            # -----------------------------
            # Transaction Details
            # -----------------------------

            st.subheader(
                "📋 Transaction Details"
            )

            details = pd.DataFrame(
                {
                    "Field": [
                        "Transaction ID",
                        "Customer ID",
                        "Amount",
                        "Device ID",
                        "Region"
                    ],

                    "Value": [
                        result["transaction_id"],
                        result["customer_id"],
                        result["amount"],
                        result["device_id"],
                        result["region"]
                    ]
                }
            )

            st.dataframe(
                details,
                use_container_width=True
            )


            # -----------------------------
            # Customer History
            # -----------------------------

            st.subheader(
                "📊 Customer Transaction History"
            )

            customer_id = result["customer_id"]

            customer_history = df[
                df["customer_id"].astype(str)
                == str(customer_id)
            ].copy()

            if not customer_history.empty:

                st.dataframe(
                    customer_history,
                    use_container_width=True
                )

            else:

                st.info(
                    "No customer history found."
                )


            # -----------------------------
            # Device Relationship Analysis
            # -----------------------------

            st.subheader(
                "📱 Device Relationship Analysis"
            )

            device_id = result["device_id"]

            device_transactions = df[
                df["device_id"].astype(str)
                == str(device_id)
            ].copy()

            if not device_transactions.empty:

                st.write(
                    f"Transactions associated with device: "
                    f"**{device_id}**"
                )

                st.dataframe(
                    device_transactions,
                    use_container_width=True
                )

                connected_customers = (
                    device_transactions[
                        "customer_id"
                    ]
                    .astype(str)
                    .unique()
                    .tolist()
                )

                st.write(
                    f"**Connected customers:** "
                    f"{len(connected_customers)}"
                )

                st.write(
                    connected_customers
                )

            else:

                connected_customers = []

                st.info(
                    "No device relationships found."
                )


            # -----------------------------
            # Suspicious Pattern Detection
            # -----------------------------

            st.subheader(
                "🚨 Suspicious Patterns"
            )

            patterns = []

            if bool(signals["unusual_amount"]):

                patterns.append(
                    "Transaction amount is unusually "
                    "high compared with the customer's "
                    "historical median."
                )

            if bool(signals["new_device"]):

                patterns.append(
                    "Transaction was made using a new device."
                )

            if bool(signals["unseen_region"]):

                patterns.append(
                    "Transaction occurred from a region "
                    "not previously associated with the customer."
                )

            if len(connected_customers) > 1:

                patterns.append(
                    f"The device is associated with "
                    f"{len(connected_customers)} customers."
                )

            if patterns:

                for number, pattern in enumerate(
                    patterns,
                    1
                ):

                    st.warning(
                        f"{number}. {pattern}"
                    )

            else:

                st.success(
                    "No major suspicious patterns detected."
                )


            # -----------------------------
            # Generate Case
            # -----------------------------

            st.subheader(
                "🗂️ Investigation Case"
            )

            case = generate_case(
                result,
                patterns,
                connected_customers
            )

            st.json(case)


            # -----------------------------
            # Download Case JSON
            # -----------------------------

            case_json = case_to_json(case)

            st.download_button(
                label="⬇️ Download Case JSON",
                data=case_json,
                file_name=f"{case['case_id']}.json",
                mime="application/json"
            )
# -----------------------------
# Organizer Reference Case
# -----------------------------

st.divider()

st.subheader("📁 Organizer Reference Case")

case_id = st.selectbox(
    "Select a case",
    ["HHG-008"]
)

if st.button("Load Reference Case"):

    reference_case = load_case(case_id)

    if reference_case is None:
       st.error(
            "Reference case not found."
        )

    else:

        st.success(
            "Reference case loaded successfully."
        )

        st.json(reference_case)            
