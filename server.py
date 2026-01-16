from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import FileResponse
import speech_recognition as sr
import threading
import asyncio
import time

app = FastAPI()
clients = []
event_loop = None

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

# ---------------- BROADCAST ----------------
async def _broadcast(cmd: str):
    for ws in clients:
        await ws.send_text(cmd)

def broadcast(cmd: str):
    if event_loop:
        asyncio.run_coroutine_threadsafe(_broadcast(cmd), event_loop)

# ---------------- VOICE ----------------
def voice_server():
    r = sr.Recognizer()
    mic = sr.Microphone()

    with mic as source:
        r.adjust_for_ambient_noise(source)
        print("🎤 Mic calibrated")

    while True:
        try:
            with mic as source:
                print("🎙 Listening...")
                audio = r.listen(source, phrase_time_limit=4)

            text = r.recognize_google(audio).lower()
            print("🧠 Recognized:", text)

            if "start demo" in text:
                broadcast("START_DEMO")

            elif "make screen green" in text or "green" in text:
                broadcast("GREEN")

            elif "make screen blue" in text or "blue" in text:
                broadcast("BLUE")

            elif "reset demo" in text or "reset" in text:
                broadcast("RESET")

        except:
            pass

        time.sleep(0.5)

# ---------------- STARTUP ----------------
@app.on_event("startup")
async def startup():
    global event_loop
    event_loop = asyncio.get_running_loop()
    threading.Thread(target=voice_server, daemon=True).start()


