import datetime

from dateutil import tz


def now():
    return datetime.datetime.now(tz=tz.UTC)
