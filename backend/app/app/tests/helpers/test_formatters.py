from app.api.helpers.formatters import (
    convert_timestamp_to_string,
    format_opening_hours_output,
    parse_and_format_opening_hours,
    transform_hours,
)
from app.schemas import OpeningHourType


def test_transform_hours():
    hours_data = {
        "Monday": [
            {"type": OpeningHourType.OPEN, "value": 0},
            {"type": OpeningHourType.CLOSE, "value": 3600},
        ],
        "Tuesday": [
            {"type": OpeningHourType.OPEN, "value": 0},
            {"type": OpeningHourType.CLOSE, "value": 7200},
            {"type": OpeningHourType.OPEN, "value": 10800},
            {"type": OpeningHourType.CLOSE, "value": 14400},
        ],
    }
    expected_output = {
        "Monday": ["12 AM - 1 AM"],
        "Tuesday": ["12 AM - 2 AM", "3 AM - 4 AM"],
    }
    assert transform_hours(hours_data) == expected_output


def test_format_opening_hours_output():
    transformed_data = {
        "Monday": ["12 AM - 1 AM"],
        "Tuesday": ["12 AM - 2 AM", "3 AM - 4 AM"],
        "Wednesday": [],
        "Thursday": [],
        "Friday": [],
        "Saturday": [],
        "Sunday": [],
    }
    expected_output = {
        "monday": "12 AM - 1 AM",
        "tuesday": "12 AM - 2 AM, 3 AM - 4 AM",
        "wednesday": "Closed",
        "thursday": "Closed",
        "friday": "Closed",
        "saturday": "Closed",
        "sunday": "Closed",
    }
    assert format_opening_hours_output(transformed_data) == expected_output


def test_parse_and_format_opening_hours(opening_hours_output, opening_hours_input):
    output = parse_and_format_opening_hours(opening_hours_input)
    assert output == opening_hours_output


def test_convert_timestamp_to_string():
    assert convert_timestamp_to_string(0) == "12 AM"
    assert convert_timestamp_to_string(3600) == "1 AM"
    assert convert_timestamp_to_string(37800) == "10:30 AM"
    assert convert_timestamp_to_string(86399) == "11:59 PM"
