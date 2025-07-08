from datetime import datetime
from zoneinfo import ZoneInfo

TZ = ZoneInfo("Europe/Belgrade")

def now():
    return datetime.now(TZ)

def to_local(dt):
    return dt.astimezone(TZ)