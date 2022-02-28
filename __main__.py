"""For the exercise, you will edit two functions in this file. See the function docstrings
under 'get_cases_7day_rolling_avg' and 'test_data_freshness' for more detailed instructions.
"""
import datetime as dt
import database_loader


def main():
    """Main entry point for the script"""
    cxn = database_loader.get_db_connection()
    database_loader.load_database(cxn)
    get_cases_7day_rolling_avg(cxn)
    get_cases_7day_rolling_avg_ny_times(cxn)
    test_data_freshness(cxn)


def get_cases_7day_rolling_avg(db_connection):
    """Write a query that returns, the average number of new cases reported 
       over the previous seven days of data for each day and state. In other 
       words, the seven-day trailing average.

    Parameters:
    - db_connection: a sqlite database connection
    """
    #Rounding to match original dataset though this may slightly hurt smoothness but is still accurate numerially
    executing_now = db_connection.cursor()
    executing_now.execute('''SELECT *,
                ROUND(AVG(cases) OVER(PARTITION BY state ORDER BY "date" ROWS 6 PRECEDING),2) as MOVING_AVERAGE 
                FROM covid_cases''')
    print(executing_now.fetchall())

def  get_cases_7day_rolling_avg_ny_times(db_connection):
    """An alternative version of the 7day rolling average function that exactly mimics the
        results of the NY times dataset with rounding. Please see the README for the reasoning
        on this alternative implementation.

    Parameters:
    - db_connection: a sqlite database connection
    """
    executing_now = db_connection.cursor()
    executing_now.execute('''SELECT *,
                ROUND(SUM(cases) OVER(PARTITION BY state ORDER BY "date" ROWS 6 PRECEDING)/7.0, 2) as MOVING_AVERAGE 
                FROM covid_cases''')
    print(executing_now.fetchall())


def test_data_freshness(db_connection):
    """On any given day we expect that yesterday's data should be available.
       Write a test that asserts that yesterday's data is available in the
       covid_cases table.

    Parameters:
    - db_connection: a sqlite database connection
    """
    delta = dt.timedelta(days=1)
    yesterday= dt.date.today() - delta
    #SQL 
    executing_now=db_connection.cursor()
    executing_now.execute('''SELECT MAX  (date)
                FROM covid_cases;''')
    date_val=executing_now.fetchone()[0]
    date_converted = dt.datetime.strptime(date_val,"%Y-%m-%d").date()
    time_dif = yesterday - date_converted
    assert time_dif.days == 0 or time_dif.days == 1, "Data is stale!" #The first case checks if the max date is yesterday. The second checks if the max date is today assuming continuity to imply the presence of yesterday's data.
    print("Certified Fresh!!")



if __name__ == "__main__":
    main()
