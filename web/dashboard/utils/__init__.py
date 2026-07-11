from datetime import datetime
import json
import logging

from django.core.cache import cache
from django.utils import timezone

from .calendar_ import get_html_calendar  # noqa

logger = logging.getLogger(__name__)

TIME_DISPLAY_FORMAT = "%I:%M %p"


def get_redis_data(key: str) -> dict:
    """
    Retrieve data from Redis and format it into dict
    """
    redis = cache._cache.get_client()

    out = {}
    logger.info({"msg": "Retrieving data from Redis", "key": key})
    try:
        out = json.loads(redis.get(key))
        logger.info({"msg": "Retrieved data from Redis", "data": out})
    except TypeError:
        logger.error({"msg": "Data not found in Redis", "key": key})
    return out


def get_time_of_day() -> str:
    current_hour = timezone.now().hour

    tod = "night_forecast"
    if 5 <= current_hour < 12:
        tod = "morning_forecast"
    elif 12 <= current_hour < 19:
        tod = "afternoon_forecast"

    return tod


def format_weather_data(data: dict) -> dict:
    """
    Add 'current_forecast' key
    """
    logger.info(
        {
            "msg": "Formatting weather data",
            "raw_data": data,
        }
    )
    if not data:
        return data

    out = {}
    for k, v in data.items():
        if not isinstance(v, str):
            out.update({k: v})
            continue

        if v.lower().startswith("tiada hujan"):
            out.update({k: "☀️"})
        elif v.lower().startswith("hujan"):
            out.update({k: "🌧️"})
        elif v.lower().startswith("ribut"):
            out.update({k: "🌪️"})
        elif v.lower().startswith("mendung"):
            out.update({k: "🌦️"})
        else:
            out.update({k: v})

        if k == "night_forecast" and v.lower().startswith("tiada hujan"):
            out.update({k: "🌙"})

    return {"current_forecast": out[get_time_of_day()], **out}


def format_prayer_data(data: dict) -> dict:
    out = {}
    for k, v in data.items():
        try:
            d = datetime.strptime(v, "%H:%M:%S").strftime(TIME_DISPLAY_FORMAT).lower()
        except ValueError:
            d = v
        out.update({k: d})

    return out


def format_train_arrival_data(data: dict) -> list[dict]:
    out = []
    for station_name, arrival_times in data.items():
        formatted_arrival_times = []
        for at in arrival_times:
            try:
                d = (
                    datetime.strptime(at, "%H:%M:%S")
                    .strftime(TIME_DISPLAY_FORMAT)
                    .lower()
                )
            except ValueError:
                formatted_arrival_times.append(at)
            else:
                formatted_arrival_times.append(d)

        out.append(
            {
                "name": station_name.title(),
                "arrival_times": formatted_arrival_times,
            }
        )

    return out
