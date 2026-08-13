from pathlib import Path
import pandas as pd
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, trim, upper, isnan

# --------------------------------------------------
# Paths
# --------------------------------------------------
project_root = Path(__file__).resolve().parents[2]

raw_file = project_root / "data" / "raw" / "Online_Retail.xlsx"
processed_dir = project_root / "data" / "processed" / "clean_sales"

# --------------------------------------------------
# Read Excel with pandas
# --------------------------------------------------
pdf = pd.read_excel(raw_file)

# --------------------------------------------------
# Start Spark
# --------------------------------------------------
spark = (
    SparkSession.builder
    .appName("RetailSalesCleaning")
    .getOrCreate()
)

df = spark.createDataFrame(pdf)

print("Raw rows:", df.count())

# --------------------------------------------------
# Cleaning
# --------------------------------------------------
clean_df = (
    df
    .filter(col("CustomerID").isNotNull())
    .filter(~isnan(col("CustomerID")))   # remove NaN values
    .filter(col("Description").isNotNull())
    .filter(~col("InvoiceNo").startswith("C"))
    .filter(col("Quantity") > 0)
    .filter(col("UnitPrice") > 0)
)

# Standardize text
clean_df = (
    clean_df
    .withColumn("Description", trim(upper(col("Description"))))
    .withColumn("Country", trim(col("Country")))
)

# Cast types
clean_df = (
    clean_df
    .withColumn("CustomerID", col("CustomerID").cast("long"))
    .withColumn("Quantity", col("Quantity").cast("int"))
    .withColumn("UnitPrice", col("UnitPrice").cast("double"))
)

# Sales amount
clean_df = clean_df.withColumn(
    "sales_amount",
    col("Quantity") * col("UnitPrice")
)

print("Clean rows:", clean_df.count())

# --------------------------------------------------
# Save cleaned data
# --------------------------------------------------
clean_df.write.mode("overwrite").parquet(str(processed_dir))

print(f"Cleaned data saved to: {processed_dir}")

# Show sample
clean_df.show(5, truncate=False)

spark.stop()