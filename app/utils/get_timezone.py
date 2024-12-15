import pytz

import datetime as dt
from timezonefinder import TimezoneFinder

from app.schemas.coordinates import Coordinates

def get_timezone(location: Coordinates) -> pytz.timezone:
    tz_finder = TimezoneFinder()
    lng = float(location.longitude)
    lat = float(location.latitude)
    timezone_str = tz_finder.timezone_at(lat=lat, lng=lng)
    timezone = pytz.timezone(timezone_str)
    return timezone

def timezone_adaptation(datetime: dt.datetime, timezone: pytz.tzinfo.DstTzInfo) -> dt.datetime:
    datetime = timezone.localize(datetime, True)
    datetime = datetime.astimezone(dt.timezone.utc)
    datetime = datetime.replace(tzinfo=None)
    return datetime