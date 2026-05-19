
import sqlite3, argparse
import pandas as pd

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--db-path", default="calls.db")
    db = parser.parse_args().db_path

    con = sqlite3.connect(db)
    print(f" Connected to '{db}'")
    print("   Type your SQL query, then press Enter twice to run.")
    print("   Type 'exit' to quit.\n")

    while True:
        print("SQL> ", end="", flush=True)
        lines = []
        while True:
            line = input()
            if line.lower() == "exit":
                con.close()
                print("Bye!")
                return
            if line == "" and lines: 
                break
            if line:
                lines.append(line)

        query = " ".join(lines)

        try:
            df = pd.read_sql_query(query, con)
            print(f"\n {len(df)} rows returned:")
            print(df.to_string(index=False))
            save = input("\nSave to CSV? (y/n): ").strip().lower()
            if save == "y":
                name = input("Filename (e.g. result.csv): ").strip()
                df.to_csv(name, index=False)
                print(f" Saved → {name}")

        except Exception as e:
            print(f"Error: {e}")

        print()

if __name__ == "__main__":
    main()
    