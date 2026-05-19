import sqlite3
import pandas as pd

con = sqlite3.connect("calls.db")

print("Connected to calls.db")
print("Type SQL query or type 'exit' to quit\n")

while True:

    query = input("SQL> ").strip()

    if query.lower() == "exit":
        break

    if query == "":
        continue

    try:

        df = pd.read_sql_query(query, con)

        print("\nResult:\n")

        print(df.to_string(index=False))

    except Exception as e:

        print(f"\nError: {e}")

    print()

con.close()

print("Connection closed")