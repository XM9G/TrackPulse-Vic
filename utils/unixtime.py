import time
import datetime


def convert_to_unix_time(date: datetime.datetime) -> str:
    # Get the end date
    end_date = date

    # Get a tuple of the date attributes
    date_tuple = (end_date.year, end_date.month, end_date.day, end_date.hour, end_date.minute, end_date.second)

    # Convert to unix time
    return f'<t:{int(time.mktime(datetime.datetime(*date_tuple).timetuple()))}:R>'

def convert_iso_to_unix_time(iso_time: str, format=None) -> str:
    # Parse the ISO 8601 formatted time string
    date = datetime.datetime.fromisoformat(iso_time.replace('Z', '+00:00'))

    # Convert to the computer's current timezone
    date_local = date.astimezone()

    # Convert to Unix time
    unix_time = int(time.mktime(date_local.timetuple()))

    if format=='long-time':
        return f'<t:{unix_time}:T>'
    elif format=='short-time':
        return f'<t:{unix_time}:t>'
    else:
        # Format Unix time for Discord's timestamp
        return f'<t:{unix_time}:R>'
    