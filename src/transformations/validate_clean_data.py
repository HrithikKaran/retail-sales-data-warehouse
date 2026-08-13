from pathlib import Path
from pyspark.sql import SparkSession
from pyspark.sql.functions import min, max, countDistinct

project_root = Path(__file__).resolve().parents[2]
processed_dir = project_root / "data" / "processed" / "clean_sales"

spark = (
    SparkSession.builder
    .appName("ValidateCleanData")
    .getOrCreate()
)

df = spark.read.parquet(str(processed_dir))

print("Rows:", df.count())
print("Columns:", len(df.columns))

df.select(
    min("InvoiceDate").alias("min_date"),
    max("InvoiceDate").alias("max_date")
).show()

df.select(
    countDistinct("InvoiceNo").alias("invoices"),
    countDistinct("CustomerID").alias("customers"),
    countDistinct("StockCode").alias("products"),
    countDistinct("Country").alias("countries")
).show()

spark.stop()