from pathlib import Path
from sqlalchemy import create_engine, text
import pandas as pd

from config.db_config import DB_CONFIG

# --------------------------------------------------
# Paths
# --------------------------------------------------
project_root = Path(__file__).resolve().parents[2]
warehouse_path = project_root / "data" / "warehouse"

# --------------------------------------------------
# Database connection
# --------------------------------------------------
connection_string = (
    f"postgresql+psycopg2://{DB_CONFIG['user']}:{DB_CONFIG['password']}"
    f"@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}"
)

engine = create_engine(connection_string)

# --------------------------------------------------
# Load order
# --------------------------------------------------
tables = [
    "dim_date",
    "dim_customer",
    "dim_product",
    "dim_country",
    "fact_sales"
]

# --------------------------------------------------
# Truncate existing data
# --------------------------------------------------
with engine.begin() as conn:
    conn.execute(text("TRUNCATE TABLE retail_dw.fact_sales RESTART IDENTITY CASCADE"))
    conn.execute(text("TRUNCATE TABLE retail_dw.dim_country RESTART IDENTITY CASCADE"))
    conn.execute(text("TRUNCATE TABLE retail_dw.dim_product RESTART IDENTITY CASCADE"))
    conn.execute(text("TRUNCATE TABLE retail_dw.dim_customer RESTART IDENTITY CASCADE"))
    conn.execute(text("TRUNCATE TABLE retail_dw.dim_date RESTART IDENTITY CASCADE"))

print("Existing warehouse data truncated.")

# --------------------------------------------------
# Load tables
# --------------------------------------------------
for table in tables:

    print(f"\\nLoading {table} ...")

    parquet_path = warehouse_path / table

    df = pd.read_parquet(parquet_path)

    print(f"Rows to load: {len(df)}")

    df.to_sql(
        name=table,
        con=engine,
        schema="retail_dw",
        if_exists="append",
        index=False,
        method="multi",
        chunksize=10000
    )

    print(f"{table} loaded successfully.")

print("\\nAll warehouse tables loaded into PostgreSQL successfully.")