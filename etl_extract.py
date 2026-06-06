import pandas as pd

print("=" * 55)
print("EXTRACTING DATA — Loading all CSV files")
print("=" * 55)

# ── LOAD ALL 9 FILES ─────────────────────────────────────────
# Think of each CSV like one sheet in a big Excel workbook
# They are all connected through common ID columns like order_id

orders       = pd.read_csv("olist_orders_dataset.csv")
order_items  = pd.read_csv("olist_order_items_dataset.csv")
products     = pd.read_csv("olist_products_dataset.csv")
customers    = pd.read_csv("olist_customers_dataset.csv")
payments     = pd.read_csv("olist_order_payments_dataset.csv")
reviews      = pd.read_csv("olist_order_reviews_dataset.csv")
sellers      = pd.read_csv("olist_sellers_dataset.csv")
translations = pd.read_csv("product_category_name_translation.csv")

# ── PRINT A SUMMARY OF EACH FILE ─────────────────────────────
# .shape tells you (how many rows, how many columns)

all_files = {
    "orders"      : orders,
    "order_items" : order_items,
    "products"    : products,
    "customers"   : customers,
    "payments"    : payments,
    "reviews"     : reviews,
    "sellers"     : sellers,
    "translations": translations,
}

print(f"\n{'File':<20} {'Rows':>10} {'Columns':>10}")
print("-" * 42)
for name, df in all_files.items():
    print(f"{name:<20} {df.shape[0]:>10,} {df.shape[1]:>10}")

# ── PEEK AT THE MAIN TABLE ────────────────────────────────────
# .head() shows the first 5 rows — like scrolling to the top of an Excel sheet
print("\nFirst 3 rows of the orders table:")
print(orders.head(3).to_string())

print("\nExtract complete!")