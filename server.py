from fastapi import FastAPI
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

current_state = "idle"


@app.get("/")
async def home():
    return FileResponse("index.html")


@app.get("/state")
async def state():
    return JSONResponse({"state": current_state})


@app.post("/cmd/idle")
async def idle():
    global current_state
    current_state = "idle"
    return {"ok": True}


@app.post("/cmd/attack")
async def attack():
    global current_state
    current_state = "attack"
    return {"ok": True}


@app.post("/cmd/monitoring")
async def monitoring():
    global current_state
    current_state = "monitoring"
    return {"ok": True}


@app.post("/cmd/secure")
async def secure():
    global current_state
    current_state = "secure"
    return {"ok": True}


@app.post("/cmd/video")
async def video():
    global current_state
    current_state = "video"
    return {"ok": True}


@app.post("/cmd/reset")
async def reset():
    global current_state
    current_state = "reset"
    return {"ok": True}