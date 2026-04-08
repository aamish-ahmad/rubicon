import random
import math
from .models import Observation, Action, Reward, State

TASKS = {
    "easy": {
        "ground_truth": "phishing_attack",
        "signals": ["suspicious_email", "phishing_link", "spoofed_sender", "phishing_link", "suspicious_email"]
    },
    "medium": {
        "ground_truth": "malware_execution",
        "signals": ["suspicious_email", "process_anomaly", "network_spike", "process_anomaly", "file_encryption"]
    },
    "hard": {
        "ground_truth": "malware_execution",
        "signals": ["phishing_link", "phishing_link", "spoofed_sender", "process_anomaly", "file_encryption"]
    }
}

VALID_ACTIONS = [
    "inspect_headers", "analyze_process", "check_network",
    "review_user_behavior", "escalate_phishing",
    "escalate_malware", "close_false_positive"
]

COMMIT_ACTIONS = {
    "escalate_phishing": "phishing_attack",
    "escalate_malware": "malware_execution",
    "close_false_positive": "false_positive"
}

class RubiconEnvironment:
    def __init__(self, task: str = "easy"):
        self.task = task
        self.reset()

    # def reset(self):
    #     self.step_count = 0
    #     self.action_history = []
    #     self.committed = False
    #     self.ground_truth = TASKS[self.task]["ground_truth"]
    #     self.signals = TASKS[self.task]["signals"].copy()
    #     self.belief = {"phishing_attack": 0.33, "malware_execution": 0.33, "false_positive": 0.34}
    #     self.wrong_path_steps = 0
    #     self.max_steps = 10
    #     return self._get_obs()
    def reset(self):
        self.current_step = 0
        self.done = False
    # default task (already set in init)
        obs = self._get_observation()
        return obs

    def _entropy(self):
        return -sum(p * math.log(p + 1e-9) for p in self.belief.values())

    def _update_belief(self, action: str):
        signal = self.signals[min(self.step_count, len(self.signals)-1)]
        if action == "inspect_headers" and signal in ["suspicious_email", "spoofed_sender", "phishing_link"]:
            self.belief["phishing_attack"] = min(0.9, self.belief["phishing_attack"] + 0.2)
        elif action == "analyze_process" and signal in ["process_anomaly", "file_encryption"]:
            self.belief["malware_execution"] = min(0.9, self.belief["malware_execution"] + 0.2)
        elif action == "check_network" and signal == "network_spike":
            self.belief["malware_execution"] = min(0.9, self.belief["malware_execution"] + 0.15)
        elif action == "review_user_behavior":
            self.belief["false_positive"] = min(0.9, self.belief["false_positive"] + 0.1)
        total = sum(self.belief.values())
        self.belief = {k: v/total for k, v in self.belief.items()}

    def _get_obs(self):
        visible_signals = self.signals[:min(self.step_count+1, len(self.signals))]
        return Observation(
            step=self.step_count,
            alerts=visible_signals,
            belief=self.belief,
            uncertainty=self._entropy(),
            action_history=self.action_history,
            time_remaining=self.max_steps - self.step_count
        )

    def step(self, action: str):
        if action not in VALID_ACTIONS:
            return self._get_obs(), Reward(value=-0.1, reason="invalid_action"), False, {"error": "invalid action"}

        prev_entropy = self._entropy()
        self._update_belief(action)
        curr_entropy = self._entropy()
        self.action_history.append(action)
        self.step_count += 1

        if action in COMMIT_ACTIONS:
            chosen = COMMIT_ACTIONS[action]
            self.committed = True
            if chosen == self.ground_truth:
                calibration_bonus = min(0.4, len(self.action_history) * 0.05)
                reward = Reward(value=1.0 + calibration_bonus, reason="correct_commit")
            else:
                reward = Reward(value=-0.5, reason="wrong_commit")
            return self._get_obs(), reward, True, {"error": None}

        reward_val = 0.0
        reason = []
        if prev_entropy - curr_entropy > 0.05:
            reward_val += 0.2
            reason.append("informative")
        if action in self.action_history[:-1]:
            reward_val -= 0.3
            reason.append("stagnation")
        if self.step_count > 6:
            reward_val -= 0.05 * (self.step_count - 6)
            reason.append("delay_penalty")
        if not reason:
            reward_val -= 0.1
            reason.append("uninformative")

        done = self.step_count >= self.max_steps
        return self._get_obs(), Reward(value=round(reward_val, 2), reason=",".join(reason)), done, {"error": None}

    def state(self):
        return State(
            step=self.step_count,
            ground_truth=self.ground_truth,
            belief=self.belief,
            committed=self.committed
        )
