from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import FileResponse

app = FastAPI()
clients = []

# ---------------- SERVE UI ----------------
@app.get("/")
async def index():
    return FileResponse("index.html")

# ---------------- WEBSOCKET ----------------
@app.websocket("/ws")
async def websocket_endpoint(ws: WebSocket):
    await ws.accept()
    clients.append(ws)
    print("🟢 Client connected")

    try:
        while True:
            await ws.receive_text()
    except WebSocketDisconnect:
        clients.remove(ws)
        print("🔴 Client disconnected")


