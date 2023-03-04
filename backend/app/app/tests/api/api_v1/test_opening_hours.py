import json

from app.core.config import settings
from fastapi.testclient import TestClient


def test_api_schema_validation(client: TestClient, opening_hours_input: dict) -> None:
    opening_hours_input["sunday"][-1]["type"] = "open"
    opening_hours_input = json.dumps(opening_hours_input)
    expected_output = {
        "detail": [
            {
                "loc": ["body"],
                "msg": "cannot have the same type for start and end of the week",
                "type": "value_error",
            }
        ]
    }
    r = client.post(f"{settings.API_V1_STR}/opening-hours/", data=opening_hours_input)
    assert r.status_code == 422
    assert r.json() == expected_output


def test_api_correct_result(
    client: TestClient,
    opening_hours_input: dict,
    opening_hours_output: dict,
    clear_cache,
) -> None:
    opening_hours_input = json.dumps(opening_hours_input)
    r = client.post(f"{settings.API_V1_STR}/opening-hours/", data=opening_hours_input)
    assert r.status_code == 200
    assert r.json() == opening_hours_output
