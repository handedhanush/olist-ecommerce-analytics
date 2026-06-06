import pandas as pd
import numpy as np

print("=" * 55)
print("TRANSFORMING DATA — Cleaning and joining tables")
print("=" * 55)

# ── LOAD ALL FILES ────────────────────────────────────────────
orders       = pd.read_csv("olist_orders_dataset.csv")
order_items  = pd.read_csv("olist_order_items_dataset.csv")
products     = pd.read_csv("olist_products_dataset.csv")
customers    = pd.read_csv("olist_customers_dataset.csv")
payments     = pd.read_csv("olist_order_payments_dataset.csv")
reviews      = pd.read_csv("olist_order_reviews_dataset.csv")
translations = pd.read_csv("product_category_name_translation.csv")

print(f"Starting with {len(orders):,} orders")

# ── STEP 1: JOIN TABLES TOGETHER ─────────────────────────────
# .merge() is like VLOOKUP — it matches rows across two tables
# using a shared column like order_id or product_id

# Add English category names to the products table
products = products.merge(translations, on="product_category_name", how="left")

# Attach customer info to orders (to get customer state)
df = orders.merge(customers, on="customer_id", how="left")

# Attach order items (to get product_id and price per item)
df = df.merge(order_items, on="order_id", how="left")

# Attach English product category
df = df.merge(
    products[["product_id", "product_category_name_english"]],
    on="product_id", how="left"
)

# One order can have multiple payment rows — add them up per order
payment_totals = payments.groupby("order_id")["payment_value"].sum().reset_index()
df = df.merge(payment_totals, on="order_id", how="left")

# One order can have multiple reviews — take the average score per order
review_avg = reviews.groupby("order_id")["review_score"].mean().reset_index()
df = df.merge(review_avg, on="order_id", how="left")

print(f"After joining all tables: {len(df):,} rows")

# ── STEP 2: FIX DATE COLUMNS ─────────────────────────────────
# Right now dates are stored as plain text like "2017-10-02 10:56:33"
# We convert them into real date objects so Python can do math with them

date_columns = [
    "order_purchase_timestamp",
    "order_delivered_customer_date",
    "order_estimated_delivery_date"
]
for col in date_columns:
    # errors="coerce" means: if a value cant be converted, just make it blank
    df[col] = pd.to_datetime(df[col], errors="coerce")

# ── STEP 3: KEEP ONLY DELIVERED ORDERS ───────────────────────
# We only want orders that were actually delivered to the customer
# Cancelled or still-processing orders would mess up our analysis

df = df[df["order_status"] == "delivered"]
print(f"After keeping only delivered orders: {len(df):,} rows")

# ── STEP 4: REMOVE ROWS MISSING CRITICAL DATA ─────────────────
# We cannot analyse an order if we dont know when it was placed or what it cost
df = df.dropna(subset=["order_purchase_timestamp", "price"])
print(f"After removing rows with missing date or price: {len(df):,} rows")

# ── STEP 5: CREATE NEW USEFUL COLUMNS ────────────────────────
# Called "feature engineering" — we calculate new columns from existing ones
# This shows analytical thinking in interviews

# Break the purchase date into separate time parts
df["year"]        = df["order_purchase_timestamp"].dt.year
df["month"]       = df["order_purchase_timestamp"].dt.month
df["month_name"]  = df["order_purchase_timestamp"].dt.strftime("%b")  # Jan, Feb...
df["quarter"]     = df["order_purchase_timestamp"].dt.quarter          # 1, 2, 3 or 4
df["day_of_week"] = df["order_purchase_timestamp"].dt.day_name()       # Monday, Tuesday...

# How many days did the actual delivery take?
df["delivery_days"] = (
    df["order_delivered_customer_date"] - df["order_purchase_timestamp"]
).dt.days

# Was delivery late? 1 = yes it was late, 0 = arrived on time or early
df["is_late"] = (
    df["order_delivered_customer_date"] > df["order_estimated_delivery_date"]
).astype(int)

# Use payment value as revenue. Fall back to item price if payment is missing
df["revenue"] = df["payment_value"].fillna(df["price"])

# Clean up the category column
df["category"] = df["product_category_name_english"].fillna("Unknown")

# ── STEP 6: REMOVE UNREALISTIC DELIVERY TIMES ─────────────────
# Delivery in less than 1 day or more than 120 days is likely a data error
df = df[df["delivery_days"].between(1, 120)]
print(f"After removing unrealistic delivery times: {len(df):,} rows")

# ── STEP 7: KEEP ONLY THE COLUMNS WE NEED ────────────────────
# Drop everything we do not need — keeps the final dataset clean and readable

columns_to_keep = [
    "order_id", "customer_id", "customer_state",
    "order_purchase_timestamp", "year", "month", "month_name",
    "quarter", "day_of_week", "category", "price",
    "revenue", "delivery_days", "is_late", "review_score"
]
df = df[columns_to_keep].copy()

# ── FINAL CHECK ───────────────────────────────────────────────
print(f"\nFinal clean dataset: {len(df):,} rows, {len(df.columns)} columns")
print("\nColumn types:")
print(df.dtypes)
print("\nMissing values remaining:")
print(df.isnull().sum())

# Save to a new CSV file — this is what we use for all the next steps
df.to_csv("transformed_data.csv", index=False)
print("\nTransform complete! Saved as transformed_data.csv")