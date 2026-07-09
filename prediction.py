import pandas as pd
import sqlite3

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

print("="*60)
print("PATIENT RISK PREDICTION")
print("="*60)

# -----------------------------
# Connect Database
# -----------------------------

conn = sqlite3.connect("database/hospital.db")

df = pd.read_sql("SELECT * FROM patients", conn)

print("\nDataset Loaded Successfully")
print("Total Records:", len(df))

# -----------------------------
# Encode Categorical Columns
# -----------------------------

le_gender = LabelEncoder()
le_disease = LabelEncoder()
le_ward = LabelEncoder()
le_department = LabelEncoder()
le_severity = LabelEncoder()

df["Gender"] = le_gender.fit_transform(df["Gender"])

df["Disease"] = le_disease.fit_transform(df["Disease"])

df["Ward"] = le_ward.fit_transform(df["Ward"])

df["Department"] = le_department.fit_transform(df["Department"])

# Target Variable

df["Severity"] = le_severity.fit_transform(df["Severity"])

# -----------------------------
# Features
# -----------------------------

X = df[[
    "Age",
    "Gender",
    "Disease",
    "Ward",
    "Waiting_Time_Minutes",
    "Length_of_Stay",
    "Department"
]]

y = df["Severity"]

# -----------------------------
# Split Data
# -----------------------------

X_train,X_test,y_train,y_test=train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42
)

# -----------------------------
# Train Model
# -----------------------------

model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)

model.fit(X_train,y_train)

# -----------------------------
# Prediction
# -----------------------------

prediction=model.predict(X_test)

accuracy=accuracy_score(y_test,prediction)

print("\nModel Accuracy")

print(round(accuracy*100,2),"%")

# -----------------------------
# Predict Entire Dataset
# -----------------------------

df["Predicted_Risk"]=model.predict(X)

# -----------------------------
# Convert Numbers Back
# -----------------------------

df["Predicted_Risk"]=le_severity.inverse_transform(df["Predicted_Risk"])

# -----------------------------
# Save Results
# -----------------------------

df.to_sql(
    "patients_prediction",
    conn,
    if_exists="replace",
    index=False
)

conn.close()

print("\nPrediction Table Created")

print("Table Name : patients_prediction")

print("\nSTEP 8 COMPLETED SUCCESSFULLY")
