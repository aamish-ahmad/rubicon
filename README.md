# Rubicon

When should an agent stop gathering information and act?

Act too early → irreversible mistake  
Wait too long → cost already incurred  

**Rubicon measures this.**

---

## What It Is

Rubicon is a decision-making environment where agents are evaluated not just on *what* they decide — but *when* they decide it.

---

## The Problem

Most AI systems optimize for final accuracy.

They ignore what happens before the final answer:
- how long the agent stays wrong
- when it commits to a decision
- the cost of delayed or premature actions

Two agents can have the same accuracy — but very different real-world impact.

Rubicon makes this visible.

---

## Behavioral Difference

Example difference between two agents:

|                | Agent A | Agent B |
|----------------|--------|--------|
| Accuracy       | similar | similar |
| wrong_path_steps | high | low |
| accumulated_cost | high | low |

Both agents may reach similar final answers.

But one spends significantly longer in incorrect reasoning states.

This difference is invisible to standard evaluation.

Rubicon captures it.

---

## How It Works

An agent interacts with a partially observable environment.

At each step, it can:
- gather information (investigation actions)
- commit to a decision (irreversible)

The agent must balance:
- uncertainty (incomplete information)
- time cost (waiting too long is expensive)
- risk (committing too early can be wrong)

Once a decision is made, the episode ends.

---

## Features

- behavioral evaluation (not just accuracy)
- cost-aware decision tracking
- simple HTTP API
- lightweight environment
- easy integration with agents

---

## Prerequisites

- Python 3.9+
- pip

---

## Run Locally

```bash
git clone https://github.com/aamish-ahmad/rubicon.git
cd rubicon/rubicon-openenv
pip install -r requirements.txt
uvicorn app:app --host 0.0.0.0 --port 7860