from datetime import datetime
import logging

import requests
from requests.exceptions import HTTPError

BASE_URL = "https://api.data.gov.my/weather/forecast"


logger = logging.getLogger(__name__)

DATE_FORMAT = "%Y-%m-%d"

class TodayWeather:
    """
    Get today's weather for given locations
    """

    def get_today_date_filter(self) -> str:
        today = datetime.now().strftime(DATE_FORMAT)
        return f"{today}@date"

    def get_today_weather(self) -> list:
        """
        Get today's weather for all location.
        """
        url = f"{BASE_URL}?contains={self.get_today_date_filter()}"
        
        try:
            response = requests.get(url=url)
            response.raise_for_status()
        except HTTPError:
            logger.exception(
                {
                    "msg": "Fail to retrieve data",
                    "url": BASE_URL,
                    "response": response.text,
                    "status_code": response.status_code
                }
            )

        return response.json()

    def __call__(self, locations: list[str]):
        data = self.get_today_weather()
        _locations = list(map(lambda l: l.lower(), locations))

        # The API only allow one filter at a time. So we are handling filtering of here.
        return list(
            filter(
                lambda d: d["location"]["location_name"].lower() in _locations,
                data
            )
        )
