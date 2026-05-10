from datetime import datetime
import logging

import requests
from requests.exceptions import HTTPError

from .constants import Location, Frequency

logger = logging.getLogger(__name__)

BASE_URL = "https://www.e-solat.gov.my/index.php?r=esolatApi/takwimsolat"

class Jakim:
    date_format = "%d-%b-%Y"

    def __call__(self, location: Location):
        url = f"{BASE_URL}&period={Frequency.WEEK.value}&zone={location.value}"

        logger.info(
            {
                "msg": "Retrieving data from JAKIM",
                "url": url
            }
        )

        response = requests.get(url)
        try:
            response.raise_for_status()
        except HTTPError:
            logger.exception(
                {
                    "msg": "Failed retrieving data from JAKIM",
                    "url": url,
                    "response": response.text,
                    "status_code": response.status_code
                }
            )

        today_date = datetime.now().strftime(self.date_format)
        data = response.json()["prayerTime"]
        return list(filter(lambda d: d["date"] == today_date, data))[0]
