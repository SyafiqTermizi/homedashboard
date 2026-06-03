from importlib import import_module
import json
import logging
from random import randint

from django.conf import settings
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.utils import timezone

from .utils import (
    get_html_calendar,
    get_redis_data,
    format_prayer_data,
    format_train_arrival_data,
    format_weather_data,
)

logger = logging.getLogger(__name__)


def dashboard(request):
    quotes = []
    with open(settings.BASE_DIR / "web" / "dashboard" / "quotes.json") as f:
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
        "calendar": get_html_calendar()
    }

    return render(request=request, template_name="dashboard.html", context=context)


def refresh_feed(request):
    if request.method != "POST":
        return

    for val in settings.CELERY_BEAT_SCHEDULE.values():
        module_name = ".".join(val["task"].split(".")[:-1])
        func_name = val["task"].split(".")[-1]

        logger.info(
            {"msg": "Importing module", "module": module_name, "func": func_name}
        )

        module = import_module(module_name)
        func = getattr(module, func_name)
        func.delay(*val["args"])

    return HttpResponseRedirect(redirect_to=reverse("dashboard:index"))
