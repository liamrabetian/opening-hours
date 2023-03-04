from pydantic import BaseModel


class FormattedHours(BaseModel):
    day: str
    hours: str

    def to_str(self) -> str:
        return f"{self.hours}"


class OpeningHoursOutput(BaseModel):
    monday: str
    tuesday: str
    wednesday: str
    thursday: str
    friday: str
    saturday: str
    sunday: str
