import json

from celery import shared_task
from django.conf import settings
from redis import from_url as Redis

from .solat.api import get_prayer_time as prayer_time_api
from .ktmb.api import KTMBData
from .weather.utils import get_weather_summary
from .weather.api import TodayWeather


def store_result(key: str, value) -> None:
    r = Redis(settings.CELERY_BROKER_URL)
    r.set(key, json.dumps(value))
    r.close()


@shared_task
def get_weather_forecast(locations: list[str]):
    """
    Get weather forecast and store into redis
    """
    get_forecast = TodayWeather()
    forecast_data = get_weather_summary(get_forecast(locations=locations))
    store_result("weather_forecast", forecast_data)


@shared_task
def get_train_time(kwargs: dict):
    """
    Get train arrival time for given stations and store into redis
    """
    get_train_time = KTMBData()
    arrival_data = get_train_time(**kwargs)

    store_result("train_arrival", arrival_data)


@shared_task
def get_prayer_time(location):
    """
    Get prayer time and store result into redis
    """
    store_result("prayer_time", prayer_time_api(location))
