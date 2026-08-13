from pathlib import Path
import requests


DATA_URL = "https://archive.ics.uci.edu/ml/machine-learning-databases/00352/Online%20Retail.xlsx"

project_root = Path(__file__).resolve().parents[2]
raw_dir = project_root / "data" / "raw"
raw_dir.mkdir(parents=True, exist_ok=True)

output_file = raw_dir / "Online_Retail.xlsx"

print(f"Downloading datasets to {output_file}...")

response = requests.get(DATA_URL, timeout=60)
response.raise_for_status()

with open(output_file, "wb") as f:
    f.write(response.content)


print("Download Completed Successfully!")
print(f"File size: {output_file.stat().st_size / 1024:.2f} KB")

