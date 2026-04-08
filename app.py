from fastapi import FastAPI
from typing import Optional, Dict, Any
import sys
import os
import gradio as gr

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))
from rubicon_openenv.environment import FraudEnvironment

# Initialize API and Environment
api = FastAPI()
env = FraudEnvironment()

# ==========================================
# 1. FASTAPI ENDPOINTS (For Scaler Auto-Grader)
# ==========================================

@api.post("/reset")
async def reset_env(payload: Optional[Dict[str, Any]] = None):
    task = "easy"
    if payload and "task" in payload:
        task = payload["task"]
    return env.reset(task)

@api.post("/step")
async def step_env(payload: Optional[Dict[str, Any]] = None):
    action_type = "investigate"
    if payload and "action" in payload:
        if isinstance(payload["action"], dict):
            action_type = payload["action"].get("action_type", "investigate")
        else:
            action_type = payload["action"]
            
    return env.step(action_type)

@api.get("/state")
async def get_state():
    return env.state()

@api.get("/health")
async def health():
    return {"status": "healthy"}

# ==========================================
# 2. GRADIO FRONTEND (For your Portfolio)
# ==========================================

def check_system():
    return {"status": "healthy", "verification": "Backend reachable and responding"}

def run_step_ui(action_choice):
    # Call the environment directly for the UI
    res = env.step(action_choice)
    return res

def reset_ui(task_choice):
    res = env.reset(task_choice)
    return res

with gr.Blocks(theme=gr.themes.Soft()) as demo:
    gr.Markdown("# ⚖️ Rubicon: Financial Fraud Analyst")
    gr.Markdown("### Decision Timing Under Uncertainty")
    gr.Markdown("Agent must balance the cost of gathering information against the risk of making a wrong, irreversible decision.")
    
    with gr.Row():
        btn_health = gr.Button("🩺 Check System")
        task_dropdown = gr.Dropdown(["easy", "medium", "hard"], label="Select Task", value="easy")
        btn_reset = gr.Button("🔄 Reset Environment")
        
    with gr.Row():
        action_dropdown = gr.Dropdown(["investigate", "freeze_account", "approve_transaction"], label="Take Action", value="investigate")
        btn_step = gr.Button("⚡ Run Decision Step")

    with gr.Row():
        out_system = gr.JSON(label="System Status / Reset Info")
        out_env = gr.JSON(label="Environment Response (Observation, Reward, Done)")
        
    btn_health.click(check_system, outputs=out_system)
    btn_reset.click(reset_ui, inputs=task_dropdown, outputs=out_system)
    btn_step.click(run_step_ui, inputs=action_dropdown, outputs=out_env)

# Mount the Gradio app onto the FastAPI app
app = gr.mount_gradio_app(api, demo, path="/")