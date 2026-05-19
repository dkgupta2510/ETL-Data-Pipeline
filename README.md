# ETL Call Records Pipeline

This folder contains a simple end-to-end ETL pipeline for call record data. It simulates raw input, validates and cleans the data, transforms it for analysis, loads it into SQLite, and provides an interactive query interface.

## Project Flow

1. `generate.py` — generate synthetic `raw_calls.json` with simulated call records and injected data issues such as missing required fields, duplicates, and malformed timestamps.
2. `deduplicate.py` — validate raw records, reject bad records, remove duplicates, and save good records as `clean_valid_records.json`. Rejected entries are logged to `rejected_log.json`.
3. `pipeline.py` — transform cleaned records:
   - parse and normalize timestamps to `Asia/Kolkata`
   - deduplicate by `call_id`, keeping the latest `start_time`
   - compute `call_duration_seconds`, `call_hour`, `call_date`, `is_weekend`, and `duration_bucket`
   - impute missing `amount_promised` and flag imputed values
   - save output as `transformed_calls.json`
4. `sqlload.py` — load transformed records into SQLite `calls.db` and save ingestion metadata in `ingestion_log`.
5. `queries.py` — launch an interactive SQL prompt against `calls.db` for ad hoc analysis.

## Files

- `generate.py` — raw data generation with noise injection
- `raw_calls.json` — generated unvalidated input data
- `deduplicate.py` — data validation and rejection logic
- `clean_valid_records.json` — cleaned records after validation
- `rejected_log.json` — detailed reject reasons for invalid input
- `pipeline.py` — transformation and feature engineering
- `transformed_calls.json` — final transformed data ready for loading
- `sqlload.py` — SQLite load script with idempotent inserts
- `calls.db` — SQLite database containing the `calls` table and ingestion log
- `queries.py` — interactive SQL console for the database
- `samplequeries.txt` — example SQL queries
- `requirements.txt` — Python dependencies
- `outputs/` — saved query result CSVs

## Requirements

Install dependencies:

```bash
pip install -r requirements.txt
```

## Run Order

```bash
python generate.py
python pipeline.py
python deduplicate.py
python sqlload.py
python queries.py
```

## What I’d do differently at scale
-Replace JSON files with a columnar format like Parquet or a streaming source, because JSON does not scale well for large volumes.
-Use a production-grade data warehouse or OLAP store instead of SQLite: PostgreSQL, Snowflake, BigQuery, or Redshift.
-Avoid dropping and recreating tables on each load; use proper staging, merge/upsert logic, and partitioned storage.
