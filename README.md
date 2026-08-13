# Retail Sales Data Warehouse

End-to-end Data Engineering project using Python, PySpark, and PostgreSQL.

## Tech Stack
- Python
- PySpark
- PostgreSQL

## Project Goal
Build a retail sales data warehouse with a star schema and automated ETL pipeline.


## Run the Full Pipeline

```bash
source venv/bin/activate
python -m src.orchestration.run_pipeline
```

Or simply:

```bash
./run_pipeline.sh
```

This command performs:
1. Dataset download
2. Data cleaning with PySpark
3. Dimension table creation
4. Fact table creation
5. PostgreSQL loading


## Architecture

Raw Excel Data
    ↓
Python Ingestion
    ↓
PySpark Cleaning
    ↓
Dimension Tables
    ↓
Fact Table
    ↓
PostgreSQL Star Schema
    ↓
Indexes & Materialized Views
    ↓
Analytics Queries

