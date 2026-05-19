import json
import pandas as pd
from datetime import datetime


with open("raw_calls.json", "r") as file:
    records = json.load(file)


# Required schema


required_fields = {
    "call_id": str,
    "agent_id": str,
    "customer_phone": str,
    "start_time": str,
    "end_time": str,
    "call_outcome": str,
    "language": str,
    "disposition_code": str,
    "retry_flag": bool
}


# Validation containers
valid_records = []
rejected_log = []

seen_call_ids = set()

for record in records:

    reject_reason = None

    # check missing
    for field, dtype in required_fields.items():

        if field not in record:
            reject_reason = f"missing field: {field}"
            break

    # check duplicate 
    if not reject_reason:
        if record["call_id"] in seen_call_ids:
            reject_reason = "duplicate record"
        else:
            seen_call_ids.add(record["call_id"])

    # check bad data types
    if not reject_reason:

        for field, dtype in required_fields.items():

            if not isinstance(record[field], dtype):
                reject_reason = f"bad type: {field}"
                break

    # check malformed timestamps
    if not reject_reason:

        try:
            datetime.fromisoformat(record["start_time"])
            datetime.fromisoformat(record["end_time"])

        except:
            reject_reason = "bad type: malformed timestamp"

   
    if reject_reason:

        rejected_log.append({
            "record": record,
            "reason": reject_reason
        })

    else:
        valid_records.append(record)


raw_df = pd.DataFrame(valid_records)

rejected_df = pd.DataFrame(rejected_log)
print("\n===== INGESTION SUMMARY =====")

print(f"Total Records Read     : {len(records)}")
print(f"Total Valid Records    : {len(valid_records)}")
print(f"Total Rejected Records : {len(rejected_log)}")

print("\nRejection Breakdown:")

print(
    rejected_df["reason"]
    .value_counts()
)


# Save rejected log
rejected_df.to_json(
    "rejected_log.json",
    orient="records",
    indent=2
)

print("\nRejected log saved as rejected_log.json")

raw_df.to_json(
    "clean_valid_records.json",
    orient="records",
    indent=2
)

print("Valid records saved as clean_valid_records.json")