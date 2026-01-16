from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import FileResponse

app = FastAPI()
clients = []

@app.get("/")
async def index():
    return FileResponse("index.html")

@app.websocket("/ws")
async def websocket_endpoint(ws: WebSocket):
    await ws.accept()
    clients.append(ws)

    try:
        while True:
            msg = await ws.receive_text()
            for c in clients:
                await c.send_text(msg)
    except WebSocketDisconnect:
        clients.remove(ws)


