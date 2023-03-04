from enum import Enum
from typing import Dict, List

from pydantic import BaseModel, validator


class OpeningHourType(str, Enum):
    OPEN = "open"
    CLOSE = "close"


class OpeningHour(BaseModel):
    type: str
    value: int


class Weekday(str, Enum):
    MONDAY = "monday"
    TUESDAY = "tuesday"
    WEDNESDAY = "wednesday"
    THURSDAY = "thursday"
    FRIDAY = "friday"
    SATURDAY = "saturday"
    SUNDAY = "sunday"


class OpeningHours(BaseModel):
    __root__: Dict[Weekday, List[OpeningHour]]

    @validator("__root__")
    def validate(cls, data):
        """
        Validate the input data for the OpeningHours model.

        Args:
            cls: The OpeningHours class.
            data: The input data to validate, which is expected to be a dictionary with a key
                  for each day of the week, and values that are a list of OpeningHour objects.

        Raises:
            ValueError: If the input data does not contain at least 2 events, has the same event
                        type for the start and end of the week, contains invalid opening hour types,
                        contains values that are not between 0 and 86399, or has consecutive events
                        of the same type.
        Returns:
            The validated input data if no errors are raised.
        """
        event_types = [event["type"] for day in data.values() for event in day]
        if len(event_types) < 2:
            raise ValueError("input data must contain at least 2 events")
        if event_types[0] == event_types[-1]:
            raise ValueError("cannot have the same type for start and end of the week")
        for day, events in data.items():
            for i, event in enumerate(events[:-1]):
                next_event = events[i + 1]
                if event["type"] not in OpeningHourType.__members__.values():
                    raise ValueError('type must be "open" or "close"')
                if event["value"] < 0 or event["value"] > 86399:
                    raise ValueError("value must be between 0 and 86399")
                if event["type"] == next_event["type"]:
                    raise ValueError(
                        f"consecutive {event['type']} times are not allowed for {day}"
                    )
        return data
