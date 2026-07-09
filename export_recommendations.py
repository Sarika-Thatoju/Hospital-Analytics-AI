import sqlite3
import pandas as pd

# Connect to database
conn = sqlite3.connect("database/hospital.db")

# Read recommendation table
df = pd.read_sql_query(
    "SELECT * FROM hospital_recommendations",
    conn
)

# Save CSV in Data folder
df.to_csv("Data/hospital_recommendations.csv", index=False)

conn.close()

print("✅ hospital_recommendations.csv exported successfully!")
