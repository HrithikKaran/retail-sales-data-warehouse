-- =========================================
-- Monthly Sales Summary
-- =========================================
CREATE MATERIALIZED VIEW IF NOT EXISTS retail_dw.mv_monthly_sales AS
SELECT
    d.year,
    d.month,
    d.month_name,
    ROUND(SUM(f.sales_amount)::numeric, 2) AS total_sales,
    SUM(f.quantity) AS total_quantity,
    COUNT(DISTINCT f.invoice_no) AS total_invoices
FROM retail_dw.fact_sales f
JOIN retail_dw.dim_date d
    ON f.date_key = d.date_key
GROUP BY d.year, d.month, d.month_name
ORDER BY d.year, d.month;

-- =========================================
-- Top Products Summary
-- =========================================
CREATE MATERIALIZED VIEW IF NOT EXISTS retail_dw.mv_top_products AS
SELECT
    p.product_key,
    p.stock_code,
    p.description,
    SUM(f.quantity) AS total_quantity,
    ROUND(SUM(f.sales_amount)::numeric, 2) AS total_sales
FROM retail_dw.fact_sales f
JOIN retail_dw.dim_product p
    ON f.product_key = p.product_key
GROUP BY p.product_key, p.stock_code, p.description
ORDER BY total_sales DESC;