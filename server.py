from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import FileResponse, PlainTextResponse

app = FastAPI()

clients = set()

@app.get("/")
async def index():
    return FileResponse("index.html")

@app.websocket("/ws")
async def websocket_endpoint(ws: WebSocket):
    await ws.accept()
    clients.add(ws)
    print("🟢 UI connected")

    try:
        while True:
            await ws.receive_text()
    except WebSocketDisconnect:
        clients.remove(ws)
        print("🔴 UI disconnected")

async def broadcast(cmd: str):
    dead = []
    for ws in clients:
        try:
            await ws.send_text(cmd)
        except:
            dead.append(ws)
    for ws in dead:
        clients.remove(ws)

@app.post("/cmd/{command}")
async def send_command(command: str):
    cmd = command.upper()
    await broadcast(cmd)
    return PlainTextResponse(f"OK: {cmd}")