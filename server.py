from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import PlainTextResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI()

clients = set()

# Serve index.html + video + assets
app.mount("/", StaticFiles(directory=".", html=True), name="static")

@app.websocket("/ws")
async def websocket_endpoint(ws: WebSocket):
    await ws.accept()
    clients.add(ws)
    try:
        while True:
            await ws.receive_text()
    except WebSocketDisconnect:
        clients.remove(ws)

async def broadcast(cmd: str):
    for ws in list(clients):
        try:
            await ws.send_text(cmd)
        except:
            clients.remove(ws)

@app.post("/cmd/{command}")
async def send_command(command: str):
    await broadcast(command.upper())
    return PlainTextResponse(f"OK: {command}")