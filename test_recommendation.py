import sqlite3
import pandas as pd

conn = sqlite3.connect("database/hospital.db")

df = pd.read_sql(
    "SELECT * FROM hospital_recommendations",
    conn
)

print(df)

conn.close()
