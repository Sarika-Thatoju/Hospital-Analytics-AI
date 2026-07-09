import sqlite3
import pandas as pd

conn = sqlite3.connect("database/hospital.db")

query = """
SELECT Patient_ID,
Age,
Disease,
Severity,
Predicted_Risk
FROM patients_prediction
LIMIT 20;
"""

df = pd.read_sql(query, conn)

print(df)

conn.close()