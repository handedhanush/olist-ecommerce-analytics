import pandas as pd
import sqlite3

# Connect to the database we created in etl_load.py
conn = sqlite3.connect("olist.db")

print("=" * 55)
print("SQL ANALYSIS — 5 Business Queries")
print("=" * 55)

results = {}  # we store all results here and export to Excel at the end

# ── QUERY 1: Revenue Trend by Month ──────────────────────────
# How did the business grow month by month?

query_1 = """
    SELECT
        year,
        month,
        month_name,
        COUNT(DISTINCT order_id)    AS total_orders,
        ROUND(SUM(revenue), 2)      AS total_revenue,
        ROUND(AVG(revenue), 2)      AS avg_order_value
    FROM sales
    GROUP BY year, month
    ORDER BY year, month
"""
results["Monthly Revenue"] = pd.read_sql_query(query_1, conn)
print("\n--- Query 1: Monthly Revenue Trend ---")
print(results["Monthly Revenue"].to_string(index=False))

# ── QUERY 2: Top 10 Product Categories ───────────────────────
# Which product types bring in the most money and have the best reviews?

query_2 = """
    SELECT
        category,
        COUNT(DISTINCT order_id)        AS total_orders,
        ROUND(SUM(revenue), 2)          AS total_revenue,
        ROUND(AVG(revenue), 2)          AS avg_order_value,
        ROUND(AVG(review_score), 2)     AS avg_review_score
    FROM sales
    WHERE category != 'Unknown'
    GROUP BY category
    ORDER BY total_revenue DESC
    LIMIT 10
"""
results["Top 10 Categories"] = pd.read_sql_query(query_2, conn)
print("\n--- Query 2: Top 10 Categories ---")
print(results["Top 10 Categories"].to_string(index=False))

# ── QUERY 3: Revenue by Customer State ───────────────────────
# Which Brazilian states order the most?

query_3 = """
    SELECT
        customer_state,
        COUNT(DISTINCT order_id)        AS total_orders,
        ROUND(SUM(revenue), 2)          AS total_revenue,
        ROUND(AVG(delivery_days), 1)    AS avg_delivery_days
    FROM sales
    GROUP BY customer_state
    ORDER BY total_revenue DESC
    LIMIT 10
"""
results["Revenue by State"] = pd.read_sql_query(query_3, conn)
print("\n--- Query 3: Top States by Revenue ---")
print(results["Revenue by State"].to_string(index=False))

# ── QUERY 4: Late Delivery Impact on Reviews ─────────────────
# Do late deliveries actually get worse reviews? Prove it with numbers.

query_4 = """
    SELECT
        CASE WHEN is_late = 1 THEN 'Late' ELSE 'On Time' END   AS delivery_status,
        COUNT(*)                                                 AS total_orders,
        ROUND(AVG(delivery_days), 1)                            AS avg_delivery_days,
        ROUND(AVG(review_score), 2)                             AS avg_review_score,
        ROUND(SUM(revenue), 2)                                  AS total_revenue
    FROM sales
    GROUP BY is_late
"""
results["Late Delivery Impact"] = pd.read_sql_query(query_4, conn)
print("\n--- Query 4: Late Delivery Impact ---")
print(results["Late Delivery Impact"].to_string(index=False))

# ── QUERY 5: Best Day of Week for Orders ─────────────────────
# Which day drives the most orders and revenue?

query_5 = """
    SELECT
        day_of_week,
        COUNT(DISTINCT order_id)    AS total_orders,
        ROUND(SUM(revenue), 2)      AS total_revenue,
        ROUND(AVG(revenue), 2)      AS avg_order_value
    FROM sales
    GROUP BY day_of_week
    ORDER BY total_revenue DESC
"""
results["Day of Week"] = pd.read_sql_query(query_5, conn)
print("\n--- Query 5: Performance by Day of Week ---")
print(results["Day of Week"].to_string(index=False))

# ── EXPORT ALL RESULTS TO EXCEL ───────────────────────────────
# Each query goes into its own sheet
with pd.ExcelWriter("sql_results.xlsx") as writer:
    for sheet_name, df in results.items():
        df.to_excel(writer, sheet_name=sheet_name[:30], index=False)

conn.close()
print("\nAll results saved to sql_results.xlsx")