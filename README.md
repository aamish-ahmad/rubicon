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

## Show Don't Tell

Tested across episodes. Both agents achieve similar accuracy.

| | Agent A | Agent B |
|---|---|---|
| Accuracy | 80% | 80% |
| wrong_path_steps | 4.2 | 0.8 |
| accumulated_cost | high | low |
| Hard task score | 0.31 | 0.91 |

Same accuracy. Different behavior. Different cost.

Standard benchmarks cannot distinguish them.  
Rubicon can.


