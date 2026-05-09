from enum import Enum

BASE_URL = "https://api.data.gov.my/gtfs-static/ktmb"
ROUTE_SNAME = "Seremban Line"


class Direction(Enum):
    NORTHBOUND = "1"
    SOUTHBOUND = "0"


class Service(Enum):
    WEEKEND = "komuter_weekend"
    WEEKDAY = "komuter_weekday"
