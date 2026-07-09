import pandas as pd
import os

# -----------------------------
# File Paths
# -----------------------------
input_file = "Data/Hospital_Synthetic_Dataset_50000.xlsx"
output_folder = "data"

# Create output folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

# -----------------------------
# Read Excel File
# -----------------------------
print("Reading dataset...")
df = pd.read_excel(input_file, engine="openpyxl")

print("\nOriginal Dataset Shape:")
print(df.shape)

# -----------------------------
# Remove Duplicate Records
# -----------------------------
duplicates = df.duplicated().sum()
print(f"\nDuplicate Records Found: {duplicates}")

df = df.drop_duplicates()

# -----------------------------
# Handle Missing Values
# -----------------------------
print("\nMissing Values Before Cleaning:")
print(df.isnull().sum())

# Fill numeric columns with median
numeric_columns = df.select_dtypes(include=['int64', 'float64']).columns
for col in numeric_columns:
    df[col].fillna(df[col].median(), inplace=True)

# Fill text columns with "Unknown"
text_columns = df.select_dtypes(include=['object']).columns
for col in text_columns:
    df[col].fillna("Unknown", inplace=True)

# -----------------------------
# Convert Date Columns
# -----------------------------
df['Admission_Date'] = pd.to_datetime(df['Admission_Date'])
df['Discharge_Date'] = pd.to_datetime(df['Discharge_Date'])

# -----------------------------
# Remove Invalid Ages
# -----------------------------
df = df[(df['Age'] >= 0) & (df['Age'] <= 100)]

# -----------------------------
# Standardize Text Columns
# -----------------------------
df['Gender'] = df['Gender'].str.title()
df['Severity'] = df['Severity'].str.title()
df['Status'] = df['Status'].str.title()

# -----------------------------
# Create New Column
# -----------------------------
df['Length_of_Stay'] = (
    df['Discharge_Date'] - df['Admission_Date']
).dt.days

# -----------------------------
# Save Clean Dataset
# -----------------------------
csv_file = os.path.join(output_folder, "hospital_clean.csv")
excel_file = os.path.join(output_folder, "hospital_clean.xlsx")

df.to_csv(csv_file, index=False)
df.to_excel(excel_file, index=False)

# -----------------------------
# Display Summary
# -----------------------------
print("\nCleaning Completed Successfully!")

print("\nFinal Dataset Shape:")
print(df.shape)

print("\nMissing Values After Cleaning:")
print(df.isnull().sum())

print("\nDataset Preview:")
print(df.head())

print("\nFiles Saved:")
print(csv_file)
print(excel_file)