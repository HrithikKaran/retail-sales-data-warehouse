-- =========================================
-- 1. Total Sales
-- =========================================
SELECT ROUND(SUM(sales_amount)::numeric, 2) AS total_sales
FROM retail_dw.fact_sales;

-- =========================================
-- 2. Top 10 Customers by Revenue
-- =========================================
SELECT
    c.customer_id,
    ROUND(SUM(f.sales_amount)::numeric, 2) AS revenue
FROM retail_dw.fact_sales f
JOIN retail_dw.dim_customer c
    ON f.customer_key = c.customer_key
GROUP BY c.customer_id
ORDER BY revenue DESC
LIMIT 10;

-- =========================================
-- 3. Top 10 Products by Revenue
-- =========================================
SELECT
    p.stock_code,
    p.description,
    ROUND(SUM(f.sales_amount)::numeric, 2) AS revenue
FROM retail_dw.fact_sales f
JOIN retail_dw.dim_product p
    ON f.product_key = p.product_key
GROUP BY p.stock_code, p.description
ORDER BY revenue DESC
LIMIT 10;

-- =========================================
-- 4. Sales by Country
-- =========================================
SELECT
    c.country_name,
    ROUND(SUM(f.sales_amount)::numeric, 2) AS revenue
FROM retail_dw.fact_sales f
JOIN retail_dw.dim_country c
    ON f.country_key = c.country_key
GROUP BY c.country_name
ORDER BY revenue DESC
LIMIT 10;

-- =========================================
-- 5. Monthly Sales Trend
-- =========================================
SELECT
    d.year,
    d.month,
    ROUND(SUM(f.sales_amount)::numeric, 2) AS revenue
FROM retail_dw.fact_sales f
JOIN retail_dw.dim_date d
    ON f.date_key = d.date_key
GROUP BY d.year, d.month
ORDER BY d.year, d.month;