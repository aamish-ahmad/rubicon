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

    # Execute step
    response = env.step(action)

    # --- FIRST PRINCIPLES FIX: SCALER RANGE COMPLIANCE ---
    if isinstance(response, dict) and "reward" in response:
        # Force reward strictly between (0.05, 0.95)
        response["reward"] = max(0.05, min(0.95, float(response["reward"])))
    # -----------------------------------------------------

    return response

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
# 3. GRADIO FRONTEND
# ==========================================

DIFFICULTY_DESCRIPTIONS = {
    "easy":   "A high-value transaction from an unusual location — strong early signals.",
    "medium": "A low-value everyday purchase with a privacy tool — ambiguous situation.",
    "hard":   "Dozens of micro-charges in seconds — subtle, adversarial pattern.",
}

def parse_observation(obs: str) -> dict:
    """
    Extract structured fields from the flat observation string
    returned by FraudEnvironment, without modifying the environment.
    """
    obs = obs.strip()
    # Detect initial case assignment
    if obs.startswith("New case assigned."):
        # Strip the actions suffix for cleaner display
        desc = obs.replace("New case assigned.", "").strip()
        # Remove the actions hint appended by the environment
        if "Available actions:" in desc:
            desc = desc[:desc.index("Available actions:")].strip()
        return {"type": "case", "text": desc}

    # Investigation result
    if obs.startswith("Investigation result:"):
        clue = obs.replace("Investigation result:", "").strip()
        # Strip cost note
        if "(Cost incurred:" in clue:
            clue = clue[:clue.index("(Cost incurred:")].strip()
        return {"type": "investigate", "text": clue}

    # Terminal outcomes
    if obs.startswith("Correct decision"):
        return {"type": "correct", "text": obs}
    if obs.startswith("Critical Error"):
        return {"type": "error", "text": obs}
    if obs.startswith("Timeout"):
        return {"type": "timeout", "text": obs}

    return {"type": "other", "text": obs}


def build_case_md(task: str, obs_parsed: dict, info: dict) -> str:
    difficulty_label = task.capitalize()
    difficulty_desc = DIFFICULTY_DESCRIPTIONS.get(task, "")
    case_text = obs_parsed.get("text", "")

    cost_display = f"{info.get('cost', 0.0):.1f}"
    steps_display = str(info.get("steps", 0))

    md = f"""
**Difficulty:** {difficulty_label} — {difficulty_desc}

---

**Current Case**

{case_text}

---

**Evidence Steps Taken:** {steps_display} &nbsp;&nbsp;|&nbsp;&nbsp; **Investigation Cost:** {cost_display}
"""
    return md.strip()


def build_evidence_md(clue_text: str, info: dict) -> str:
    cost_display = f"{info.get('cost', 0.0):.1f}"
    steps_display = str(info.get("steps", 0))
    return f"""**New Evidence**

{clue_text}

**Evidence Steps Taken:** {steps_display} &nbsp;&nbsp;|&nbsp;&nbsp; **Investigation Cost:** {cost_display}
""".strip()


def build_terminal_md(action: str, obs_parsed: dict, info: dict) -> str:
    action_label = {
        "freeze_account":      "Freeze Account",
        "approve_transaction": "Approve Transaction",
    }.get(action, action)

    outcome_type = obs_parsed["type"]
    outcome_text = obs_parsed["text"]

    if outcome_type == "correct":
        outcome_emoji = "✅ Correct"
    elif outcome_type == "error":
        outcome_emoji = "❌ Wrong"
    else:
        outcome_emoji = "⏱️ Timeout"

    cost_display = f"{info.get('cost', 0.0):.1f}"
    step_count = int(info.get("steps", 0))
    if action in ("freeze_account", "approve_transaction"):
        evidence_steps = max(step_count - 1, 0)
    else:
        evidence_steps = step_count
    steps_display = str(evidence_steps)

    return f"""### Episode Complete

| Field | Value |
|---|---|
| **Decision** | {action_label} |
| **Outcome** | {outcome_emoji} |
| **Evidence gathered** | {steps_display} step(s) |
| **Investigation cost** | {cost_display} |

_{outcome_text}_
""".strip()


def run_step_ui(action: str):
    res = env.step(action)
    done = bool(res.get("done"))
    info = res.get("info", {})
    obs_parsed = parse_observation(res.get("observation", ""))

    if done:
        main_md = build_terminal_md(action, obs_parsed, info)
        status_md = "**Episode complete.** Start a new case to continue."
    else:
        # investigate path
        main_md = build_evidence_md(obs_parsed.get("text", ""), info)
        status_md = "Evidence gathered. You may investigate further or make a final decision."

    interactive = not done
    return (
        main_md,
        status_md,
        gr.update(interactive=interactive),
        gr.update(interactive=interactive),
        gr.update(interactive=interactive),
    )


def reset_ui(task_choice):
    res = env.reset(task_choice)
    info = res.get("info", {})
    obs_parsed = parse_observation(res.get("observation", ""))

    main_md = build_case_md(task_choice, obs_parsed, info)
    status_md = "Review the case, gather evidence if needed, then make one irreversible decision."

    return (
        main_md,
        status_md,
        gr.update(interactive=True),
        gr.update(interactive=True),
        gr.update(interactive=True),
    )


# ==========================================
# 4. UI LAYOUT
# ==========================================
CSS = """
.point-of-no-return {
    border: 2px solid #e53e3e;
    border-radius: 10px;
    padding: 16px 20px;
    background: linear-gradient(135deg, #fff5f5 0%, #fed7d7 100%);
    margin-top: 8px;
}
.ponr-label {
    color: #c53030;
    font-weight: 800;
    letter-spacing: 0.12em;
    font-size: 0.85rem;
    text-transform: uppercase;
    margin-bottom: 4px;
}
"""

with gr.Blocks(
    title="Rubicon — Irreversible Decision Timing",
    theme=gr.themes.Soft(),
    css=CSS,
) as demo:

    # ── Header ──────────────────────────────────────────────────────────────
    gr.Markdown("""
# Rubicon — Irreversible Decision Timing

**How much evidence should an AI system gather before making a decision it cannot undo?**
""")

    # ── Controls ────────────────────────────────────────────────────────────
    with gr.Row():
        task_dropdown = gr.Dropdown(
            choices=["easy", "medium", "hard"],
            label="Difficulty",
            value="medium",
            scale=1,
        )
        btn_reset = gr.Button("▶ Start New Case", variant="primary", scale=2)

    # ── Main output area ─────────────────────────────────────────────────────
    out_box = gr.Markdown("*Start a new case to begin.*")

    # ── Evidence action ──────────────────────────────────────────────────────
    btn_investigate = gr.Button(
        "🔍 Gather More Evidence  (adds investigation cost)",
        interactive=False,
    )

    # ── Point of No Return section ───────────────────────────────────────────
    with gr.Group(elem_classes=["point-of-no-return"]):
        gr.Markdown('<div class="ponr-label">⛔ Point of No Return</div>', sanitize_html=False)
        gr.Markdown('Either action below is **irreversible** and ends the episode.')
        with gr.Row():
            btn_freeze = gr.Button(
                "🔒 Freeze Account",
                variant="stop",
                interactive=False,
            )
            btn_approve = gr.Button(
                "✅ Approve Transaction",
                variant="secondary",
                interactive=False,
            )

    # ── Status bar ───────────────────────────────────────────────────────────
    episode_status = gr.Markdown("*Start a new case to begin.*")

    # ── Wire up events ───────────────────────────────────────────────────────
    OUTPUTS = [out_box, episode_status, btn_investigate, btn_freeze, btn_approve]

    btn_reset.click(reset_ui, inputs=task_dropdown, outputs=OUTPUTS)
    btn_investigate.click(lambda: run_step_ui("investigate"), outputs=OUTPUTS)
    btn_freeze.click(lambda: run_step_ui("freeze_account"), outputs=OUTPUTS)
    btn_approve.click(lambda: run_step_ui("approve_transaction"), outputs=OUTPUTS)

app = gr.mount_gradio_app(api, demo, path="/ui")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=7860)