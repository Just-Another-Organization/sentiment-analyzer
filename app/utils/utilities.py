from datetime import datetime, timedelta

import utils.constants as constants


def get_sentiment_by_scores(scores):
    max_rank = max(scores)
    sentiment_index = scores.index(max_rank)

    if sentiment_index == 0:
        return constants.NEGATIVE
    elif sentiment_index == 1:
        return constants.NEUTRAL
    elif sentiment_index == 2:
        return constants.POSITIVE


def get_sentiment_by_label(label):
    return constants.LABELS[label]


def get_seconds_by_interval(interval):
    # intervals = ['1M', '1w', '3d', '1d', '12h', '8h', '6h', '4h', '2h', '1h', '30m', '15m', '5m', '3m', '1m']
    interval_digit = interval[0: len(interval) - 1]
    interval_period = interval[len(interval) - 1: len(interval)]

    periods = {
        'm': 60,
        'h': 3600,  # 60 * 60
        'd': 86400,  # 24 * 60 * 60
        'w': 604800,  # 7 * 24 * 60 * 60,
        'M': 2592000,  # 30 * 24 * 60 * 60,
    }
    time_multiplier = periods[interval_period]
    return int(interval_digit) * time_multiplier


def get_interval(interval, end_time=None):
    if end_time is None:
        # End time must be a minimum of 10 seconds prior to the request time.
        # Using 60 seconds as threshold instead of 10.
        end_time = datetime.utcnow() - timedelta(seconds=60)
    interval = get_seconds_by_interval(interval)
    start_time = end_time - timedelta(seconds=interval)
    return start_time, end_time
