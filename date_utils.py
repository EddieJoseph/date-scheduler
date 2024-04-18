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