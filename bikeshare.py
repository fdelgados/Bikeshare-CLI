import time
import pandas as pd
import numpy as np

import utils as ut
import formatter as fmt
from stats_retriever import StatsRetriever
from stats import *


def print_cities():
    """ Prints the cities dictionary. """

    message = []
    for code, name in ut.cities().items():
        message.append('{} = {}'.format(code, name))

    return ', '.join(message)


def print_months():
    """ Prints the months list. """

    message = []
    for i, name in enumerate(ut.months()):
        message.append('{} = {}'.format(i, name))

    return ', '.join(message)


def print_days():
    """ Prints the days list. """

    message = []
    for i, name in enumerate(ut.days_of_week()):
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
        city_code = input('\nChose a city from the list\n{}\nYour choice: '.format(print_cities())).strip()
        try:
            city = ut.city_name(city_code)
            break
        except ValueError:
            pass

    # get user input for month (all, january, february, ... , june)
    while True:
        month_number = int(input('\nChoose a month from the list\n{}\nYour choice: '.format(print_months())).strip())
        try:
            month = ut.month_name(month_number)
            break
        except ValueError:
            pass

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day_of_week = int(input('\nChoose a day of week from the list\n{}\nYour choice: '.format(print_days())).strip())
        try:
            day = ut.day_name(day_of_week)
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
        StatsRetriever: StatsRetriever object with a Pandas DataFrame
            containing city data filtered by month and day
    """

    return StatsRetriever(city, month, day)

def time_stats(retriever):
    """Displays statistics on the most frequent times of travel.

    Args:
        retriever (StatsRetriever): StatsRetriever object with a DataFrame loaded
    """

    print('\nCalculating The Most Frequent Times of Travel...\n')
    time_stats = retriever.time_stats()

    # display the most common month
    print(' * Most common month: {}'.format(time_stats.most_common_month))

    # display the most common day of week
    print(' * Most common day of week: {}'.format(time_stats.most_common_day_of_week))

    # display the most common start hour
    print(' * Most common start hour: {}'.format(time_stats.most_common_start_hour))

    seconds = fmt.float_formatter(retriever.operation_time['time'])
    print("\nThis took {} seconds.".format(seconds))
    print('-' * 40)


def station_stats(retriever):
    """
    Displays statistics on the most popular stations and trip.

    Args:
        retriever (StatsRetriever): StatsRetriever object with a DataFrame loaded
    """

    print('\nCalculating The Most Popular Stations and Trip...\n')
    station_stats = retriever.station_stats()

    # display most commonly used start station
    print(' * Most commonly used start station: {}'.format(station_stats.most_common_start_station))

    # display most commonly used end station
    print(' * Most commonly used end station: {}'.format(station_stats.most_common_end_station))

    # display most frequent combination of start station and end station trip
    print(' * Most frequent combination of start station and end station trip: {}'.format(station_stats.most_common_start_end_stations))

    seconds = fmt.float_formatter(retriever.operation_time['station'])
    print("\nThis took {} seconds.".format(seconds))
    print('-' * 40)


def trip_duration_stats(retriever):
    """Displays statistics on the total and average trip duration.

    Args:
        retriever (StatsRetriever): StatsRetriever object with a DataFrame loaded
    """

    print('\nCalculating Trip Duration...\n')

    # display total travel time
    trip_stats = retriever.trip_duration_stats()
    print(' * Total trips duration: {}'.format(fmt.seconds_formatter(trip_stats.total_trips_duration)))

    # display mean travel time
    print(' * Average trip duration: {}'.format(fmt.seconds_formatter(trip_stats.avg_trip_duration)))

    seconds = fmt.float_formatter(retriever.operation_time['trip_duration'])
    print("\nThis took {} seconds.".format(seconds))
    print('-' * 40)


def user_stats(retriever):
    """Displays statistics on bikeshare users.

    Args:
        retriever (StatsRetriever): StatsRetriever object with a DataFrame loaded
    """

    print('\nCalculating User Stats...\n')

    user_stats = retriever.user_stats()

    # Display counts of user types
    print('Number of users by type:')
    users_by_type = user_stats.users_by_type
    if users_by_type is not None:
        for gender, count in users_by_type.items():
            print(' * {}: {}'.format(gender, fmt.int_formatter(count)))
    else:
        print('No user type data available')

    # Display counts of gender
    print('\nNumber of users by gender:')
    users_by_gender = user_stats.users_by_gender
    if users_by_gender is not None:
        for gender, count in users_by_gender.items():
            print(' * {}: {}'.format(gender, fmt.int_formatter(count)))
    else:
        print('No user gender data available')

    # Display earliest, most recent, and most common year of birth
    print('\nYear of birth stats:')
    if user_stats.has_birth_year_stats():
        print(' * Earliest: {}'.format(user_stats.earliest_birth_year))
        print(' * Most recent: {}'.format(user_stats.most_recent_birth_year))
        print(' * Most common: {}'.format(user_stats.most_common_birth_year))
    else:
        print('No year of birth data available')

    seconds = fmt.float_formatter(retriever.operation_time['user'])
    print("\nThis took {} seconds.".format(seconds))
    print('-' * 40)


def main():
    while True:
        city, month, day = get_filters()

        try:
            stats_retriever = load_data(city, month, day)
            time_stats(stats_retriever)
            station_stats(stats_retriever)
            trip_duration_stats(stats_retriever)
            user_stats(stats_retriever)
        except ValueError:
            print('\nThere is no data for your filter combination, try another one')
            print('-' * 40)

        restart = int(input('\nWhat do you like to do?\n[0] Exit\n[1] Restart\n[2] View the 50 first records\nYour choice: ').strip())
        if restart == 2:
            print(stats_retriever.take_first(50))
            break
        elif restart == 0:
            break



if __name__ == "__main__":
    main()
