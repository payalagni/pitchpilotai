"""
WebSocket Manager - Handle real-time connections
"""

import asyncio
from typing import Dict, List
from fastapi import WebSocket


class ConnectionManager:
    """Manage WebSocket connections"""
    
    def __init__(self):
        self.active_connections: Dict[str, List[WebSocket]] = {}
    
    async def connect(self, websocket: WebSocket, session_id: str):
        """Connect a new WebSocket"""
        await websocket.accept()
        if session_id not in self.active_connections:
            self.active_connections[session_id] = []
        self.active_connections[session_id].append(websocket)
    
    def disconnect(self, session_id: str):
        """Disconnect a WebSocket"""
        if session_id in self.active_connections:
            self.active_connections[session_id] = [
                conn for conn in self.active_connections[session_id]
                if conn.close_code is None
            ]
            if not self.active_connections[session_id]:
                del self.active_connections[session_id]
    
    async def send_personal_message(self, message: dict, session_id: str):
        """Send message to a specific session"""
        if session_id in self.active_connections:
            for connection in self.active_connections[session_id]:
                try:
                    await connection.send_json(message)
                except:
                    pass
    
    async def broadcast_to_session(self, message: dict, session_id: str):
        """Broadcast message to all connections in a session"""
        await self.send_personal_message(message, session_id)
    
    async def broadcast(self, message: dict):
        """Broadcast to all connections"""
        for session_id in self.active_connections:
            await self.send_personal_message(message, session_id)