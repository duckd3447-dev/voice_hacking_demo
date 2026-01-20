from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import FileResponse, PlainTextResponse
import asyncio

app = FastAPI()

# Store connected UI clients
clients = set()

# ---------------- UI ----------------
@app.get("/")
async def index():
    return FileResponse("index.html")

# ---------------- WEBSOCKET ----------------
@app.websocket("/ws")
async def websocket_endpoint(ws: WebSocket):
    await ws.accept()
    clients.add(ws)
    print("🟢 UI connected")

    try:
        while True:
            await ws.receive_text()  # keep alive
    except WebSocketDisconnect:
        clients.remove(ws)
        print("🔴 UI disconnected")

# ---------------- BROADCAST ----------------
async def broadcast(cmd: str):
    dead = []
    for ws in clients:
        try:
            await ws.send_text(cmd)
        except:
            dead.append(ws)
    for ws in dead:
        clients.remove(ws)

# ---------------- COMMAND API ----------------
@app.post("/cmd/{command}")
async def send_command(command: str):
    cmd = command.upper()
    await broadcast(cmd)
    return PlainTextResponse(f"OK: {cmd}")


