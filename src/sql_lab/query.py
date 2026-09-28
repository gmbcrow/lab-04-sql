#!/usr/bin/env python3
"""
query.py

Queries the "mock" table in the database named by the DBNAME environment
variable. Modeled on basic-sql.py's get_people_by_lastname and
plot_continent_counts.

Required environment variables:
    DBHOST, DBUSER, DBPASS, DBNAME

Usage:
    uv run python src/sql_lab/query.py
"""

import logging
import os

import matplotlib.pyplot as plt
import mysql.connector
import pandas as pd

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

DBHOST = os.environ.get("DBHOST")
DBUSER = os.environ.get("DBUSER")
DBPASS = os.environ.get("DBPASS")
DBNAME = os.environ.get("DBNAME")

db = mysql.connector.connect(user=DBUSER, host=DBHOST, password=DBPASS, database=DBNAME)
cur = db.cursor()


def get_data_by_group(value):
    """
    Return all rows from "mock" whose `group` column equals value.

    "group" is a reserved word in MySQL, so the column is quoted with
    backticks. The filter value is passed as a parameter, not inserted
    into the SQL string, to avoid SQL injection.

    Args:
        value (str): The group value to filter on.

    Returns:
        list[tuple]: Matching rows, or None on error.
    """
    query = "SELECT * FROM mock WHERE `group` = %s;"
    try:
        cur.execute(query, (value,))
        results = cur.fetchall()
        logger.info("Fetched %d rows for group=%s", len(results), value)
        return results
    except mysql.connector.Error as e:
        logger.error("MySQL Error: %s", e)
        return None


def plot_counts(groupby):
    """
    Count rows per distinct value of a column in "mock" and show a bar chart.

    Args:
        groupby (str): The column name to group by (e.g. "group").

    Returns:
        pandas.DataFrame: The counts, or None on error.
    """
    query = f"SELECT `{groupby}`, COUNT(*) FROM mock GROUP BY `{groupby}`;"
    try:
        cur.execute(query)
        results = cur.fetchall()
        logger.info("Computed counts for %d distinct values of %s", len(results), groupby)
        df = pd.DataFrame(results)
        df.plot.bar(x=0, y=1)
        plt.tight_layout()
        plt.show()
        return df
    except mysql.connector.Error as e:
        logger.error("MySQL Error: %s", e)
        return None


def main():
    """Run the demo queries and close the database connection."""
    print("=== by group ===")
    print(get_data_by_group("a"))

    print("=== counts ===")
    plot_counts("group")

    cur.close()
    db.close()


if __name__ == "__main__":
    main()
