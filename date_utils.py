from datetime import datetime

import numpy as np


def convert_to_day_of_year(date,throw_errors=True):
    # Convert date to day of year
    try:
        return date.timetuple().tm_yday-1
    except:
        if throw_errors:
            raise ValueError('Invalid date format')
        else:
            return np.random.randint(1, 365)-1

def convert_to_date(day_of_year, year):
    # Convert day of year to date
    return convert_to_datetime(day_of_year, year).date()

def convert_to_datetime(day_of_year, year):
    # Convert day of year to datetime
    return datetime.strptime(str(year) +"-"+ str(day_of_year+1), '%Y-%j')

def get_week_days_of_year(year):
    # Get working days of year
    return np.array([i for i in range(365) if convert_to_datetime(i, year).weekday() < 5])

def get_saturdays_of_year(year):
    # Get saturdays of year
    return np.array([i for i in range(365) if convert_to_datetime(i, year).weekday() == 5])

def get_sundays_of_year(year):
    # Get sundays of year
    return np.array([i for i in range(365) if convert_to_datetime(i, year).weekday() == 6])

# This method will not work for leap years!
# however this should not be an issue because the goal is only to generate good suggestions
def get_month_from_day_of_year(day_of_year):
    # Get month from day of year
    if day_of_year < 31:
        return 1
    elif day_of_year < 59:
        return 2
    elif day_of_year < 90:
        return 3
    elif day_of_year < 120:
        return 4
    elif day_of_year < 151:
        return 5
    elif day_of_year < 181:
        return 6
    elif day_of_year < 212:
        return 7
    elif day_of_year < 243:
        return 8
    elif day_of_year < 273:
        return 9
    elif day_of_year < 304:
        return 10
    elif day_of_year < 334:
        return 11
    else:
        return 12

def get_weekday_name(weekday):
    # Get weekday name
    if weekday == 0:
        return 'Montag'
    if weekday == 1:
        return 'Dienstag'
    if weekday == 2:
        return 'Mittwoch'
    if weekday == 3:
        return 'Donnerstag'
    if weekday == 4:
        return 'Freitag'
    if weekday == 5:
        return 'Samstag'
    if weekday == 6:
        return 'Sonntag'
    raise Exception('Invalid')
