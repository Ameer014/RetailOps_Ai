import pandas as pd


def calculate_sales_metrics(df):

    metrics = {}

    numeric_columns = df.select_dtypes(
        include="number"
    ).columns

    metrics["total_records"] = len(df)

    metrics["numeric_columns"] = list(numeric_columns)

    if "price" in df.columns:

        metrics["total_revenue"] = df["price"].sum()

        metrics["average_price"] = df["price"].mean()

    if "order_id" in df.columns:

        metrics["total_orders"] = df["order_id"].nunique()

    if "customer_id" in df.columns:

        metrics["total_customers"] = df["customer_id"].nunique()

    return metrics