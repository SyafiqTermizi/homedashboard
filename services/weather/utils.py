from collections import defaultdict


def get_weather_summary(data):
    """
    Given a list of weather forecast, return only one forecast with highest count
    """
    forecast_counter = {
        "morning_forecast": defaultdict(int),
        "afternoon_forecast": defaultdict(int),
        "night_forecast": defaultdict(int),
        "min_temp": defaultdict(int),
        "max_temp": defaultdict(int),
    }

    for datum in data:
        for forecast_time in forecast_counter.keys():
            forecast_counter[forecast_time][datum[forecast_time]] += 1

    out = {}
    for k, v in forecast_counter.items():
        out[k] = max(v, key=v.get)

    return out
