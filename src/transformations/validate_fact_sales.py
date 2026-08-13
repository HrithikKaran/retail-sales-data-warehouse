from pathlib import Path
from pyspark.sql import SparkSession
from pyspark.sql.functions import sum as spark_sum, countDistinct

project_root = Path(__file__).resolve().parents[2]
fact_path = project_root / "data" / "warehouse" / "fact_sales"

spark = SparkSession.builder.appName("ValidateFactSales").getOrCreate()

df = spark.read.parquet(str(fact_path))

print("Rows:", df.count())
print("Columns:", len(df.columns))

df.select(
    spark_sum("sales_amount").alias("total_sales")
).show()

df.select(
    countDistinct("invoice_no").alias("invoices"),
    countDistinct("customer_key").alias("customers"),
    countDistinct("product_key").alias("products")
).show()

spark.stop()