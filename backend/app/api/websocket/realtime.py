"""
WebSocket endpoints for real-time updates
"""
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import Dict, Set
from app.core.logger import app_logger
from app.models.schemas import WSMessage
from datetime import datetime
import json

router = APIRouter()

# Store active connections
class ConnectionManager:
    def __init__(self):
        self.active_connections: Set[WebSocket] = set()
        self.user_connections: Dict[str, Set[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, user_id: str = "default"):
        await websocket.accept()
        self.active_connections.add(websocket)

        if user_id not in self.user_connections:
            self.user_connections[user_id] = set()
        self.user_connections[user_id].add(websocket)

        app_logger.info(f"WebSocket connected: {user_id} (Total: {len(self.active_connections)})")

    def disconnect(self, websocket: WebSocket, user_id: str = "default"):
        self.active_connections.discard(websocket)

        if user_id in self.user_connections:
            self.user_connections[user_id].discard(websocket)
            if not self.user_connections[user_id]:
                del self.user_connections[user_id]

        app_logger.info(f"WebSocket disconnected: {user_id} (Total: {len(self.active_connections)})")

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def send_to_user(self, message: str, user_id: str):
        if user_id in self.user_connections:
            for connection in self.user_connections[user_id]:
                try:
                    await connection.send_text(message)
                except:
                    pass

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except:
                pass


manager = ConnectionManager()


@router.websocket("/updates")
async def websocket_endpoint(websocket: WebSocket, user_id: str = "default"):
    """WebSocket endpoint for real-time updates"""
    await manager.connect(websocket, user_id)

    try:
        # Send welcome message
        welcome_msg = WSMessage(
            type="connection",
            data={
                "status": "connected",
                "message": "Connected to BluePeak Compass real-time updates",
                "user_id": user_id
            }
        )
        await manager.send_personal_message(welcome_msg.model_dump_json(), websocket)

        # Listen for messages
        while True:
            data = await websocket.receive_text()
            app_logger.info(f"Received WS message from {user_id}: {data[:100]}")

            try:
                # Parse incoming message
                message = json.loads(data)
                message_type = message.get("type", "unknown")

                # Handle different message types
                if message_type == "ping":
                    response = WSMessage(
                        type="pong",
                        data={"timestamp": datetime.utcnow().isoformat()}
                    )
                    await manager.send_personal_message(response.model_dump_json(), websocket)

                elif message_type == "subscribe":
                    # Subscribe to specific events
                    topics = message.get("data", {}).get("topics", [])
                    response = WSMessage(
                        type="subscription",
                        data={
                            "status": "subscribed",
                            "topics": topics
                        }
                    )
                    await manager.send_personal_message(response.model_dump_json(), websocket)

                else:
                    # Echo back unknown messages
                    await manager.send_personal_message(data, websocket)

            except json.JSONDecodeError:
                error_msg = WSMessage(
                    type="error",
                    data={"message": "Invalid JSON format"}
                )
                await manager.send_personal_message(error_msg.model_dump_json(), websocket)

    except WebSocketDisconnect:
        manager.disconnect(websocket, user_id)
        app_logger.info(f"Client {user_id} disconnected")

    except Exception as e:
        app_logger.error(f"WebSocket error for {user_id}: {e}")
        manager.disconnect(websocket, user_id)


async def broadcast_update(update_type: str, data: Dict):
    """Broadcast an update to all connected clients"""
    message = WSMessage(
        type=update_type,
        data=data
    )
    await manager.broadcast(message.model_dump_json())


async def send_user_notification(user_id: str, notification_type: str, data: Dict):
    """Send notification to specific user"""
    message = WSMessage(
        type=notification_type,
        data=data
    )
    await manager.send_to_user(message.model_dump_json(), user_id)
