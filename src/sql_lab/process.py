"""Read MOCK_DATA.csv, clean it, and load it into the MySQL 'mock' table."""

import logging
import os

import mysql.connector
import pandas as pd

# Set up logging so each step reports what it's doing
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)

# Database credentials come from environment variables, never hardcoded
DBHOST = os.environ.get("DBHOST")
DBUSER = os.environ.get("DBUSER")
DBPASS = os.environ.get("DBPASS")
DBNAME = os.environ.get("DBNAME")

# Map pandas dtypes to MySQL column types (from Step 3)
TYPE_MAPPING = {
    "int64": "BIGINT",
    "int32": "INT",
    "float64": "DOUBLE",
    "bool": "TINYINT(1)",
    "datetime64[ns]": "DATETIME",
    "object": "VARCHAR(255)",
    "string": "VARCHAR(255)",
    "str": "VARCHAR(255)",  # pandas 3.0 labels text columns as "str"
}


def read_data(filename):
    """Load a CSV file into a pandas DataFrame and return it."""
    logger.info("Reading data from %s", filename)
    data = pd.read_csv(filename)
    logger.info("Read %d rows and %d columns", len(data), len(data.columns))
    return data


def clean_data(data):
    """Remove rows with missing values and return the cleaned DataFrame."""
    logger.info("Cleaning data (%d rows before)", len(data))
    # Remove any row that has a blank in any column
    data = data.dropna()
    logger.info("Cleaned data has %d rows", len(data))
    return data


def load_data(data, table):
    """Create the table if it doesn't exist and insert each row of the DataFrame."""
    logger.info("Loading %d rows into table %s", len(data), table)

    # Column types chosen with TYPE_MAPPING from Step 3.
    # `group` needs backticks because GROUP is a reserved word in MySQL.
    create_table = """
        CREATE TABLE IF NOT EXISTS mock (
            id          BIGINT,
            `group`     VARCHAR(255),
            email       VARCHAR(255),
            first_name  VARCHAR(255),
            age         BIGINT,
            signup_date DATE
        )
    """

    # Insert statement with parameterized values (same pattern as insert_data.py)
    add_record = "INSERT INTO mock (id, `group`, email, first_name, age, signup_date) VALUES (%s, %s, %s, %s, %s, %s)"

    try:
        # Connect to the database using the environment variables
        db = mysql.connector.connect(host=DBHOST, user=DBUSER, password=DBPASS, database=DBNAME)
        cursor = db.cursor()

        # Create the table, then empty it so rerunning doesn't add duplicates
        cursor.execute(create_table)
        cursor.execute("TRUNCATE TABLE mock")

        # Insert one row at a time
        for index, row in data.iterrows():
            record_data = (
                int(row["id"]),
                row["group"],
                row["email"],
                row["first_name"],
                int(row["age"]),
                row["signup_date"],
            )
            cursor.execute(add_record, record_data)

        # Save the changes and close the connection
        db.commit()
        cursor.close()
        db.close()
        logger.info("Successfully inserted %d rows into %s", len(data), table)
    except mysql.connector.Error as e:
        logger.error("MySQL Error: %s", e)


def main():
    """Read, clean, and load the mock data into MySQL."""
    data = read_data("MOCK_DATA.csv")
    data = clean_data(data)
    load_data(data, "mock")


if __name__ == "__main__":
    main()