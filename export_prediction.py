import sqlite3
import pandas as pd
import os

# Connect to SQLite database
conn = sqlite3.connect("database/hospital.db")

# Read prediction table
df = pd.read_sql("SELECT * FROM patients_prediction", conn)

# Create output folder if needed
os.makedirs("Data", exist_ok=True)

# Save to CSV
df.to_csv("Data/patients_prediction.csv", index=False)

conn.close()

print("patients_prediction.csv created successfully!")
