# Rubicon

Every decision has two properties most benchmarks ignore:

1. It happens at a specific moment in time
2. Some decisions cannot be undone

Rubicon is an environment that measures both.

## The Gap

Current AI benchmarks ask: did the agent get it right?

They do not ask:
- Did it act too early, before enough evidence?
- Did it wait too long, accumulating unnecessary cost?
- Did it treat an irreversible decision with the same weight as a reversible one?

These questions matter in every high-stakes domain. Rubicon is built to answer them.

## How It Works

An agent operates in a partially observable environment.

At each step it chooses to either:
- **Gather information** — reduce uncertainty, but time passes
- **Commit** — make a final irreversible decision and end the episode

The environment tracks not just whether the agent was right — but when it decided, how long it stayed wrong, and what that cost.

## What Gets Measured

| Metric | What it captures |
|---|---|
| `wrong_path_steps` | Time spent committed to an incorrect hypothesis |
| `commitment_calibration` | Evidence depth at the moment of irreversible action |
| `accumulated_wrong_cost` | Total cost incurred while wrong |

These metrics exist because two agents can score identically on accuracy while one causes significantly more real-world damage than the other.

## Tasks

| Difficulty | Signal Quality | What it tests |
|---|---|---|
| Easy | Clear, unambiguous | Can the agent act decisively when it should? |
| Medium | Two plausible hypotheses | Can it eliminate the wrong one before committing? |
| Hard | First signals actively mislead | Can it resist a compelling but incorrect early commit? |

## Try It

Live environment with interactive UI:

https://aamish-ahmad-rubicon.hf.space/ui

```bash
git clone https://github.com/aamish-ahmad/rubicon
cd rubicon
pip install fastapi uvicorn pydantic openai gradio
python app.py
```

## Built For

Any domain where decisions are time-sensitive and partially irreversible:

- Medical diagnosis — treat now or run more tests?
- Fraud detection — block the transaction or gather more signals?
- Incident response — escalate now or investigate further?
- Autonomous systems — act on partial information or wait?

Rubicon provides the evaluation infrastructure to measure agent behavior across all of these.
