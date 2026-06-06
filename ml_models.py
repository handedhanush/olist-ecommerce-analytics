import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")   # must come before importing pyplot — saves charts without opening a window
import matplotlib.pyplot as plt

from sklearn.ensemble        import RandomForestClassifier
from sklearn.linear_model    import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics         import (accuracy_score, classification_report,
                                      mean_absolute_error, r2_score)

# Load the cleaned data
df = pd.read_csv("transformed_data.csv")
df["order_purchase_timestamp"] = pd.to_datetime(df["order_purchase_timestamp"])

# ══════════════════════════════════════════════════════════════
# MODEL 1 — LATE DELIVERY PREDICTOR
# Type: Classification (the answer is yes or no — will this order be late?)
# Algorithm: Random Forest (100 decision trees voting together)
# ══════════════════════════════════════════════════════════════

print("=" * 55)
print("MODEL 1: LATE DELIVERY PREDICTOR (Classification)")
print("=" * 55)

# Pick the input columns (called features) and the output column (called target)
# Features = what we know before delivery happens
# Target   = what we are trying to predict

model1_data = df[["revenue", "review_score", "month", "quarter", "is_late"]].dropna()

X1 = model1_data[["revenue", "review_score", "month", "quarter"]]  # inputs
y1 = model1_data["is_late"]                                         # what to predict

# Split data: 80% for training (model learns from this)
#             20% for testing  (we check predictions on data the model has never seen)
X1_train, X1_test, y1_train, y1_test = train_test_split(
    X1, y1, test_size=0.2, random_state=42
)

print(f"\nTraining on {len(X1_train):,} orders, testing on {len(X1_test):,} orders")

# Random Forest = 100 decision trees each making a prediction
# Final answer = whichever answer the majority of trees voted for
# More accurate and stable than a single decision tree
rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
rf_model.fit(X1_train, y1_train)

y1_pred  = rf_model.predict(X1_test)
accuracy = accuracy_score(y1_test, y1_pred)

print(f"\nAccuracy: {accuracy * 100:.1f}%")
print("\nDetailed breakdown (precision, recall, F1 score):")
print(classification_report(y1_test, y1_pred, target_names=["On Time", "Late"]))

# Feature importance: which input column mattered most for the prediction?
# Higher score = more important for the model's decision
feature_importance = pd.DataFrame({
    "Feature"   : X1.columns,
    "Importance": rf_model.feature_importances_
}).sort_values("Importance", ascending=False)

print("Which factors predict late delivery the most?")
print(feature_importance.to_string(index=False))

# ══════════════════════════════════════════════════════════════
# MODEL 2 — MONTHLY REVENUE FORECASTER
# Type: Regression (the answer is a number — what will revenue be?)
# Algorithm: Linear Regression (finds the best straight line through the data)
# ══════════════════════════════════════════════════════════════

print("\n" + "=" * 55)
print("MODEL 2: MONTHLY REVENUE FORECASTER (Regression)")
print("=" * 55)

# Group all orders by month and add up revenue for that month
monthly = (
    df.groupby(["year", "month"])["revenue"]
    .sum()
    .reset_index()
    .sort_values(["year", "month"])
    .reset_index(drop=True)
)

# Give each month a simple number: 1, 2, 3, 4...
# The model learns: as month number goes up, revenue goes up by X amount
monthly["month_number"] = range(1, len(monthly) + 1)

print(f"\nTotal months of data available: {len(monthly)}")

# 80/20 split again
split    = int(len(monthly) * 0.8)
train    = monthly[:split]
test     = monthly[split:]

X2_train = train[["month_number"]]
y2_train = train["revenue"]
X2_test  = test[["month_number"]]
y2_test  = test["revenue"]

# Linear Regression finds the best straight line through the training data
# Then uses that line to predict future months
lr_model = LinearRegression()
lr_model.fit(X2_train, y2_train)

y2_pred = lr_model.predict(X2_test)
mae     = mean_absolute_error(y2_test, y2_pred)
r2      = r2_score(y2_test, y2_pred)

print(f"\nModel Performance:")
print(f"  Mean Absolute Error (MAE) : R${mae:>12,.0f}")
print(f"  (on average predictions are off by this amount)")
print(f"\n  R2 Score : {r2:.2f}")
print(f"  (1.0 = perfect predictions, 0.0 = useless — higher is better)")

# Predict the next 3 months
last_month    = monthly["month_number"].max()
future_months = pd.DataFrame({"month_number": [last_month+1, last_month+2, last_month+3]})
future_preds  = lr_model.predict(future_months)

print(f"\nRevenue Forecast — Next 3 Months:")
for i, pred in enumerate(future_preds, 1):
    print(f"  Month {last_month + i}: R${pred:,.0f}")

# ── SAVE BOTH CHARTS IN ONE IMAGE ────────────────────────────
fig, axes = plt.subplots(1, 2, figsize=(15, 6))

# Left chart: Revenue forecast — actual vs predicted vs future
axes[0].plot(monthly["month_number"], monthly["revenue"],
             label="Actual Revenue", color="steelblue",
             marker="o", markersize=4, linewidth=2)
axes[0].plot(test["month_number"], y2_pred,
             label="Predicted (Test Period)", color="orange",
             linestyle="--", marker="x", markersize=6)
axes[0].plot(future_months["month_number"], future_preds,
             label="Future Forecast", color="green",
             linestyle="--", marker="^", markersize=8)
axes[0].set_title("Monthly Revenue — Actual vs Predicted vs Forecast")
axes[0].set_xlabel("Month Number")
axes[0].set_ylabel("Revenue (R$)")
axes[0].legend()
axes[0].grid(True, alpha=0.3)

# Right chart: Feature importance for late delivery model
axes[1].barh(
    feature_importance["Feature"],
    feature_importance["Importance"],
    color="tomato", edgecolor="white"
)
axes[1].invert_yaxis()  # most important at the top
axes[1].set_title("Late Delivery Predictor — Feature Importance")
axes[1].set_xlabel("Importance Score")
axes[1].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig("ml_charts.png", dpi=150)
plt.close()

print("\nCharts saved as ml_charts.png")
print("\nBoth ML models complete!")
print(f"\nNumbers for your resume:")
print(f"  Random Forest accuracy : {accuracy*100:.1f}%")
print(f"  Linear Regression R2   : {r2:.2f}")