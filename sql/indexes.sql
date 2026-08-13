-- Fact table foreign key indexes
CREATE INDEX IF NOT EXISTS idx_fact_sales_date_key
ON retail_dw.fact_sales(date_key);

CREATE INDEX IF NOT EXISTS idx_fact_sales_customer_key
ON retail_dw.fact_sales(customer_key);

CREATE INDEX IF NOT EXISTS idx_fact_sales_product_key
ON retail_dw.fact_sales(product_key);

CREATE INDEX IF NOT EXISTS idx_fact_sales_country_key
ON retail_dw.fact_sales(country_key);

-- Common search indexes
CREATE INDEX IF NOT EXISTS idx_fact_sales_invoice_no
ON retail_dw.fact_sales(invoice_no);

CREATE INDEX IF NOT EXISTS idx_dim_product_stock_code
ON retail_dw.dim_product(stock_code);

CREATE INDEX IF NOT EXISTS idx_dim_customer_customer_id
ON retail_dw.dim_customer(customer_id);

CREATE INDEX IF NOT EXISTS idx_dim_country_country_name
ON retail_dw.dim_country(country_name);