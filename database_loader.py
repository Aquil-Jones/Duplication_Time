import sqlite3
import logging
import os
import urllib.request

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

DATA_SOURCE_URL = "https://raw.githubusercontent.com/nytimes/covid-19-data/master/rolling-averages/us-states.csv"

DATABASE_NAME = "covid.db"
TABLE_NAME = "covid_cases"

# Start with a new sqlite database each time
try:
    os.remove(DATABASE_NAME)
except FileNotFoundError:
    pass


def get_db_connection():
    return sqlite3.connect(DATABASE_NAME)


def load_database(cxn):
    logger.debug(f"Initializing database {DATABASE_NAME}")
    create_table(cxn)
    load_table(cxn)
    test_date_column_contains_valid_values(cxn)

    logger.debug(f"Database {DATABASE_NAME} successfully initialized")



def create_table(cxn):
    """Creates a sqlite table

    Parameters:
    - cxn: a sqlite database connection
    """
    logging.debug(f"Creating table {TABLE_NAME}")
    curs = cxn.cursor()
    curs.execute(
        f"create table {TABLE_NAME} (date text, state text, cases integer, deaths integer)"
    )
    cxn.commit()


def load_table(cxn):
    """Loads a table from a url response payload. The payload
       is expected to be in csv format.

    Parameters:
    - cxn: a sqlite database connection
    """
    logging.debug(f"Loading table {TABLE_NAME}")

    with urllib.request.urlopen(DATA_SOURCE_URL) as response:
        r = response.read()
    lines = r.decode().split("\n")
    to_db = []
    for idx, line in enumerate(lines):
        # don't load the header column
        if idx == 0:
            continue
        columns = line.split(",")
        date = columns[0]
        state = columns[2]
        cases = columns[3]
        deaths = columns[6]
        to_db.append((date, state, cases, deaths,))

    #print(to_db)
    curs = cxn.cursor()
    curs.executemany(
        f"INSERT INTO {TABLE_NAME} (date, state, cases, deaths) VALUES (?, ?, ?, ?);", to_db
    )
    cxn.commit()


def test_date_column_contains_valid_values(cxn):
    """This validation step checks to see if there are
       any improperly-formatted date values in the date column.

    Parameters:
    - cxn: a sqlite database connection
    """
    logging.debug("Performing data validation check.")

    expected_row_count = 0
    curs = cxn.cursor()
    try:
        row_count = curs.execute(
            f"SELECT count(*) FROM {TABLE_NAME} where date not like '____-__-__'",
        ).fetchone()[0]
        assert row_count == expected_row_count


    except AssertionError:
        logging.error(
            (
                f"Database setup failed! Expected row count: {expected_row_count}, "
                f"actual row count: {row_count}"
            )
        )
        raise
