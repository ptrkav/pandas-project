import pandas as pd
import sqlite3
import os

file_path = os.path.abspath("data/employees.csv")  # Get absolute path
print(f"Looking for file at: {file_path}")

df = pd.read_csv(file_path)  # Use absolute path

# Data Cleaning: Convert date format
df["hire_date"] = pd.to_datetime(df["hire_date"])

# Add a new column: Years of Service
df["years_of_service"] = 2024 - df["hire_date"].dt.year

# Connect to SQLite database
conn = sqlite3.connect("data/employees.db")
cursor = conn.cursor()

# Create table if it doesn't exist
cursor.execute("""
    CREATE TABLE IF NOT EXISTS employees (
        employee_id INTEGER PRIMARY KEY,
        name TEXT,
        age INTEGER,
        department TEXT,
        salary INTEGER,
        hire_date TEXT,
        years_of_service INTEGER
    )
""")

# Insert data into database
df.to_sql("employees", conn, if_exists="replace", index=False)

# Query data to verify migration
print("Migrated Data Preview:")
print(pd.read_sql("SELECT * FROM employees WHERE department = 'IT'", conn))

# Save transformed data back to a new CSV file
df.to_csv("data/migrated_employees.csv", index=False)

# Close the database connection
conn.close()