from app.api.api_v1.endpoints import opening_hours, ping
from fastapi import APIRouter

api_router = APIRouter()

api_router.include_router(ping.router)
api_router.include_router(opening_hours.router, tags=["opening-hours"])
