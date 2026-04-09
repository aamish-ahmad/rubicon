from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
import sys
import os
import gradio as gr

# 1. Connect to your real logic
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))
from rubicon_openenv.environment import FraudEnvironment

api = FastAPI()
env = FraudEnvironment()

# ==========================================
# 2. BULLETPROOF FASTAPI ENDPOINTS
# ==========================================
@api.post("/reset")
async def reset_env(request: Request):
    # This prevents the 422 error. If the bot sends an empty request, it safely defaults to {}.
    try:
        payload = await request.json()
    except Exception:
        payload = {}
        
    task = payload.get("task", "easy") if payload else "easy"
    return env.reset(task)

@api.post("/step")
async def step_env(request: Request):
    try:
        payload = await request.json()
    except Exception:
        payload = {}
        
    action = "investigate"
    if payload and "action" in payload:
        if isinstance(payload["action"], dict):
            action = payload["action"].get("action_type", "investigate")
        else:
            action = payload["action"]
            
    return env.step(action)

@api.get("/health")
async def health():
    return {"status": "healthy"}

@api.get("/state")
async def get_state():
    return env.state()

@api.get("/")
async def root():
    return RedirectResponse(url="/ui")

# ==========================================
# 3. GRADIO FRONTEND (mounted at /ui to avoid route conflicts)
# ==========================================
def check_health():
    return "✅ System Healthy: Backend and Logic are connected."

def run_step_ui(action_choice):
    return str(env.step(action_choice))

def reset_ui(task_choice):
    return str(env.reset(task_choice))

with gr.Blocks() as demo:
    gr.Markdown("# ⚖️ Rubicon: Decision Timing Environment")
    
    with gr.Row():
        btn_health = gr.Button("🩺 Check System")
        task_dropdown = gr.Dropdown(["easy", "medium", "hard"], label="Task Difficulty", value="medium")
        btn_reset = gr.Button("🔄 Reset Env")
        
    with gr.Row():
        action_dropdown = gr.Dropdown(["investigate", "freeze_account", "approve_transaction"], label="Take Action", value="investigate")
        btn_step = gr.Button("⚡ Execute Action")

    out_box = gr.Textbox(label="Environment Response", lines=5)
        
    btn_health.click(check_health, outputs=out_box)
    btn_reset.click(reset_ui, inputs=task_dropdown, outputs=out_box)
    btn_step.click(run_step_ui, inputs=action_dropdown, outputs=out_box)

app = gr.mount_gradio_app(api, demo, path="/ui", theme=gr.themes.Soft())
def main():
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=7860)

if __name__ == "__main__":
    main()
