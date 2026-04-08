# Rubicon

When should an agent stop gathering information and act?

Act too early → irreversible mistake  
Wait too long → cost already incurred  

Rubicon measures this.

## What It Is

A decision-making environment where agents are evaluated not just on *what* they decide — but *when* they decide it.

## The Problem

Most AI systems optimize for final accuracy.

They ignore what happens before the final answer:
- How long the agent stays wrong
- When it commits to a decision
- The cost of delayed or premature actions

Two agents can have the same accuracy — but very different real-world impact.

Rubicon makes this visible.

## Behavioral Difference

Example behavior difference between two agents:

| | Agent A | Agent B |
|---|---|---|
| Accuracy | similar | similar |
| wrong_path_steps | high | low |
| accumulated_cost | high | low |

Both agents may reach similar final answers.

But one spends significantly longer in incorrect reasoning states.

This difference is invisible to standard accuracy-based evaluation.

Rubicon is designed to capture it.

