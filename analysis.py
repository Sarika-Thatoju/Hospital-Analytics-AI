import pandas as pd
import os

df = pd.read_csv("Data/hospital_clean.csv")

summary = []

summary.append(["Total Patients", len(df)])
summary.append(["Average Age", round(df["Age"].mean(),2)])
summary.append(["Average Waiting Time", round(df["Waiting_Time_Minutes"].mean(),2)])
summary.append(["Average Length of Stay", round(df["Length_of_Stay"].mean(),2)])

summary_df = pd.DataFrame(summary, columns=["Metric","Value"])

os.makedirs("reports", exist_ok=True)

summary_df.to_csv("reports/summary_report.csv", index=False)

print(summary_df)

print("\nSummary Report Saved Successfully!")
