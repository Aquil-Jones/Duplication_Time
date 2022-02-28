# Inquirer Data Engineering Candidate Exercise
In this exercise, you'll edit the `__main__.py` file to write some queries and tests against a database with historical COVID-19 case data. 

## Execution and Requirements
You can run the exercise with the following command:
```shell
python __main__.py
```

The execise does not require any external dependencies, and should run on Python
3.6 or greater.

## Contents
This exercise contains two files: 
### `__main__.py`
You will be editing two functions in `__main__.py`:
- `get_cases_7day_rolling_avg`
- `test_data_freshness`

See the docstrings under these two functions for more detailed instructions.

### `database_loader.py`
The main function in this module is named `load_database`, which performs the
following steps:
1. Creates a sqlite database, and a table named `covid_cases` in that database.
2. Loads the table `covid_cases` with U.S. state-level data on COVID-19 cases from the [New York Times](https://github.com/nytimes/covid-19-data).
3. Performs a data validation check against the data in `covid_cases`

## Data Dictionary
### `covid_cases` 
- `date` (text): The reported date for the data (in `YYYY-MM-DD` format).
- `state` (text): The name of the U.S. state, district, or territory.
- `cases` (integer): The number of new cases of Covid-19 reported that day, including both confirmed and probable.
- `deaths` (integer): The total number of new deaths from Covid-19 reported that day, including both confirmed and probable.

Note that, due to sqlite limitations, the columne `date` has data type `text`; however,
the data validation step checks that `date` only contains properly-formatted values.

## Change notes and thought process
### `database_loader.py`
* I made additions to this module on lines 46 and 78 respectively to commit the changes being made. I made this change so I could persist the full database past the point of the `__main__.py` running. Thus allowing me to debug my quieries in a different databse tool. It considered making another parameter to toggle databse cleanup or not. But the goal of this was not feature implementation else I might just keep making changes and we would end up with a whole datbase tool in and off itself.
### `__main__.py`
* The first change I made to this module, beyond implmenting the requisite functions, was to move the printing of the database elements inside of the functions themselves. This was simply because in sqlite3 you can print all the rows or just one, but simply printing will only tell you the object type. To avoid confusion instead of fetching the columns and returning them to be printed it seemed clearer to just print them there. I could also have persisted them to the database itself  or used the csv package but that would compromise the easy cleanup that the exercise seemed to favor thus neccessitating other changes.
#### `get_cases_7day_rolling_avg_ny_times` and `get_cases_7day_rolling_avg`
* The exercise only called for one version of this function after looking at the original ny times dataset I believe the version with thioer name is what you are looking for, but I will argue my version is better. While they both give the same values for the vast majority of the dataset my version will differ for the first 6 days of data. This difference is due to the fact that the new york times always divides the values of thier cases by 7 while my implementation will only divide by the current size of the window. I believe my version is to be preffered because it only works on data that we know we have. To this day there is still some debate as to the accuracy of the covid number especially in the early days of this (_accursed!_) pandemic. The new york times method essentially says there are zero cases in the days leading up to monitoring but the epidemiology of that suppossition is questionable. Another advantage of my method is that it will lead to slightly more accurate smoothing function when graphed and will scale better with larger windows.

#### `test_data_freshness`
* I actually went through about five different versions of this before getting to the version I am submitting. Eventually I decide on the current approach as it keeps the SQL somewhat simple and focused on extracting data and allows python to evaluate logic. While I did have to add an import of the datetime library datetime is in the Python standard library so I do not think there is any hit to portability. Besides that I have two conditions on the assert these are to account for possible variations in when this script can be run versus when the dataset is updated.

Thank you for your time and please let me know if there is any feedback ~ Aquil Jones(aquil.codes@gmail.com)