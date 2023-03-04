from datetime import datetime
from typing import Dict, List

from app.schemas import OpeningHourType


def transform_hours(
    hours_data: Dict[str, List[Dict[str, int]]]
) -> Dict[str, List[str]]:
    """
    Process the hours data and converts them to a human readable time string

    Args:
        hours_data: A dictionary of opening hours data.

    Returns:
        A dictionary of opening hours data in a human-readable format. The dictionary is keyed by
        day of the week (e.g. "Monday", "Tuesday", etc.), and each value is a list of
        opening hour ranges for that day.
        The opening hour ranges are represented as strings in the format:
        "opening_time - closing_time".

    Raises:
        None
    """
    opening_time, current_day = None, None
    transformed_data = {}
    for day, events in hours_data.items():
        transformed_data[day] = []
        for event in events:
            if event["type"] == OpeningHourType.OPEN:
                opening_time = convert_timestamp_to_string(event["value"])
                current_day = day
            else:
                closing_time = convert_timestamp_to_string(event["value"])
                transformed_data[current_day].append(f"{opening_time} - {closing_time}")

    return transformed_data


def convert_timestamp_to_string(timestamp: int) -> str:
    dt = datetime.utcfromtimestamp(timestamp)
    if dt.minute == 0:
        return dt.strftime("%-l %p")
    else:
        return dt.strftime("%-l:%M %p")


def format_opening_hours_output(data: Dict[str, List[str]]) -> Dict[str, str]:
    """Format the transformed hours and include closed days."""
    formatted_dict = {
        day.lower(): ", ".join(times) if times else "Closed"
        for day, times in data.items()
    }
    return formatted_dict


def parse_and_format_opening_hours(
    data: Dict[str, List[Dict[str, int]]]
) -> Dict[str, str]:
    transformed_data = transform_hours(data)
    formatted_data = format_opening_hours_output(transformed_data)

    return formatted_data
