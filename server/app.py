from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
import sys
sys.path.insert(0, "src")
from rubicon_openenv.environment import RubiconEnvironment

app = FastAPI()
envs = {
    "easy": RubiconEnvironment("easy"),
    "medium": RubiconEnvironment("medium"),
    "hard": RubiconEnvironment("hard")
}

class ResetRequest(BaseModel):
    event_id: Optional[str] = None
    task: Optional[str] = "easy"

class ActionRequest(BaseModel):
    event_id: Optional[str] = None
    action_type: str
    task: Optional[str] = "easy"

@app.post("/reset")
def reset(req: ResetRequest):
    task = req.task or "easy"
    obs = envs[task].reset()
    return obs.model_dump()

@app.post("/step")
def step(req: ActionRequest):
    task = req.task or "easy"
    obs, reward, done, info = envs[task].step(req.action_type)
    return {"observation": obs.model_dump(), "reward": reward.model_dump(), "done": done, "info": info}

@app.get("/state")
def state(task: str = "easy"):
    return envs[task].state().model_dump()

@app.get("/health")
def health():
    return {"status": "healthy"}

def main():
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=7860)

if __name__ == "__main__":
    main()
