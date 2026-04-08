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
        res = requests.post(f"{BASE}/step").json()
        res["interpretation"] = (
            "Agent chose to WAIT → gathering more info before committing."
        )
        return res
    except Exception as e:
        return str(e)

with gr.Blocks() as demo:
    gr.Markdown("# ⚖️ Rubicon")
    gr.Markdown("### When should an agent act vs wait?")

    gr.Markdown(
        "Rubicon evaluates decision timing — not just accuracy.\n\n"
        "- Acting too early → wrong decision\n"
        "- Waiting too long → unnecessary cost\n"
    )

    with gr.Row():
        btn1 = gr.Button("Check System Health")
        btn2 = gr.Button("Simulate Decision Step")

    out1 = gr.JSON(label="System Status")
    out2 = gr.JSON(label="Agent Decision Output")

    btn1.click(check_health, outputs=out1)
    btn2.click(run_step, outputs=out2)

demo.launch(server_name="0.0.0.0", server_port=7860)