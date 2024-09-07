from opensky_api import OpenSkyApi
from datetime import datetime, timedelta

api = OpenSkyApi()

def flightDepartures(icao):
    current_time = datetime.now()
    current_timestamp = int(current_time.timestamp())

    # Get the time 1 hour ago as a UNIX timestamp
    starttime = current_time - timedelta(hours=5)
    starttimestamp = int(starttime.timestamp())

    departures = api.get_departures_by_airport(icao, starttimestamp, current_timestamp)
    return departures

def flightArrivals(icao):
    current_time = datetime.now()
    current_timestamp = int(current_time.timestamp())

    # Get the time 1 hour ago as a UNIX timestamp
    starttime = current_time - timedelta(hours=1)
    starttimestamp = int(starttime.timestamp())

    arrivals = api.get_arrivals_by_airport(icao, starttimestamp, current_timestamp)
    return arrivals