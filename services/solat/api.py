from datetime import datetime
import logging

import requests
from requests.exceptions import HTTPError

from .constants import Location, Frequency

logger = logging.getLogger(__name__)

BASE_URL = "https://www.e-solat.gov.my/index.php?r=esolatApi/takwimsolat"


def get_jakim_date():
    """
    Get date format used by Jakim
    """
    month_map = {
        "1": "Jan",
        "2": "Feb",
        "3": "Mac",
        "4": "Apr",
        "5": "Mei",
        "6": "Jun",
        "7": "Jul",
        "8": "Ogos",
        "9": "Sep",
        "10": "Okt",
        "11": "Nov",
        "12": "Dis",
    }
    today_date = datetime.now()
    return f"{today_date.day}-{month_map[str(today_date.month)]}-{today_date.year}"


def get_prayer_time(location: Location):
    """
    Get prayer time from JAKIM
    """
    try:
        _location = location.value
    except AttributeError:
        _location = location

    url = f"{BASE_URL}&period={Frequency.YEAR.value}&zone={_location}"

    logger.info({"msg": "Retrieving data from JAKIM", "url": url})

    response = requests.get(url)

    try:
        response.raise_for_status()
    except HTTPError:
        logger.exception(
            {
                "msg": "Failed retrieving data from JAKIM",
                "url": url,
                "response": response.text,
                "status_code": response.status_code,
            }
        )

    data = response.json()["prayerTime"]

    return list(filter(lambda d: d["date"] == get_jakim_date(), data))[0]
