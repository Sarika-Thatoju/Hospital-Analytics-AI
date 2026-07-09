import pandas as pd
import sqlite3

print("="*60)
print("SMART HOSPITAL DECISION SUPPORT SYSTEM")
print("="*60)

# ---------------------------------------
# Connect Database
# ---------------------------------------

conn = sqlite3.connect("database/hospital.db")

df = pd.read_sql(
    "SELECT * FROM patients_prediction",
    conn
)

recommendations = []

# ---------------------------------------
# ICU Occupancy
# ---------------------------------------

icu = len(df[df["Ward"]=="ICU"])

total = len(df)

icu_percent = round((icu/total)*100,2)

if icu_percent > 20:
    recommendations.append([
        "ICU Occupancy",
        f"{icu_percent} %",
        "Increase ICU Beds"
    ])
else:
    recommendations.append([
        "ICU Occupancy",
        f"{icu_percent} %",
        "Current Capacity is Sufficient"
    ])

# ---------------------------------------
# Waiting Time
# ---------------------------------------

avg_wait = round(df["Waiting_Time_Minutes"].mean(),2)

if avg_wait > 90:
    recommendations.append([
        "Average Waiting Time",
        f"{avg_wait} Minutes",
        "Deploy Additional Doctors"
    ])
else:
    recommendations.append([
        "Average Waiting Time",
        f"{avg_wait} Minutes",
        "Waiting Time is Acceptable"
    ])

# ---------------------------------------
# Critical Patients
# ---------------------------------------

critical = len(df[df["Predicted_Risk"]=="Critical"])

if critical > 5000:
    recommendations.append([
        "Critical Patients",
        critical,
        "Allocate More Emergency Staff"
    ])
else:
    recommendations.append([
        "Critical Patients",
        critical,
        "Current Staff is Sufficient"
    ])

# ---------------------------------------
# Average Stay
# ---------------------------------------

stay = round(df["Length_of_Stay"].mean(),2)

if stay > 5:
    recommendations.append([
        "Average Stay",
        f"{stay} Days",
        "Review Discharge Planning"
    ])
else:
    recommendations.append([
        "Average Stay",
        f"{stay} Days",
        "Hospital Stay is Normal"
    ])

# ---------------------------------------
# High Risk Patients
# ---------------------------------------

high = len(df[df["Predicted_Risk"]=="High"])

if high > 8000:
    recommendations.append([
        "High Risk Patients",
        high,
        "Prioritize Monitoring"
    ])
else:
    recommendations.append([
        "High Risk Patients",
        high,
        "Normal Monitoring"
    ])

# ---------------------------------------
# Bed Occupancy
# ---------------------------------------

beds = df["Bed_Number"].nunique()

occupied = len(df)

occupancy = round((occupied/(beds*100))*100,2)

if occupancy > 80:
    recommendations.append([
        "Bed Occupancy",
        f"{occupancy} %",
        "Prepare Additional Beds"
    ])
else:
    recommendations.append([
        "Bed Occupancy",
        f"{occupancy} %",
        "Beds Available"
    ])

# ---------------------------------------
# Save Recommendation Table
# ---------------------------------------

recommendation_df = pd.DataFrame(
    recommendations,
    columns=[
        "Metric",
        "Current_Value",
        "Recommendation"
    ]
)

recommendation_df.to_sql(
    "hospital_recommendations",
    conn,
    if_exists="replace",
    index=False
)

print("\nRecommendations")

print(recommendation_df)

conn.close()

print("\nSTEP 9 COMPLETED SUCCESSFULLY")