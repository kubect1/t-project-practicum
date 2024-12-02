import pytz

from app.schemas.coordinates import Coordinates
from timezonefinder import TimezoneFinder
import datetiem as dt

def get_timezone(location: Coordinates) -> pytz.timezone:
    tz_finder = TimezoneFinder()
    lng = float(location.longitude)
    lat = float(location.latitude)
    timezone_str = tz_finder.timezone_at(lat=lat, lng=lng)
    timezone = pytz.timezone(timezone_str)
    return timezone

def timezone_adaptation(datetime, timezone) -> dt.datetime:
    datetime = datetime.replace(tzinfo=timezone)
    datetime = datetime.astimezone(dt.timezone.utc)
    datetime = datetime.replace(tzinfo=None)
    return datetime