from pathlib import Path
import pandas as pd

project_root = Path(__file__).resolve().parents[2]

file_path = project_root / "data" / "raw" / "Online_Retail.xlsx"

df = pd.read_excel(file_path)

print("Shape:", df.shape)
print("\\nColumns:")
print(df.columns.tolist())

print("\\nFirst 5 rows:")
print(df.head())

print("\\Missing values:")
print(df.isnull().sum())
