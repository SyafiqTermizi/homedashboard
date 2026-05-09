from datetime import datetime
import logging

import requests
from requests.exceptions import HTTPError

BASE_URL = "https://api.data.gov.my/weather/forecast"


logger = logging.getLogger(__name__)


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
        
        try:
            response = requests.get(url=url)
            response.raise_for_status()
        except HTTPError:
            logger.exception(
                {
                    "msg": "Fail to retrieve data",
                    "url": self.base_url,
                    "response": response.text,
                    "status_code": response.status_code
                }
            )

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
