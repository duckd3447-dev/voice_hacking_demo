from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Allow browser access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve UI
@app.get("/")
def home():
    return FileResponse("index.html")

# COMMAND API
@app.get("/command/{cmd}")
def command(cmd: str):
    print("Received command:", cmd)
    return {
        "status": "ok",
        "command": cmd
    }