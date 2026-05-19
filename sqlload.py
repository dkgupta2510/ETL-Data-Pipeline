import pandas as pd
import sqlite3
from datetime import datetime



df = pd.read_json("transformed_calls.json")


conn = sqlite3.connect("calls.db")
cursor = conn.cursor()
cursor.execute("DROP TABLE IF EXISTS calls")

cursor.execute("""
CREATE TABLE calls (

    call_id TEXT PRIMARY KEY,
    agent_id TEXT,
    customer_phone TEXT,
    start_time TEXT,
    end_time TEXT,
    call_outcome TEXT,
    language TEXT,
    disposition_code TEXT,
    amount_promised REAL,
    retry_flag BOOLEAN,

    call_duration_seconds INTEGER,
    call_hour INTEGER,
    call_date TEXT,
    is_weekend BOOLEAN,
    duration_bucket TEXT,
    is_amount_imputed BOOLEAN
)
""")

# Create ingestion log tabl
cursor.execute("""
CREATE TABLE ingestion_log (

    run_timestamp TEXT,
    records_processed INTEGER,
    rejected_count INTEGER
)
""")
for _, row in df.iterrows():

    cursor.execute("""
    INSERT OR REPLACE INTO calls VALUES (
        ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
        ?, ?, ?, ?, ?, ?
    )
    """, (

        row["call_id"],
        row["agent_id"],
        row["customer_phone"],
        str(row["start_time"]),
        str(row["end_time"]),
        row["call_outcome"],
        row["language"],
        row["disposition_code"],
        row["amount_promised"],
        bool(row["retry_flag"]),

        row["call_duration_seconds"],
        row["call_hour"],
        str(row["call_date"]),
        bool(row["is_weekend"]),
        row["duration_bucket"],
        bool(row["is_amount_imputed"])
    ))

records_processed = len(df)

#read rejected count
try:
    rejected_df = pd.read_json("rejected_log.json")
    rejected_count = len(rejected_df)

except:
    rejected_count = 0

cursor.execute("""
INSERT INTO ingestion_log VALUES (?, ?, ?)
""", (
    datetime.now().isoformat(),
    records_processed,
    rejected_count
))
conn.commit()
conn.close()

print("\n===== DATA LOADED SUCCESSFULLY =====")

print(f"Records Loaded : {records_processed}")
print(f"Rejected Count : {rejected_count}")

print("\nSQLite Database Created: calls.db")