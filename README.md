# Olist E-Commerce Analytics & Forecasting Pipeline

## Overview
End-to-end data analytics project on 100,000+ real Brazilian e-commerce orders.

## Tech Stack
Python | pandas | SQLite | scikit-learn | matplotlib | seaborn | Power BI

## Project Structure
| File | What it does |
|---|---|
| etl_extract.py | Extract: load all 9 raw CSV files |
| etl_transform.py | Transform: join tables, clean data, engineer features |
| eda.ipynb | Exploratory Data Analysis with 15+ charts |
| etl_load.py | Load: store clean data in SQLite database |
| sql_analysis.py | SQL: 5 business queries with joins and aggregations |
| ml_models.py | ML: late delivery predictor + revenue forecaster |

## ETL Pipeline
1. Extracted 9 raw CSV files covering 100,000+ orders, customers, products, payments, and reviews
2. Joined all tables using pandas merge — equivalent to SQL JOINs across 9 tables
3. Cleaned nulls, fixed date columns, and engineered new features: delivery_days, is_late, revenue, quarter, day_of_week
4. Loaded clean data into SQLite database for SQL analysis

## Exploratory Data Analysis
15+ charts covering revenue distribution, monthly trends, top categories,
delivery time analysis, late vs on-time comparison, review score impact,
day-of-week patterns, state-level breakdown, and quarterly performance.

## SQL Analysis
5 business queries: monthly revenue trend, top 10 categories, state-level revenue,
late delivery impact on reviews, day-of-week order performance.

## Machine Learning

**Model 1 — Late Delivery Predictor (Random Forest Classifier)**
Predicts whether an order will be delivered late based on revenue, review score, month, and quarter.
Accuracy: XX%

**Model 2 — Monthly Revenue Forecaster (Linear Regression)**
Forecasts monthly revenue for the next 3 months based on historical trend.
R2 Score: 0.XX

## Power BI Dashboard
Interactive dashboard with 4 KPI cards, line chart, bar chart, map, donut chart,
ML forecast chart, and dynamic slicers for Year, Quarter, and Category.

## Key Findings
- 7.9% of orders were delivered late
- Late deliveries received 2.55 average review score vs 4.21 for on-time orders
- Top revenue category: bed_bath_table
- Busiest ordering day: Monday
