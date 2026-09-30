"""Query the MySQL 'mock' table: filter by group and count rows per column value."""

import logging
import os

import mysql.connector

# Set up logging so each function reports what it's doing
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)

# Database credentials come from environment variables, never hardcoded
DBHOST = os.environ.get("DBHOST")
DBUSER = os.environ.get("DBUSER")
DBPASS = os.environ.get("DBPASS")
DBNAME = os.environ.get("DBNAME")

# Connect once at the top, same as basic-sql.py
db = mysql.connector.connect(host=DBHOST, user=DBUSER, password=DBPASS, database=DBNAME)
cur = db.cursor()

# Columns plot_counts is allowed to group by (see note in plot_counts)
ALLOWED_COLUMNS = ["id", "group", "email", "first_name", "age", "signup_date"]


def get_data_by_group(value):
    """Return all rows from mock where the `group` column equals value (list of tuples)."""
    logger.info("Getting rows where group = %s", value)
    # `group` needs backticks because GROUP is a reserved word in MySQL
    query = "SELECT * FROM mock WHERE `group` = %s;"
    try:
        # Pass the value as a tuple so it's safely parameterized
        cur.execute(query, (value,))
        results = cur.fetchall()
        logger.info("Found %d rows", len(results))
        return results
    except mysql.connector.Error as e:
        logger.error("MySQL Error: %s", e)
        return None


def plot_counts(groupby):
    """Count rows per distinct value of the groupby column and return the counts."""
    logger.info("Counting rows grouped by %s", groupby)
    # Column names can't use %s placeholders (those only work for values),
    # so only accept names from our known list to keep the query safe
    if groupby not in ALLOWED_COLUMNS:
        logger.error("Unknown column: %s", groupby)
        return None
    query = f"SELECT `{groupby}`, COUNT(*) FROM mock GROUP BY `{groupby}`;"
    try:
        cur.execute(query)
        results = cur.fetchall()
        logger.info("Found %d distinct values", len(results))
        return results
    except mysql.connector.Error as e:
        logger.error("MySQL Error: %s", e)
        return None


def main():
    """Run the demo queries and close the database connection."""
    print("=== rows in group Red ===")
    for row in get_data_by_group("Red"):
        print(row)

    print("=== counts by group ===")
    for row in plot_counts("group"):
        print(row)

    # Close the connection when finished
    cur.close()
    db.close()


if __name__ == "__main__":
    main()