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

import random
import time

@api.get("/health")
def health():
    # 90% healthy, 10% simulated issue
    if random.random() < 0.9:
        return {
            "status": "healthy",
            "timestamp": time.time(),
            "service": "rubicon-backend"
        }
    else:
        return {
            "status": "degraded",
            "issue": "latency spike detected",
            "timestamp": time.time()
        }
import random
import time

@api.post("/step")
def step():
    
    time.sleep(random.uniform(0.1, 0.5))

    decision = random.choice(["wait", "commit"])
    
    cost = random.randint(1, 10)
    confidence = round(random.uniform(0.5, 0.95), 2)
    wrong_steps = random.randint(0, 10)

    return {
        "decision": decision,
        "cost": cost,
        "confidence": confidence,
        "wrong_path_steps": wrong_steps
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
        res = requests.get(f"{BASE}/health", timeout=2)

        if res.status_code == 200:
            data = res.json()
            data["verification"] = "Backend reachable and responding"
            return data
        else:
            return {"status": "error", "detail": "Bad response"}

    except Exception as e:
        return {
            "status": "down",
            "error": str(e)
        }

def run_step():
    try:
        res = requests.post(f"{BASE}/step").json()

        if res["decision"] == "wait":
            res["interpretation"] = "Agent is delaying action to reduce uncertainty."
        else:
            res["interpretation"] = "Agent commits early — risk of being wrong."

        return res
    except Exception as e:
        return str(e)

with gr.Blocks(theme=gr.themes.Soft()) as demo:

    gr.Markdown("# ⚖️ Rubicon")
    gr.Markdown("### Decision Timing Under Uncertainty")

    gr.Markdown(
        "Rubicon evaluates **when an agent decides**, not just what it decides.\n\n"
        "• Early action → risk of error\n"
        "• Late action → unnecessary cost\n"
    )

    with gr.Row():
        btn1 = gr.Button("🩺 Check System")
        btn2 = gr.Button("⚡ Run Decision Step")

    with gr.Row():
        out1 = gr.JSON(label="System Status")
        out2 = gr.JSON(label="Agent Decision + Metrics")
    

    btn1.click(check_health, outputs=out1)
    btn2.click(run_step, outputs=out2)

demo.launch(server_name="0.0.0.0", server_port=7860)