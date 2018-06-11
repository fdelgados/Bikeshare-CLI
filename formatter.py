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



