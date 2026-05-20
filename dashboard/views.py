from datetime import datetime
from importlib import import_module
import json
import logging
from random import randint

from django.conf import settings
from django.core.cache import cache
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.utils import timezone

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
    if not data:
        return data

    formatted = {"current_forecast": data[get_time_of_day()], **data}

    out = {}
    for k, v in formatted.items():
        if not isinstance(v, str):
            out.update({k: v})
            continue

        if v.lower().startswith("tiada hujan"):
            out.update({k: "☀️"})
        elif v.lower().startswith("hujan"):
            out.update({k: "🌧️"})
        elif v.lower().startswith("ribut"):
            out.update({k: "🌪️"})

        if k == "night_forecast" and v.lower().startswith("tiada hujan"):
            out.update({k: "🌙"})

    return out


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


def dashboard(request):
    quotes = []
    with open(settings.BASE_DIR / "dashboard" / "quotes.json") as f:
        quotes = [*json.load(f)]

    raw_weather_data = get_redis_data("weather_forecast")
    raw_prayer_data = get_redis_data("prayer_time")
    raw_arrival_data = get_redis_data("train_arrival")

    context = {
        "today_date": timezone.now().strftime("%a, %d %b %Y"),
        "weather_forecast": format_weather_data(raw_weather_data),
        "train_arrival": format_train_arrival_data(raw_arrival_data),
        "prayer_time": format_prayer_data(raw_prayer_data),
        "quote": quotes[randint(0, len(quotes) - 1)],
    }

    return render(request=request, template_name="dashboard.html", context=context)


def refresh_feed(request):
    if request.method != "POST":
        return

    for val in settings.CELERY_BEAT_SCHEDULE.values():
        module_name = ".".join(val["task"].split(".")[:-1])
        func_name = val["task"].split(".")[-1]

        module = import_module(module_name)
        func = getattr(module, func_name)
        func.delay(*val["args"])

    return HttpResponseRedirect(redirect_to=reverse("dashboard:index"))
