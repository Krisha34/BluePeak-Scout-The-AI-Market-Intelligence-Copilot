"""
WebSocket API module
"""
from fastapi import APIRouter
from app.api.websocket.realtime import router as realtime_router

websocket_router = APIRouter()
websocket_router.include_router(realtime_router)
