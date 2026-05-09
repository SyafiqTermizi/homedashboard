from datetime import datetime
import json

import requests

BASE_URL = "https://api.data.gov.my/weather/forecast"

class TodayWeather:
    """
    Get today's weather for given locations
    """

    base_url = "https://api.data.gov.my/weather/forecast"
    date_format = "%Y-%m-%d"

    def __init__(self, locations: list[str]):
        self.locations = locations

    def get_today_date_filter(self) -> str:
        today = datetime.now().strftime(self.date_format)
        return f"{today}@date"

    def get_today_weather(self) -> list:
        """
        Get today's weather for all location.
        """
        url = f"{self.base_url}?contains={self.get_today_date_filter()}"
        response = requests.get(url=url)
        return response.json()

    def __call__(self):
        data = self.get_today_weather()
        _locations = list(map(lambda l: l.lower(), self.locations))

        # The API only allow one filter at a time. So we are handling filtering of here.
        return list(
            filter(
                lambda d: d["location"]["location_name"].lower() in _locations,
                data
            )
        )

def main():
    get_today_weather = TodayWeather(locations=["baNgi", "kajang", "nilai"])
    return get_today_weather()


if __name__ == "__main__":
    print(json.dumps(main(), indent=2))
