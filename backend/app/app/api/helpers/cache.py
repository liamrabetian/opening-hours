import json
from logging import getLogger
from typing import Union

import aioredis
from app.core.connections import redis_cache

logger = getLogger(__name__)


async def get_opening_hours_result_from_cache(input_hash: str) -> Union[bytes, None]:
    """Checks for processed opening_time result.
    If there are no data in the cache, returns None.

    Cache invalidation mechanism: Not needed for formatting use case, time expiration.

    Args:
        input_hash (str): the input data converted to hash

    Returns:
        binary | None
    """
    try:
        cache_value: json = await redis_cache.get(input_hash)
        if cache_value:
            return cache_value
    except aioredis.RedisError as err:  # pragma: no cover # general exception
        logger.error("error with cache backend", exc_info=err)


async def set_processed_opening_time_to_cache(
    input_hash: str, opening_times: dict
) -> None:
    """Store processed opening_time data in cache.
    Default expiration time is 24 hours.

    Args:
        input_hash (str): Used as the key for the key/value store
        opening_times (dict): Processed opening_times
    """
    cache_value = json.dumps(opening_times)
    try:
        await redis_cache.execute(
            "set", input_hash, cache_value, "ex", twenty_four_hours := 24 * 3600
        )
    except aioredis.RedisError as err:  # pragma: no cover # general exception
        logger.error("error in cache backend", exc_info=err)
        return
    logger.debug("new processed opening times data is cached, %s", input_hash)
