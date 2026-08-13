from pathlib import Path
from pyspark.sql import SparkSession

project_root = Path(__file__).resolve().parents[2]
warehouse_path = project_root / "data" / "warehouse"

spark = SparkSession.builder.appName("CheckDimensions").getOrCreate()

for table in ["dim_date", "dim_customer", "dim_product", "dim_country"]:
    print(f"\\n ===== {table} ====")
    df = spark.read.parquet(str(warehouse_path / table))
    print("Rows: ", df.count())
    df.show(5, truncate=False)


spark.stop()