import json

import pytest
from app.api.helpers.cache import (
    get_opening_hours_result_from_cache,
    set_processed_opening_time_to_cache,
)
from app.core.connections import redis_cache
from app.main import shutdown_event, startup_event


@pytest.mark.asyncio
async def test_set_processed_opening_time_to_cache(
    input_hash, opening_hours_output, redis_connection, redis_test_database
):
    await startup_event(db=1)
    await set_processed_opening_time_to_cache(
        input_hash, opening_times=opening_hours_output
    )
    cache_value = await redis_cache.get(input_hash)
    assert isinstance(cache_value, bytes)
    redis_connection.flushdb()
    await shutdown_event()


@pytest.mark.asyncio
async def test_get_opening_hours_result_from_cache(
    input_hash, opening_hours_output, redis_connection, redis_test_database
):
    await startup_event(db=1)
    await set_processed_opening_time_to_cache(
        input_hash, opening_times=opening_hours_output
    )
    cache_value = await get_opening_hours_result_from_cache(input_hash)
    assert isinstance(cache_value, bytes)
    assert json.loads(cache_value) == opening_hours_output
    redis_connection.flushdb()
    await shutdown_event()
