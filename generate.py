import json
import random
from datetime import datetime, timedelta

random.seed(42)

records = []

# create 500 records
for i in range(1, 501):

    start = datetime(2024, 1, 1) + timedelta(
        days=random.randint(0, 90),
        hours=random.randint(8, 20),
        minutes=random.randint(0, 59)
    )

    end = start + timedelta(seconds=random.randint(10, 900))

    record = {
        "call_id": f"CALL_{i}",
        "agent_id": f"AGENT_{random.randint(1,20)}",
        "customer_phone": f"+91{random.randint(7000000000,9999999999)}",
        "start_time": start.isoformat(),
        "end_time": end.isoformat(),
        "call_outcome": random.choice([
            "connected",
            "no_answer",
            "dropped",
            "callback_requested"
        ]),
        "language": random.choice(["Hindi", "English", "Marathi"]),
        "disposition_code": f"D{random.randint(1,10)}",
        "amount_promised": random.choice([
            None,
            round(random.uniform(500, 50000), 2)
        ]),
        "retry_flag": random.choice([True, False])
    }

    records.append(record)

# add missing fields (15%)
required_fields = [
    "call_id",
    "agent_id",
    "customer_phone",
    "start_time",
    "end_time",
    "call_outcome",
    "language",
    "disposition_code",
    "retry_flag"
]

for i in random.sample(range(500), 75):
    field = random.choice(required_fields)
    records[i].pop(field)

#add duplicate records(5%)
for _ in range(25):
    duplicate = random.choice(records).copy()
    records.append(duplicate)

# add malformed timestamps(3%)
for i in random.sample(range(len(records)), 15):
    field = random.choice(["start_time", "end_time"])

    if field in records[i]:
        records[i][field] = "INVALID_DATE"

random.shuffle(records)


with open("raw_calls.json", "w") as file:
    json.dump(records, file, indent=2)

print("raw_calls.json created successfully")