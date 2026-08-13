--Create Schema
CREATE SCHEMA IF NOT EXISTS retail_dw;

--====================================
-- Dimension: Date
--====================================
CREATE TABLE IF NOT EXISTS retail_dw.dim_date (
    date_key    INTEGER PRIMARY KEY,
    full_date   DATE NOT NULL,
    day         INTEGER,
    month       INTEGER,
    month_name  VARCHAR(20),
    quarter     INTEGER,
    year        INTEGER,
    day_of_week INTEGER,
    day_name    VARCHAR(20),
    is_weekend  BOOLEAN

);

-- ====================================
-- Dimension: Customer
-- ====================================
CREATE TABLE IF NOT EXISTS retail_dw.dim_customer (
    customer_key    SERIAL PRIMARY KEY,
    customer_id     BIGINT UNIQUE
);

-- ====================================
-- Dimension: Product
-- ====================================
CREATE TABLE IF NOT EXISTS retail_dw.dim_product (
    product_key    SERIAL PRIMARY KEY,
    stock_code     VARCHAR(50) UNIQUE,
    description    TEXT
);


-- ====================================
-- Dimension: Country
-- ====================================
CREATE TABLE IF NOT EXISTS retail_dw.dim_country (
    country_key   SERIAL PRIMARY KEY,
    country_name   VARCHAR(100) UNIQUE
);


-- ====================================
-- Fact: Sales
-- ====================================
CREATE TABLE IF NOT EXISTS retail_dw.fact_sales (
    sales_key       BIGSERIAL PRIMARY KEY,
    invoice_no      VARCHAR(20),
    date_key        INTEGER REFERENCES retail_dw.dim_date(date_key),
    customer_key    INTEGER REFERENCES retail_dw.dim_customer(customer_key),
    product_key     INTEGER REFERENCES retail_dw.dim_product(product_key),
    country_key     INTEGER REFERENCES retail_dw.dim_country(country_key),
    quantity        INTEGER,
    unit_price      NUMERIC(10,2),
    sales_amount    NUMERIC(12,2)
);