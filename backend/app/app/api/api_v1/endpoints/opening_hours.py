import hashlib
import json
from logging import getLogger

from fastapi import APIRouter

from app.api.helpers import (
    get_opening_hours_result_from_cache,
    parse_and_format_opening_hours,
    set_processed_opening_time_to_cache,
)
from app.schemas import OpeningHours, OpeningHoursOutput

router = APIRouter()
logger = getLogger(__name__)


@router.post("/opening-hours", response_model=OpeningHoursOutput)
async def opening_hours(opening_hours_data: OpeningHours) -> OpeningHoursOutput:
    """Base API for processing opening times.
    Uses cache backend to retrieve the opening times for the same inputs.

    Args:
        opening_hours_data (OpeningHours)

    Returns:
        [OpeningHoursOutput]: Human readable opening times.
    """
    input_hash = hashlib.sha256(str(opening_hours_data).encode()).hexdigest()
    cache_value = await get_opening_hours_result_from_cache(input_hash=input_hash)
    if cache_value:
        logger.debug("reading opening_times from cache")
        return json.loads(cache_value)
    output = parse_and_format_opening_hours(opening_hours_data)
    await set_processed_opening_time_to_cache(input_hash, output)
    return output
