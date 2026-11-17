import duckdb
import pandas as pd

from config.settings import DATABASE_PATH


def get_connection():

    return duckdb.connect(DATABASE_PATH)


def save_dataframe(df, table_name="sales"):

    con = get_connection()

    con.register("uploaded_df", df)

    con.execute(f"""
        CREATE OR REPLACE TABLE {table_name} AS
        SELECT * FROM uploaded_df
    """)

    con.close()


def execute_query(query):

    con = get_connection()

    try:
        result = con.execute(query).fetchdf()
        return result

    finally:
        con.close()


def get_tables():

    con = get_connection()

    tables = con.execute("""
        SHOW TABLES
    """).fetchdf()

    con.close()

    return tables