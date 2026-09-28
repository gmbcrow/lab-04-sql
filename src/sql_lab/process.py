#!/usr/bin/env python3
"""
process.py

Reads MOCK_DATA.csv, cleans it, and uploads it to a MySQL table called
"mock" in the database named by the DBNAME environment variable.

Required environment variables:
    DBHOST, DBUSER, DBPASS, DBNAME

Usage:
    uv run python src/sql_lab/process.py
"""

import logging
import os

import mysql.connector
import pandas as pd

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

TYPE_MAPPING = {
    "int64": "BIGINT",
    "int32": "INT",
    "float64": "DOUBLE",
    "bool": "TINYINT(1)",
    "datetime64[ns]": "DATETIME",
    "object": "VARCHAR(255)",
    "string": "VARCHAR(255)",
}


def read_data(filename):
    """
    Load a CSV file into a pandas DataFrame.

    Args:
        filename (str): Path to the CSV file to read.

    Returns:
        pandas.DataFrame: The loaded data.
    """
    logger.info("Reading data from %s", filename)
    data = pd.read_csv(filename)
    logger.info("Loaded %d rows, %d columns", len(data), len(data.columns))
    return data


def clean_data(data):
    """
    Clean a DataFrame for upload by dropping rows with missing values.

    Args:
        data (pandas.DataFrame): The raw data to clean.

    Returns:
        pandas.DataFrame: The cleaned data, with a reset index.
    """
    before = len(data)
    cleaned = data.dropna().reset_index(drop=True)
    logger.info("Dropped %d rows with missing values (%d remaining)", before - len(cleaned), len(cleaned))
    return cleaned


def load_data(data, table):
    """
    Create a table (if it doesn't exist) and upload a DataFrame into it.

    Column types are inferred from the DataFrame's dtypes using
    TYPE_MAPPING. Column names are wrapped in backticks so reserved words
    (like "group") don't break the SQL. Rows are inserted using
    parameterized queries to avoid SQL injection.

    Args:
        data (pandas.DataFrame): The cleaned data to upload.
        table (str): The destination table name.
    """
    db = None
    try:
        db = mysql.connector.connect(
            host=os.environ["DBHOST"],
            user=os.environ["DBUSER"],
            password=os.environ["DBPASS"],
            database=os.environ["DBNAME"],
        )
        cur = db.cursor()

        columns_sql = []
        for col_name, dtype in data.dtypes.items():
            sql_type = TYPE_MAPPING.get(str(dtype), "VARCHAR(255)")
            columns_sql.append(f"`{col_name}` {sql_type}")

        create_stmt = f"CREATE TABLE IF NOT EXISTS `{table}` ({', '.join(columns_sql)})"
        logger.info("Creating table if not exists: %s", table)
        cur.execute(create_stmt)

        col_names = ", ".join(f"`{c}`" for c in data.columns)
        placeholders = ", ".join(["%s"] * len(data.columns))
        insert_stmt = f"INSERT INTO `{table}` ({col_names}) VALUES ({placeholders})"

        rows = [tuple(row) for row in data.itertuples(index=False, name=None)]
        cur.executemany(insert_stmt, rows)
        db.commit()
        logger.info("Inserted %d rows into %s", cur.rowcount, table)

    except mysql.connector.Error as e:
        logger.error("MySQL Error: %s", e)
    finally:
        if db is not None and db.is_connected():
            cur.close()
            db.close()
            logger.info("Database connection closed")


def main():
    """Run the full read -> clean -> load pipeline."""
    data = read_data("MOCK_DATA.csv")
    cleaned = clean_data(data)
    load_data(cleaned, "mock")


if __name__ == "__main__":
    main()
