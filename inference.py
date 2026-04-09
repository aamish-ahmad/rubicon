import os
import requests
from openai import OpenAI

API_BASE_URL = os.getenv("API_BASE_URL", "https://api.openai.com/v1")
# Check for API_KEY first (hackathon proxy), fallback to OPENAI_API_KEY (local)
API_KEY = os.getenv("API_KEY", os.getenv("OPENAI_API_KEY", "your-key-here"))
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4o-mini")
ENV_URL = "http://localhost:7860"

def log_start(task, env, model):
    print(f"[START] task={task} env={env} model={model}", flush=True)

def log_step(step, action, reward, done, error):
    print(f"[STEP] step={step} action={action} reward={reward} done={done} error={error}", flush=True)

def log_end(success, steps, score, rewards):
    print(f"[END] success={success} steps={steps} score={score} rewards={rewards}", flush=True)

def main():
    client = OpenAI(base_url=API_BASE_URL, api_key=API_KEY)
    
    tasks = ["easy", "medium", "hard"]
    
    for task in tasks:
        log_start(task=task, env="rubicon-fraud-analyst", model=MODEL_NAME)
        
        # Reset Env
        res = requests.post(f"{ENV_URL}/reset", json={"task": task}).json()
        obs = res.get("observation", "")
        
        done = False
        step = 0
        rewards = []
        score = 0.0
        
        while not done and step < 5:
            step += 1
            
            # Ask LLM what to do
            prompt = f"You are a fraud analyst. Observation: {obs}. Should you 'investigate', 'freeze_account', or 'approve_transaction'? Reply with ONLY the action word."
            
            try:
                completion = client.chat.completions.create(
                    model=MODEL_NAME,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.0
                )
                action = completion.choices[0].message.content.strip().lower()
            except Exception as e:
                action = "investigate"
                
            # Clean up action formatting for safety
            if "freeze" in action: action = "freeze_account"
            elif "approve" in action: action = "approve_transaction"
            else: action = "investigate"
            
            # Step Env
            step_res = requests.post(f"{ENV_URL}/step", json={"action": {"action_type": action}}).json()
            obs = step_res.get("observation", "")
            reward = step_res.get("reward", 0.0)
            done = step_res.get("done", False)
            
            rewards.append(reward)
            log_step(step=step, action=action, reward=reward, done=done, error=None)
            
            if done:
                score = reward # Grader gives final score in the last reward
                break
                
        success = score >= 0.5
        log_end(success=success, steps=step, score=score, rewards=rewards)

if __name__ == "__main__":
    main()