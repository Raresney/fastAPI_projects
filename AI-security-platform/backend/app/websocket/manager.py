import json
from collections import defaultdict
from fastapi import WebSocket


class ConnectionManager:
    def __init__(self):
        self._connections: dict[str, list[WebSocket]] = defaultdict(list)

    async def connect(self, scan_id: str, websocket: WebSocket):
        await websocket.accept()
        self._connections[scan_id].append(websocket)

    def disconnect(self, scan_id: str, websocket: WebSocket):
        self._connections[scan_id].remove(websocket)
        if not self._connections[scan_id]:
            del self._connections[scan_id]

    async def broadcast(self, scan_id: str, data: dict):
        dead = []
        for ws in self._connections.get(scan_id, []):
            try:
                await ws.send_text(json.dumps(data))
            except Exception:
                dead.append(ws)
        for ws in dead:
            self.disconnect(scan_id, ws)


ws_manager = ConnectionManager()
