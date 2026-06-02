from services.solat.api import get_prayer_time
from services.solat.constants import Location


if __name__ == "__main__":
    get_prayer_time(Location.WLY01)