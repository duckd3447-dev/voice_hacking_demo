from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

clients = set()
current_state = "idle"


@app.get("/")
async def home():
    return FileResponse("index.html")


@app.websocket("/ws")
async def websocket_endpoint(ws: WebSocket):
    await ws.accept()
    clients.add(ws)
    await ws.send_text(current_state)
    try:
        while True:
            await ws.receive_text()
    except WebSocketDisconnect:
        clients.remove(ws)


async def broadcast(state: str):
    global current_state
    current_state = state
    for ws in list(clients):
        await ws.send_text(state)


@app.post("/cmd/idle")
async def idle():
    await broadcast("idle")
    return {"ok": True}


@app.post("/cmd/attack")
async def attack():
    await broadcast("attack")
    return {"ok": True}


@app.post("/cmd/monitoring")
async def monitoring():
    await broadcast("monitoring")
    return {"ok": True}


@app.post("/cmd/secure")
async def secure():
    await broadcast("secure")
    return {"ok": True}


@app.post("/cmd/video")
async def video():
    await broadcast("video")
    return {"ok": True}


@app.post("/cmd/reset")
async def reset():
    await broadcast("reset")
    return {"ok": True}