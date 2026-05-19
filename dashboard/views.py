import json

from django.shortcuts import render
from django.core.cache import cache


def dashboard(request):
    redis = cache._cache.get_client()

    context = {
        "weather_forecast": json.loads(redis.get("weather_forecast")),
        "train_arrival": json.loads(redis.get("train_arrival")),
        "prayer_time": json.loads(redis.get("prayer_time")),
    }

    return render(request=request, template_name="dashboard.html", context=context)
