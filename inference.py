import os
import sys
sys.path.insert(0, "src")
from openai import OpenAI
from rubicon_openenv.environment import RubiconEnvironment

API_BASE_URL = os.getenv("API_BASE_URL", "https://router.huggingface.co/v1")
MODEL_NAME = os.getenv("MODEL_NAME", "Qwen/Qwen2.5-72B-Instruct")
API_KEY = os.getenv("HF_TOKEN")
MAX_STEPS = 10
TASKS = ["easy", "medium", "hard"]

client = OpenAI(base_url=API_BASE_URL, api_key=API_KEY)

def get_action(obs, task):
    prompt = f"""You are a security analyst. Investigate this incident and decide what to do.

Current step: {obs.step}
Alerts seen: {obs.alerts}
Belief state: {obs.belief}
Uncertainty: {obs.uncertainty:.2f}
Actions taken: {obs.action_history}
Time remaining: {obs.time_remaining}

Available actions:
- inspect_headers
- analyze_process
- check_network
- review_user_behavior
- escalate_phishing
- escalate_malware
- close_false_positive

Reply with ONLY the action name. Nothing else."""
    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=20,
            temperature=0.3
        )
        action = response.choices[0].message.content.strip().lower()
        valid = ["inspect_headers","analyze_process","check_network",
                 "review_user_behavior","escalate_phishing","escalate_malware","close_false_positive"]
        return action if action in valid else "inspect_headers"
    except Exception as e:
        return "inspect_headers"

def run_task(task_name):
    env = RubiconEnvironment(task=task_name)
    obs = env.reset()
    rewards = []
    print(f"[START] task={task_name} env=rubicon model={MODEL_NAME}")

    for step in range(1, MAX_STEPS + 1):
        action = get_action(obs, task_name)
        obs, reward, done, info = env.step(action)
        
        raw_reward = reward.value
        # Normalize reward to [0, 1] range for better interpretability
        
        norm_reward = max(0.0, min(1.0, (raw_reward + 1.0) / 2.0))
        
        rewards.append(norm_reward)
        
        error = info.get("last_action_error")
        error = error if error else "null"

        print(f"[STEP] step={step} action={action} reward={norm_reward:.2f} done={str(done).lower()} error={error}")
        if done:
            break

    total = sum(rewards)
    score = min(1.0, max(0.0, (total + 1.0) / 2.0))
    success = score >= 0.5
    rewards_str = ",".join(f"{r:.2f}" for r in rewards)
    print(f"[END] success={str(success).lower()} steps={step} score={score:.3f} rewards={rewards_str}")
    return score

if __name__ == "__main__":
    for task in TASKS:
        run_task(task)
