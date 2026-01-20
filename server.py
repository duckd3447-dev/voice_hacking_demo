from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path

app = FastAPI(title="Voice Hacking Demo")

# --- SAFE static mounting ---
STATIC_DIR = Path(__file__).parent / "static"
if STATIC_DIR.exists():
    app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# --- GLOBAL STATE ---
state = {
    "mode": "IDLE",
    "color": "yellow",
    "video": False,
    "message": "System standing by. Awaiting command."
}

# --- MAIN UI ---
@app.get("/", response_class=HTMLResponse)
async def home():
    return f"""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Cybersecurity Voice Attack Demo</title>
<style>
body {{
    margin: 0;
    background: #050505;
    color: #e6e6e6;
    font-family: 'Segoe UI', system-ui, sans-serif;
}}
.container {{
    height: 100vh;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    text-align: center;
}}
h1 {{
    font-size: 3rem;
    letter-spacing: 2px;
}}
.status {{
    margin-top: 20px;
    padding: 20px 40px;
    border-radius: 10px;
    background: rgba(255,255,255,0.05);
    box-shadow: 0 0 40px rgba(255,0,0,0.2);
}}
.mode {{
    font-size: 1.5rem;
    color: {state["color"]};
}}
.message {{
    margin-top: 10px;
    font-size: 1.1rem;
    opacity: 0.9;
}}
.footer {{
    position: absolute;
    bottom: 20px;
    font-size: 0.9rem;
    opacity: 0.6;
}}
</style>
</head>
<body>
<div class="container">
    <h1>VOICE HACKING SIMULATION</h1>
    <div class="status">
        <div class="mode">STATUS: {state["mode"]}</div>
        <div class="message">{state["message"]}</div>
    </div>
    <div class="footer">
        Cybersecurity Awareness Demonstration • Authorized Simulation Only
    </div>
</div>
</body>
</html>
"""

# --- COMMAND API ---
@app.post("/cmd/{action}")
async def command(action: str):
    action = action.upper()

    if action == "START":
        state.update({
            "mode": "ACTIVE THREAT",
            "color": "red",
            "video": False,
            "message": "Unauthorized voice command detected. System integrity compromised."
        })

    elif action in ["RED", "BLUE", "GREEN", "YELLOW"]:
        state["color"] = action.lower()
        state["message"] = f"Environment lighting changed to {action}."

    elif action == "VIDEO":
        state["video"] = True
        state["message"] = "Attack demonstration video initiated."

    elif action == "RESET":
        state.update({
            "mode": "IDLE",
            "color": "yellow",
            "video": False,
            "message": "System secured. Threat neutralized."
        })

    else:
        return JSONResponse({"error": "Unknown command"}, status_code=400)

    return {"status": "ok", "state": state}