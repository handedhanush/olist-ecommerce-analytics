import pandas as pd
import sqlite3

print("=" * 55)
print("LOADING DATA INTO DATABASE")
print("=" * 55)

# Load the clean transformed file
df = pd.read_csv("transformed_data.csv")

# Create a SQLite database file
# SQLite is a lightweight database that lives as a single file on your computer
# No server setup needed — Python handles everything
conn = sqlite3.connect("olist.db")

# Load all the data into a table called "sales" inside the database
# if_exists="replace" means: if the table already exists, delete it and start fresh
df.to_sql("sales", conn, if_exists="replace", index=False)

# Confirm it loaded correctly by running a count query
verify = pd.read_sql_query("SELECT COUNT(*) AS total_rows FROM sales", conn)
print(f"\nRows loaded into database: {verify['total_rows'][0]:,}")

# Show the first 3 rows straight from the database as a final check
print("\nFirst 3 rows from the database:")
preview = pd.read_sql_query("SELECT * FROM sales LIMIT 3", conn)
print(preview.to_string(index=False))

conn.close()
print("\nLoad complete! Database saved as olist.db")
print("\nFull ETL pipeline complete:")
print("  E — Extract    (etl_extract.py)")
print("  T — Transform  (etl_transform.py)")
print("  L — Load       (etl_load.py)")