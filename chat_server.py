"""
リアルタイムチャット同期サーバー
MacBook・スマホ間でチャットを即時同期する。
WebSocketで接続中の全デバイスにメッセージをブロードキャストする。
"""

import json
import uuid
from datetime import datetime, timezone
from dataclasses import dataclass, field, asdict
from typing import Optional

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse

app = FastAPI()

# --- データモデル ---


@dataclass
class Message:
    id: str
    sender: str
    content: str
    timestamp: str
    device: str


@dataclass
class ChatRoom:
    messages: list[Message] = field(default_factory=list)

    def add_message(self, sender: str, content: str, device: str) -> Message:
        msg = Message(
            id=str(uuid.uuid4()),
            sender=sender,
            content=content,
            timestamp=datetime.now(timezone.utc).isoformat(),
            device=device,
        )
        self.messages.append(msg)
        # 直近500件のみ保持
        if len(self.messages) > 500:
            self.messages = self.messages[-500:]
        return msg


# --- コネクション管理 ---


class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, data: dict):
        """全接続デバイスにメッセージを送信"""
        for connection in self.active_connections:
            try:
                await connection.send_json(data)
            except Exception:
                pass


manager = ConnectionManager()
room = ChatRoom()

# --- WebSocketエンドポイント ---


@app.websocket("/ws/{username}")
async def websocket_endpoint(websocket: WebSocket, username: str):
    await manager.connect(websocket)
    # 接続時に既存メッセージ履歴を送信
    await websocket.send_json({
        "type": "history",
        "messages": [asdict(m) for m in room.messages],
    })
    # 入室通知
    await manager.broadcast({
        "type": "system",
        "content": f"{username} が参加しました",
        "timestamp": datetime.now(timezone.utc).isoformat(),
    })
    try:
        while True:
            data = await websocket.receive_json()
            content = data.get("content", "").strip()
            device = data.get("device", "unknown")
            if not content:
                continue
            msg = room.add_message(sender=username, content=content, device=device)
            await manager.broadcast({
                "type": "message",
                **asdict(msg),
            })
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast({
            "type": "system",
            "content": f"{username} が退出しました",
            "timestamp": datetime.now(timezone.utc).isoformat(),
        })


# --- フロントエンド配信 ---


@app.get("/")
async def get():
    return HTMLResponse(CHAT_HTML)


# フロントエンドHTMLは別ファイルから読み込み
import pathlib

_html_path = pathlib.Path(__file__).parent / "chat_frontend.html"


@app.on_event("startup")
async def _load_html():
    global CHAT_HTML
    CHAT_HTML = _html_path.read_text(encoding="utf-8")
