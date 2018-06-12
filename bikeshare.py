import time
import pandas as pd
import os.path
import numpy as np

ALL_MONTHS_OPTION = 0
ALL_DAYS_OPTION = 0


def seconds_formatter(seconds):
    """ Converts seconds to a formatted string
    Args:
        (int) seconds:
    Returns:
         (string) formatted string
    """
    seconds = abs(int(seconds))
    days, seconds = divmod(seconds, 86400)
    hours, seconds = divmod(seconds, 3600)
    minutes, seconds = divmod(seconds, 60)

    if days > 0:
        return '%dd %dh %dm %ds' % (days, hours, minutes, seconds)

    if hours > 0:
        return '%dh %dm %ds' % (hours, minutes, seconds)

    if minutes > 0:
        return '%dm %ds' % (minutes, seconds)

    return '%ds' % seconds


def float_formatter(number):
    """ Format a float number to a string """

    return '{0:,.3f}'.format(number)


def int_formatter(number):
    """ Format an int number as a string"""

    return '{0:,}'.format(number)


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


def cities_to_str():
    """ Returns the cities dictionary as a string. """

    message = []
    for code, name in cities().items():
        message.append('{} = {}'.format(code, name))

    return ', '.join(message)


def months_to_str():
    """ Returns the months list as a string. """

    message = []
    for i, name in enumerate(months()):
        message.append('{} = {}'.format(i, name))

    return ', '.join(message)


def days_to_str():
    """ Returns the days list as a string. """

    message = []
    for i, name in enumerate(days_of_week()):
        message.append('{} = {}'.format(i, name))

    return ', '.join(message)


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city_code = input('\nChose a city from the list\n{}\nYour choice: '.format(cities_to_str())).strip()
        try:
            city = city_name(city_code)
            break
        except ValueError:
            pass

    # get user input for month (all, january, february, ... , june)
    while True:
        month_number = int(input('\nChoose a month from the list\n{}\nYour choice: '.format(months_to_str())).strip())
        try:
            month = month_name(month_number)
            break
        except ValueError:
            pass

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day_of_week = int(
            input('\nChoose a day of week from the list\n{}\nYour choice: '.format(days_to_str())).strip()
        )
        try:
            day = day_name(day_of_week)
            break
        except ValueError:
            pass

    print('-' * 40)

    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """

    file = '{}.csv'.format(city.lower().replace(' ', '_'))
    if not os.path.isfile(file):
        return None

    df = pd.read_csv(file)

    df['Start Time'] = pd.to_datetime(df['Start Time'])

    df['Month'] = df['Start Time'].dt.month

    if month != months()[ALL_MONTHS_OPTION]:
        month = month_by_name(month)
        df = df[df['Month'] == month]

    guard_against_empty_data_frame(df)

    df['Day of Week'] = df['Start Time'].dt.weekday_name

    if day != days_of_week()[ALL_DAYS_OPTION]:
        df = df[df['Day of Week'] == day]

    guard_against_empty_data_frame(df)

    return df


def guard_against_empty_data_frame(df):
    """ Throws an exception if the DataFrame is empty.

    Args:
        (DataFrame) df: DataFrame to be checked
    Raises:
        ValueError: if the DataFrame is empty
    """

    if df.empty:
        raise ValueError('DataFrame is empty')


def time_stats(df):
    """Displays statistics on the most frequent times of travel.

    Args:
        (DataFrame) df: bikeshare DataFrame
    """

    guard_against_empty_data_frame(df)

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    most_common_month = month_name(df['Month'].mode()[0])
    print(' * Most common month: {}'.format(most_common_month))

    # display the most common day of week
    print(' * Most common day of week: {}'.format(df['Day of Week'].mode()[0]))

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    print(' * Most common start hour: {}'.format(df['hour'].mode()[0]))

    print("\nThis took %s seconds." % (float_formatter(time.time() - start_time)))
    print('-' * 40)


def station_stats(df):
    """
    Displays statistics on the most popular stations and trip.

    Args:
        (DataFrame) df: bikeshare DataFrame
    """

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print(' * Most commonly used start station: {}'.format(df['Start Station'].mode()[0]))

    # display most commonly used end station
    print(' * Most commonly used end station: {}'.format(df['End Station'].mode()[0]))

    # display most frequent combination of start station and end station trip
    df['StartEnd Stations'] = df['Start Station'] + ' -> ' + df['End Station']
    print(' * Most frequent combination of start station and end station trip: {}'.format(
        df['StartEnd Stations'].mode()[0]))

    print("\nThis took %s seconds." % (float_formatter(time.time() - start_time)))
    print('-' * 40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration.

    Args:
        (DataFrame) df: bikeshare DataFrame
    """

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print(' * Total trips duration: {}'.format(seconds_formatter(df['Trip Duration'].sum())))

    # display mean travel time
    print(' * Average trip duration: {}'.format(seconds_formatter(df['Trip Duration'].mean())))

    print("\nThis took %s seconds." % (float_formatter(time.time() - start_time)))
    print('-' * 40)


def user_stats(df):
    """Displays statistics on bikeshare users.

    Args:
        (DataFrame) df: bikeshare DataFrame
    """

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print('Number of users by type:')
    try:
        users_by_type = df.groupby('User Type').size()
        for gender, count in users_by_type.items():
            print(' * {}: {}'.format(gender, int_formatter(count)))
    except KeyError:
        print(' * No user type data available')

    # Display counts of gender
    print('\nNumber of users by gender:')
    try:
        users_by_gender = df.groupby('Gender').size()
        for gender, count in users_by_gender.items():
            print(' * {}: {}'.format(gender, int_formatter(count)))
    except KeyError:
        print(' * No gender data available')

    # Display earliest, most recent, and most common year of birth
    print('\nYear of birth stats:')
    try:
        print(' * Earliest: {}'.format(df['Birth Year'].min().astype(int)))
        print(' * Most recent: {}'.format(df['Birth Year'].max().astype(int)))
        print(' * Most common: {}'.format(df['Birth Year'].mode()[0].astype(int)))
    except KeyError:
        print('No year of birth data available')

    print("\nThis took %s seconds." % (float_formatter(time.time() - start_time)))
    print('-' * 40)


def main():
    while True:
        city, month, day = get_filters()

        df = load_data(city, month, day)
        if df is None:
            print('\nDataset does not exists\n')
            break

        action = int(input('\nWhat would you like to do?\n'
                           '[0] View stats\n'
                           '[1] View the first 50 rows of data\n'
                           'Your choice: ').strip())
        try:
            print('\nResults')
            print('-' * 40)
            print('City: {}\nMonth: {}\nDay of Week: {}'.format(city.title(), month, day))
            print('-' * 40)

            if action == 0:
                time_stats(df)
                station_stats(df)
                trip_duration_stats(df)
                user_stats(df)
            elif action == 1:
                print(df.head(50))

        except ValueError:
            print('\nThere is no data for your filter combination, try another one')
            print('-' * 40)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
