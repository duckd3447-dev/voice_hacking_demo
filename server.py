from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# Serve static files
app.mount("/static", StaticFiles(directory="static"), name="static")

clients = set()

@app.get("/")
async def index():
    return FileResponse("index.html")

@app.websocket("/ws")
async def websocket_endpoint(ws: WebSocket):
    await ws.accept()
    clients.add(ws)
    try:
        while True:
            await ws.receive_text()
    except WebSocketDisconnect:
        clients.remove(ws)

async def broadcast(message: str):
    for ws in list(clients):
        try:
            await ws.send_text(message)
        except:
            clients.remove(ws)

@app.post("/cmd/{command}")
async def command(command: str):
    await broadcast(command.upper())
    return {"status": "ok", "command": command}