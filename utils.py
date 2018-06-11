import os.path


def cities():
    """
    Returns a dictionary with names of cities and data files.

    Returns:
        dict: A dictionary whose keys are the city codes and the values are a dictionary with city names and
              data files
    """
    return {
        'CH': 'chicago',
        'NY': 'new york city',
        'WA': 'washington'
    }


def days_of_week():
    """Returns a week day list from 1 (Sunday) to 7 (Saturday). 0 = All

    Returns:
        list: Days of weeK
    """

    return ['All', 'Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']


def months():
    """
    Returns a months list. 0 = All

    Returns:
        list: A list with the name of months
    """

    return ['All', 'January', 'February', 'March', 'April', 'May', 'June',
            'July', 'August', 'September', 'October', 'November', 'December']


def month_by_name(month):
    """
    Returns the number of a given month name.

    Args:
        month (str): A month name
    Returns:
        Index of the month
    """

    return months().index(month)


def city_data_file_path(city):
    """Returns a city csv file path.

    Args:
        city (str): City name
    Returns:
        str: Path to the city data file
    Raises:
        ValueError: if city is not in the dictionary
    """

    if city.lower() not in cities().values():
        raise ValueError('{} is not in the list of cities'.format(city))

    file = '{}.csv'.format(city.lower().replace(' ', '_'))

    src_path = '.'

    return os.path.join(src_path, file)


def city_name(city_code):
    """
    Returns the city name from a two characters code.

    Args:
        city_code (str): two characters city code
    Returns:
        str: The city name
    """

    if city_code.upper() not in cities().keys():
        raise ValueError('City code does not exists')

    return cities()[city_code.upper()]


def day_name(day):
    """
    Returns the day of given the day number

    Args:
        day (int): The day number (0-7)
    Returns:
        str: Day of the week or 'all' if the day number is 0
    Raises:
        ValueError: if number is not between 0 and 7
    """

    day = int(day)

    if day < 0 or day > 7:
        raise ValueError('day must be between 0 and 7')

    return days_of_week()[day]


def month_name(month):
    """
    Returns the month name given the month number.

    Args:
        month (int): The month number (0-12)
    Returns:
        str: Month name or 'all' if the number is 0
    Raises:
        ValueError: if month is not between 0 and 12
    """

    if month < 0 or month > 12:
        raise ValueError('month must be between 0 and 12')

    return months()[month]
