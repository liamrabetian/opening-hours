import hashlib
from typing import Generator

import pytest
from fastapi.testclient import TestClient
from redis import Redis

from app.core.config import settings
from app.main import app, shutdown_event, startup_event


@pytest.fixture()
def client() -> Generator:
    with TestClient(app) as c:
        yield c


# Seperate redis database for the tests
@pytest.fixture
async def redis_test_database():
    await startup_event(db=1)
    yield
    await shutdown_event()


@pytest.fixture
def redis_connection():
    return Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=1)


@pytest.fixture
def clear_cache(redis_connection):
    def _clear_cache():
        redis_connection.flushdb()

    _clear_cache()
    return _clear_cache


@pytest.fixture()
def opening_hours_input():
    return {
        "monday": [],
        "tuesday": [
            {"type": "open", "value": 36000},
            {"type": "close", "value": 64800},
        ],
        "wednesday": [],
        "thursday": [
            {"type": "open", "value": 37800},
            {"type": "close", "value": 64800},
        ],
        "friday": [{"type": "open", "value": 36000}],
        "saturday": [
            {"type": "close", "value": 3600},
            {"type": "open", "value": 36000},
        ],
        "sunday": [
            {"type": "close", "value": 3600},
            {"type": "open", "value": 43200},
            {"type": "close", "value": 75600},
        ],
    }


@pytest.fixture()
def input_hash(opening_hours_input):
    return hashlib.sha256(str(opening_hours_input).encode()).hexdigest()


@pytest.fixture
def opening_hours_output():
    return {
        "monday": "Closed",
        "tuesday": "10 AM - 6 PM",
        "wednesday": "Closed",
        "thursday": "10:30 AM - 6 PM",
        "friday": "10 AM - 1 AM",
        "saturday": "10 AM - 1 AM",
        "sunday": "12 PM - 9 PM",
    }
