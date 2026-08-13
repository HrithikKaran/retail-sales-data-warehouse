from pathlib import Path
from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    col, to_date, year, month, quarter,
    dayofmonth, dayofweek, date_format, when,
    monotonically_increasing_id, row_number
)
from pyspark.sql.window import Window

# --------------------------------------------------
# Paths
# --------------------------------------------------
project_root = Path(__file__).resolve().parents[2]

clean_path = project_root / "data" / "processed" / "clean_sales"
warehouse_path = project_root / "data" / "warehouse"

# --------------------------------------------------
# Start Spark
# --------------------------------------------------
spark = (
    SparkSession.builder
    .appName("BuildDimensions")
    .getOrCreate()
)

df = spark.read.parquet(str(clean_path))

# ==================================================
# DIM DATE
# ==================================================
date_df = (
    df.select(to_date(col("InvoiceDate")).alias("full_date"))
      .distinct()
)

date_df = (
    date_df
    .withColumn("date_key", date_format(col("full_date"), "yyyyMMdd").cast("int"))
    .withColumn("day", dayofmonth(col("full_date")))
    .withColumn("month", month(col("full_date")))
    .withColumn("month_name", date_format(col("full_date"), "MMMM"))
    .withColumn("quarter", quarter(col("full_date")))
    .withColumn("year", year(col("full_date")))
    .withColumn("day_of_week", dayofweek(col("full_date")))
    .withColumn("day_name", date_format(col("full_date"), "EEEE"))
    .withColumn(
        "is_weekend",
        when(dayofweek(col("full_date")).isin(1, 7), True).otherwise(False)
    )
)

date_df.write.mode("overwrite").parquet(str(warehouse_path / "dim_date"))

# ==================================================
# DIM CUSTOMER
# ==================================================
customer_window = Window.orderBy("customer_id")

customer_df = (
    df.select(col("CustomerID").cast("long").alias("customer_id"))
      .distinct()
      .withColumn("customer_key", row_number().over(customer_window))
      .select("customer_key", "customer_id")
)

customer_df.write.mode("overwrite").parquet(str(warehouse_path / "dim_customer"))

# ==================================================
# DIM PRODUCT
# ==================================================
product_window = Window.orderBy("stock_code")

product_df = (
    df.select(
        col("StockCode").alias("stock_code"),
        col("Description").alias("description")
    )
    .dropDuplicates(["stock_code"])
    .withColumn("product_key", row_number().over(product_window))
    .select("product_key", "stock_code", "description")
)

product_df.write.mode("overwrite").parquet(str(warehouse_path / "dim_product"))

# ==================================================
# DIM COUNTRY
# ==================================================
country_window = Window.orderBy("country_name")

country_df = (
    df.select(col("Country").alias("country_name"))
      .distinct()
      .withColumn("country_key", row_number().over(country_window))
      .select("country_key", "country_name")
)

country_df.write.mode("overwrite").parquet(str(warehouse_path / "dim_country"))

# --------------------------------------------------
# Print counts
# --------------------------------------------------
print("dim_date rows:", date_df.count())
print("dim_customer rows:", customer_df.count())
print("dim_product rows:", product_df.count())
print("dim_country rows:", country_df.count())

spark.stop()