from pathlib import Path
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, to_date, date_format

#=================
#Paths
#===============
project_root = Path(__file__).resolve().parents[2]

clean_path = project_root / "data" / "processed" / "clean_sales"
warehouse_path = project_root / "data" / "warehouse"

#================================
#Start Spark
#================================
spark = (
    SparkSession.builder
    .appName("BuildFactSales")
    .getOrCreate()
)

#------------------------------------------
#Read Datasets
#-----------------------------------------
sales_df = spark.read.parquet(str(clean_path))

date_df = spark.read.parquet(str(warehouse_path / "dim_date"))
customer_df = spark.read.parquet(str(warehouse_path / "dim_customer"))
product_df = spark.read.parquet(str(warehouse_path / "dim_product"))
country_df = spark.read.parquet(str(warehouse_path / "dim_country"))

#-------------------------------------------
#Prepare Sales data
#-------------------------------------------
sales_df = sales_df.withColumn(
    "invoice_date_only",
    to_date(col("InvoiceDate"))
)

sales_df = sales_df.withColumn(
    "date_key",
    date_format(col("invoice_date_only"), "yyyyMMdd").cast("int")
)

#------------------------------
#Join dimensions
#---------------------------------
fact_df = (
    sales_df
    .join(
        date_df.select("date_key"),
        on="date_key",
        how="inner"
    )
    .join(
        customer_df,
        sales_df.CustomerID == customer_df.customer_id,
        how="inner"
    )
    .join(
        product_df,
        sales_df.StockCode == product_df.stock_code,
        how="inner"
    )
    .join(
        country_df,
        sales_df.Country == country_df.country_name,
        how="inner"
    )
)

#-----------------------------
#Select fact columns
#-----------------------------
fact_df = fact_df.select(
    col("InvoiceNo").alias("invoice_no"),
    col("date_key"),
    col("customer_key"),
    col("product_key"),
    col("country_key"),
    col("Quantity").alias("quantity"),
    col("UnitPrice").alias("unit_price"),
    col("sales_amount")
)

#-------------------------
#Save fact table
#-------------------------
fact_path = warehouse_path / "fact_sales"

fact_df.write.mode("overwrite").parquet(str(fact_path))

#-------------------------
#Validation
#--------------------------
print("Fact rows:", fact_df.count())
print("Fact columns:", len(fact_df.columns))

fact_df.show(5, truncate=False)

spark.stop()