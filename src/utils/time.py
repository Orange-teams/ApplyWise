from datetime import datetime
from config.settings import TIMEZONE

def now():
    return datetime.now(TIMEZONE)