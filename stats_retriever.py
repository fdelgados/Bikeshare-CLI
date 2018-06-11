import time
import pandas as pd
import numpy

from stats import *
import utils as ut


class StatsRetriever:
    """ This class manages a DataFrame and compute statistics. """

    SLICE_SIZE = 10
    """ DataFrame slice size """

    def __init__(self, city, month_name='All', weekday='All'):
        """ Construct a new StatsRetriever object
        Args:
            (str) city: city name of which you want to analyze the data
            (str) month_name: month name
            (str) weekday: day of week
        """

        self.dataFrame = None
        self.month_name = month_name.title()
        self.weekday = weekday.title()
        self.city = city
        self.start_time = 0.0
        self.operation_time = {
            'time': 0.0,
            'station': 0.0,
            'trip_duration': 0.0,
            'user': 0.0
        }

        try:
            self._load_data()
        except ValueError:
            raise EmptyDataFrameException('DataFrame is empty')

    def _load_data(self):
        """ Loads data for the specified city and filters by month and day if applicable. """

        self.dataFrame = pd.read_csv(ut.city_data_file_path(self.city))

        self.dataFrame['Start Time'] = pd.to_datetime(self.dataFrame['Start Time'])

        self.dataFrame['Month'] = self.dataFrame['Start Time'].dt.month
        if self.month_name != 'All':
            self.dataFrame = self.dataFrame[self.dataFrame['Month'] == ut.month_by_name(self.month_name)]

        self._guard_against_empty_data_frame()

        self.dataFrame['Weekday'] = self.dataFrame['Start Time'].dt.weekday_name
        if self.weekday != 'All':
            self.dataFrame = self.dataFrame[self.dataFrame['Weekday'] == self.weekday]

        self._guard_against_empty_data_frame()

    def _guard_against_empty_data_frame(self):
        """ Throws an exception if the DataFrame is empty.

        Raises:
            ValueError: if the DataFrame is empty
        """

        if self.dataFrame.empty:
            raise EmptyDataFrameException('DataFrame is empty')

    def time_stats(self):
        """ Computes the time stats.

        Returns:
            TimeStats: A time stats object
        """

        self._start_clock()

        most_common_month = ut.month_name(self.dataFrame['Month'].mode()[0])
        most_common_day_of_week = self.dataFrame['Weekday'].mode()[0]
        self.dataFrame['Hour'] = self.dataFrame['Start Time'].dt.hour
        most_common_start_hour = self.dataFrame['Hour'].mode()[0]

        self._stop_clock('time')

        return TimeStats(most_common_month,
                         most_common_day_of_week,
                         most_common_start_hour)

    def station_stats(self):
        """ Computes the station stats.

        Returns:
            StationStats: A station stats object
        """

        self._start_clock()

        self.dataFrame['StartEnd Stations'] = self.dataFrame['Start Station'] \
                                              + ' -> ' \
                                              + self.dataFrame['End Station']

        most_common_start_station = self.dataFrame['Start Station'].mode()[0]
        most_common_end_station = self.dataFrame['End Station'].mode()[0]
        most_common_start_end_stations = self.dataFrame['StartEnd Stations'].mode()[0]

        self._stop_clock('station')

        return StationStats(most_common_start_station,
                            most_common_end_station,
                            most_common_start_end_stations)

    def trip_duration_stats(self):
        """ Computes the trip duration stats.

        Returns:
            TripDurationStats: A trip duration stats object
        """

        self._start_clock()

        total_trips_duration = self.dataFrame['Trip Duration'].sum()
        avg_trip_duration = self.dataFrame['Trip Duration'].mean()

        self._stop_clock('trip_duration')

        return TripDurationStats(total_trips_duration,
                                 avg_trip_duration)

    def user_stats(self):
        """Computes the user info stats.

        Returns:
            UserStats: A user stats object
        """

        self._start_clock()

        users_by_type = self.dataFrame.groupby('User Type').size()

        try:
            users_by_gender = self.dataFrame.groupby('Gender').size()
        except KeyError:
            users_by_gender = None

        try:
            earliest_birth_year = self.dataFrame['Birth Year'].min().astype(int)
            most_recent_birth_year = self.dataFrame['Birth Year'].max().astype(int)
            most_common_birth_year = self.dataFrame['Birth Year'].mode()[0].astype(int)
        except KeyError:
            earliest_birth_year = None
            most_recent_birth_year = None
            most_common_birth_year = None

        self._stop_clock('user')

        return UserStats(users_by_type,
                         earliest_birth_year,
                         most_recent_birth_year,
                         most_common_birth_year,
                         users_by_gender)

    def num_results(self):
        """ Returns the total number of records

        Returns:
            int: number of records
        """

        return self.dataFrame.shape[0]

    def take_first(self, num=None):
        """ Returns the first <num> rows of the DataFrame

        Returns:
            rows: the first <num> rows
        """
        num = num if num is not None else self.SLICE_SIZE

        return self.dataFrame.head(num)

    def raw_data(self, start=0):
        """ Returns a tuple containing a list of column names and a DataFrame subset sliced from
            start and with a size equals to self.SIZE

        Args:
            start (int): first slice index
        Returns:
            (list, numpy.ndarray): the first element is a list of column names, the second is a numpy ndarray
            containing the DataFrame values
        """

        end = start + self.SLICE_SIZE

        return list(self.dataFrame.columns.values), self.dataFrame.iloc[start:end].values

    def _start_clock(self):
        """ Sets the operation start time. """

        self.start_time = time.time()

    def _stop_clock(self, operation):
        """ Sets the total operation time. """
        self.operation_time[operation] = time.time() - self.start_time


class EmptyDataFrameException(Exception):
    pass
