class TimeStats:
    """ This class stores the results of time stats calculations. """

    def __init__(self, most_common_month, most_common_day_of_week, most_common_start_hour):
        """ Construct a new TimeStats object
        Args:
            (str) most_common_month:
            (str) most_common_day_of_week:
            (str) most_common_start_hour:
        """

        self.most_common_month = most_common_month
        self.most_common_day_of_week = most_common_day_of_week
        self.most_common_start_hour = most_common_start_hour


class StationStats:
    """ This class stores the results of station stats calculations. """

    def __init__(self, most_common_start_station, most_common_end_station, most_common_start_end_stations):
        """ Construct a new StationStats object
        Args:
            (str) most_common_start_station:
            (str) most_common_end_station:
            (str) most_common_start_end_stations:
        """

        self.most_common_start_station = most_common_start_station
        self.most_common_end_station = most_common_end_station
        self.most_common_start_end_stations = most_common_start_end_stations


class TripDurationStats:
    """ This class stores the results of trip duration stats calculations. """

    def __init__(self, total_trips_duration, avg_trip_duration):
        """ Construct a new TripDurationStats object
        Args:
            (float) total_trips_duration:
            (float) avg_trip_duration:
        """

        self.total_trips_duration = total_trips_duration
        self.avg_trip_duration = avg_trip_duration


class UserStats:
    """ This class stores the results of user info stats calculations. """

    def __init__(self,
                 users_by_type,
                 earliest_birth_year=None,
                 most_recent_birth_year=None,
                 most_common_birth_year=None,
                 users_by_gender=None):
        """ Construct a new UserStats object
        Args:
            (DataFrameGroupBy) users_by_type: Number of users by type
            (int) earliest_birth_year:
            (int) most_recent_birth_year:
            (int) most_common_birth_year:
            (DataFrameGroupBy) users_by_gender: Number of users by gender
        """
        self.users_by_type = users_by_type
        self.earliest_birth_year = earliest_birth_year
        self.most_recent_birth_year = most_recent_birth_year
        self.most_common_birth_year = most_common_birth_year
        self.users_by_gender = users_by_gender

    def has_birth_year_stats(self):
        """ Check if the birth of year stats has ben computed.

        Returns:
            bool
        """

        return self.earliest_birth_year is not None and \
               self.most_recent_birth_year is not None and \
               self.most_common_birth_year is not None
