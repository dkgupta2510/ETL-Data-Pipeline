import json
import pandas as pd

# load raw data
with open("raw_calls.json") as f:
    df = pd.DataFrame(json.load(f))

# parse timestamps, drop bad rows, convert to IST
df["start_time"] = pd.to_datetime(df["start_time"], utc=True, errors="coerce")
df["end_time"]   = pd.to_datetime(df["end_time"],   utc=True, errors="coerce")
df = df.dropna(subset=["start_time", "end_time"])

df["start_time"] = df["start_time"].dt.tz_convert("Asia/Kolkata")
df["end_time"]   = df["end_time"].dt.tz_convert("Asia/Kolkata")

# dedup — keep latest record per call_id
df = df.sort_values("start_time").drop_duplicates("call_id", keep="last")

# derived columns
df["call_duration_seconds"] = (df["end_time"] - df["start_time"]).dt.total_seconds().astype(int)
df["call_hour"]    = df["start_time"].dt.hour
df["call_date"]    = df["start_time"].dt.date
df["is_weekend"]   = df["start_time"].dt.dayofweek >= 5

# bucket duration
def bucket(secs):
    if secs < 60:   return "short"
    if secs <= 300: return "medium"
    return "long"

df["duration_bucket"]   = df["call_duration_seconds"].apply(bucket)

# impute nulls in amount_promised
df["is_amount_imputed"] = df["amount_promised"].isnull()
df["amount_promised"]   = df["amount_promised"].fillna(0)

df.to_json("transformed_calls.json", orient="records", indent=2, date_format="iso")
print(f"Done — {len(df)} clean records saved")
print(df.head())