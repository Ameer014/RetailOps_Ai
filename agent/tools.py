import pandas as pd
import duckdb

from langchain_core.tools import tool

from database.db import execute_query


@tool
def get_dataset_information():
    """
    Get information about the uploaded dataset,
    including available columns and sample records.
    """

    return execute_query("""
        SELECT * FROM sales LIMIT 5
    """).to_json(orient="records")


@tool
def execute_sql(query: str):
    """
    Execute a read-only SQL query on the sales table.

    Only SELECT queries are allowed.
    """

    cleaned_query = query.strip()

    if not cleaned_query.lower().startswith("select"):
        return "Only SELECT queries are allowed."

    forbidden = [
        "drop", "delete", "update",
        "insert", "alter", "attach",
        "copy", "install", "load"
    ]

    query_lower = cleaned_query.lower()

    if any(word in query_lower.split() for word in forbidden):
        return "Query contains a restricted SQL operation."

    try:
        result = execute_query(cleaned_query)

        return result.to_json(orient="records")

    except Exception as e:
        return f"SQL execution error: {str(e)}"


@tool
def get_revenue_summary():
    """
    Calculate total revenue using the price column.
    """

    try:

        result = execute_query("""
            SELECT
                SUM(price) AS total_revenue,
                AVG(price) AS average_order_item_value,
                COUNT(*) AS total_records
            FROM sales
        """)

        return result.to_json(orient="records")

    except Exception as e:

        return str(e)