from collections import defaultdict
import csv
from datetime import datetime
from enum import Enum
import io
import logging
import zipfile

import requests

logger = logging.getLogger(__name__)
BASE_URL = "https://api.data.gov.my/gtfs-static/ktmb"

ROUTE_SNAME = "Seremban Line"


class Direction(Enum):
    NORTHBOUND = "1"
    SOUTHBOUND = "0"


class Service(Enum):
    WEEKEND = "komuter_weekend"
    WEEKDAY = "komuter_weekday"


class KTMBData:
    def __init__(self):
        self.api_data = self.get_api_data()

    def get_api_data(self) -> dict[str, list]:
        """
        Read response zip file for given file name
        """
        response = requests.get(BASE_URL)

        data = {}
        with zipfile.ZipFile(io.BytesIO(response.content)) as zip_file:
            for fn in ["routes.txt", "stops.txt", "stop_times.txt", "trips.txt"]:
                with zip_file.open(fn, "r") as csv_file:
                    # the var csv_file is of ZipExtFile type. We cast it into
                    # StringIO so it can be passed into csv.DictReader
                    f = io.StringIO(csv_file.read().decode())
                    data.update({fn.split(".")[0]: [*list(csv.DictReader(f))]})

        return data

    def get_service_id(self):
        """
        Get KTMB service ID
        """
        service_id = Service.WEEKDAY.value
        if datetime.now().weekday() >= 5:
            service_id = Service.WEEKEND.value

        return service_id

    def get_route_id(self, route_data: list, short_name: str) -> str:
        """
        Get internal KTMB route ID given and long route name
        """
        try:
            d = filter(
                lambda r: (r["route_short_name"] == short_name),
                route_data,
            )
        except KeyError:
            logger.exception({"msg": "Fail extracting data from routes"})
            return

        try:
            route_id = list(d)[0]["route_id"]
        except IndexError:
            logger.exception({"msg": "Can't find routes from routes"})
            return

        return route_id

    def get_stop_id(self, stop_data: dict, station_names: list[str]) -> dict[str, str]:
        """
        Get internal KTMB stop ID

        Returns a dict of { internal_id: readable_stop_name }
        """
        return {
            s["stop_id"]: s["stop_name"]
            for s in filter(
                lambda s: s["stop_name"].lower() in station_names, stop_data
            )
        }

    def __call__(
        self,
        route_sname: str,
        stations: list[str],
        direction: Direction,
    ) -> dict[str, list]:

        # 0. Get route id
        route_id = self.get_route_id(self.api_data["routes"], route_sname)

        if not route_id:
            return

        # 1. Get stop id from stop name
        stop_ids = self.get_stop_id(self.api_data["stops"], stations)

        # 2. Get trip_ids
        trip_ids = list(
            map(
                lambda t: t["trip_id"],
                filter(
                    lambda t: (t["route_id"] == route_id)
                    and t["service_id"] == self.get_service_id()
                    and t["direction_id"] == direction,
                    self.api_data["trips"],
                ),
            )
        )

        stop_times = []
        # 2. Get stop times
        for trip_id in trip_ids:
            stop_times += list(
                filter(
                    lambda st: st["trip_id"] == trip_id and st["stop_id"] in stop_ids,
                    self.api_data["stop_times"],
                )
            )

        out = defaultdict(list)
        for stop_id, stop_name in stop_ids.items():
            out[stop_name].extend(
                list(
                    map(
                        lambda st: st["arrival_time"],
                        filter(lambda st: st["stop_id"] == stop_id, stop_times),
                    )
                )
            )

        return out


if __name__ == "__main__":
    get_stop_data = KTMBData()
    o = get_stop_data(
        route_sname=ROUTE_SNAME,
        stations=["bangi", "kajang"],
        direction=Direction.NORTHBOUND.value,
    )

    o = get_stop_data(
        route_sname=ROUTE_SNAME,
        stations=["midvalley"],
        direction=Direction.SOUTHBOUND.value,
    )

    print(o)
    print(o)
