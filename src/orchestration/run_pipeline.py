import subprocess
import sys
from pathlib import Path

project_root = Path(__file__).resolve().parents[2]

steps = [
    ("Download dataset", "python -m src.ingestion.download_data"),
    ("Clean data", "python -m src.transformations.clean_data"),
    ("Build dimensions", "python -m src.transformations.build_dimensions"),
    ("Build fact table", "python -m src.transformations.build_fact_sales"),
    ("Load to PostgreSQL", "python -m src.load.load_to_postgres"),
]

def run_step(name, command):

    print("\\n" + "=" * 60)
    print(f"STEP: {name}")
    print("=" * 60)

    result = subprocess.run(command, shell=True, cwd=project_root)

    if result.returncode != 0:
        print(f"\\n❌ Pipeline failed at step: {name}")
        sys.exit(result.returncode)

    print(f"\\n✅ Completed: {name}")

def main():

    print("Starting Retail Sales Data Warehouse Pipeline")

    for name, command in steps:
        run_step(name, command)

    print("\\n🎉 Pipeline completed successfully.")

if __name__ == "__main__":
    main()