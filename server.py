from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import FileResponse, PlainTextResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# Serve static files (video)
app.mount("/static", StaticFiles(directory="static"), name="static")

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
    try:
        while True:
            await ws.receive_text()
    except WebSocketDisconnect:
        clients.remove(ws)

# ---------------- BROADCAST ----------------
async def broadcast(message: str):
    dead = []
    for ws in clients:
        try:
            await ws.send_text(message)
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