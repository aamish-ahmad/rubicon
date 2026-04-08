import threading
import time
import requests

from fastapi import FastAPI
import uvicorn
import gradio as gr

# ------------------------
# FASTAPI BACKEND
# ------------------------

api = FastAPI()

@api.get("/health")
def health():
    return {"status": "healthy"}

@api.post("/step")
def step():
    return {
        "decision": "wait",
        "cost": 3,
        "confidence": 0.62,
        "wrong_path_steps": 5
    }

def run_api():
    uvicorn.run(api, host="0.0.0.0", port=8000)

# Start backend in background thread
threading.Thread(target=run_api, daemon=True).start()

# Give server time to start
time.sleep(2)

# ------------------------
# GRADIO UI
# ------------------------

BASE = "http://localhost:8000"

def check_health():
    try:
        return requests.get(f"{BASE}/health").json()
    except Exception as e:
        return str(e)

def run_step():
    try:
        return requests.post(f"{BASE}/step").json()
    except Exception as e:
        return str(e)

with gr.Blocks() as demo:
    gr.Markdown("# ⚖️ Rubicon")
    gr.Markdown("Evaluate when an agent decides — not just what it decides.")

    btn1 = gr.Button("Check Health")
    out1 = gr.JSON()

    btn2 = gr.Button("Run Step")
    out2 = gr.JSON()

    btn1.click(check_health, outputs=out1)
    btn2.click(run_step, outputs=out2)

demo.launch(server_name="0.0.0.0", server_port=7860)