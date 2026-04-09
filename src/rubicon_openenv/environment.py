import random

class FraudEnvironment:
    def __init__(self):
        self.max_steps = 10
        self.reset("easy")  
        
    def reset(self, task: str = "easy"):
        self.task = task
        self.step_count = 0
        self.cost = 0.0
        
        # Define the 3 required tasks
        if task == "easy":
            self.scenario = {
                "desc": "Transaction: $5,000. Merchant: Unknown Electronics. IP: Russia (User usually in USA).",
                "truth": "fraud",
                "clue": "IP address matches known botnet."
            }
        elif task == "medium":
            self.scenario = {
                "desc": "Transaction: $45. Merchant: Local Grocery. IP: Unknown VPN.",
                "truth": "legit",
                "clue": "User confirmed via SMS that they are using a VPN today."
            }
        else: # hard
            self.scenario = {
                "desc": "Transaction: 50 charges of $0.99 at App Store within 2 minutes.",
                "truth": "fraud",
                "clue": "Card testing attack signature detected in payment gateway logs."
            }
            
        return {
            "observation": f"New case assigned. {self.scenario['desc']} Available actions: 'investigate', 'freeze_account', 'approve_transaction'.",
            "reward": 0.0,
            "done": False,
            "info": {"cost": self.cost, "steps": self.step_count}
        }

    # ... keep your step() and state() functions exactly the same ...
    def step(self, action_type: str, target: str = ""):
        self.step_count += 1
        done = False
        reward = 0.0
        obs = ""
        
        # Action 1: Gather Information (Costs time/money)
        if action_type == "investigate":
            self.cost += 0.1
            obs = f"Investigation result: {self.scenario['clue']}. (Cost incurred: -0.1)"
        
        # Action 2: Commit (Irreversible)
        elif action_type in ["freeze_account", "approve_transaction"]:
            done = True
            is_correct = (action_type == "freeze_account" and self.scenario["truth"] == "fraud") or \
                         (action_type == "approve_transaction" and self.scenario["truth"] == "legit")
            
            if is_correct:
                # Map 1.0 down to 0.95 to stay below 1.0
                # Subtracting cost ensures a reward gradient (0.05 to 0.95)
                base_success = 0.95
                reward = max(0.05, base_success - self.cost)
                obs = f"Correct decision! The transaction was {self.scenario['truth']}."
            else:
                # Use 0.05 instead of 0.0 to stay above 0.0
                reward = 0.05
                obs = f"Critical Error: Wrong decision. The transaction was {self.scenario['truth']}."
    
        if self.step_count >= self.max_steps:
            done = True
            reward = 0.05  # Changed from 0.0 to 0.05
            obs = "Timeout: Fraudster escaped while you were investigating."

        return {
            "observation": obs,
            "reward": reward,
            "done": done,
            "info": {"cost": self.cost, "steps": self.step_count}
        }

    def state(self):
        return {"task": self.task, "steps": self.step_count, "accumulated_cost": self.cost}