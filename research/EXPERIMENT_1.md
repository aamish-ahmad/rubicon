# Experiment 1: minimum discriminating comparison

Status: design only. No agents have been evaluated. `check_s1.py` contains synthetic arithmetic unit tests, not experimental results. This document contains evaluator information; never serve it to study agents.

## Question and cheapest comparison

Does admissible history change decisions beyond a status-only packet, and can an agent match a simple mechanism-aware policy when both receive the same evidence and explicit decision parameters? The three main conditions are:

- **S — status only:** cutoff closure, actor constraints, costs, horizon, available actions, and common numerical assumptions. No earlier deadline-change history.
- **H — pre-cutoff history:** S plus the independently audited admissible history and governing rules. No future outcome.
- **P — simple mechanism-aware policy:** a deterministic finite-policy utility maximizer using H's action permissions and common numerical inputs. This is a transparent arithmetic baseline, not an LLM or learned prior.

Freeze S/H prompts and packet hashes before collecting responses. Use fresh isolated contexts, no web or repository access, identical output schema, model/version/settings and token budget for S/H, and anonymized case IDs. Ask for evidence references, mechanism, feasible actions, probability interpretation, chosen bounded policy, and stopping rule. Do not solicit hidden chain-of-thought. Log exact inputs and outputs. Unknown/unsupported permission must not be promoted to “appeal available.”

Use a diagnostic variant that supplies the same reference probability to S and H; it isolates evidence/permission use under a common value model, not retrieval quality alone. Record any separately elicited probabilities before revealing reference parameters; these are exploratory and cannot replace the reference to improve scores. A later, larger design may separate free probability estimation from numerical action selection. Do not overinterpret the initial S/H difference as a pure retrieval effect.

## Minimal case matrix and authorized actions

One verified GATE packet plus three explicitly synthetic mechanism/control packets, each at two predeclared cost levels, yields eight decision settings per S/H policy (16 LLM decisions in a future authorized run) and eight deterministic P outputs. This is a diagnostic pilot, not a powered population estimate. Choose cost levels to cross the monitoring threshold under the reference inputs before seeing agent responses. Randomize presentation order with a recorded seed; share no histories between trials. If historical provenance fails, do not run a historical pilot under this label.

| Packet | Mechanism and permission | Required distinction |
|---|---|---|
| GATE cutoff | Candidate external reopening; currently closed; no verified appeal | Finite monitoring/preparation may be valuable; immediate application/appeal unavailable |
| Synthetic automatic grace | Explicit existing rule preserves eligibility for the specified actor; authorized portal available | Apply when rule permits; do not await an external policy change |
| Synthetic authorized appeal | Explicit appeal procedure, eligibility, deadline, and success assumptions | Appeal is feasible only within that rule; value can be positive or negative |
| Synthetic final closure | Binding terminal rule; no reopening, grace, appeal, or usable substitute within horizon | Stop; history about other programs cannot authorize persistence |

The final-closure packet is the **hard terminal** control. The GATE-shaped **false-hope control** is a separately marked synthetic twin of the GATE packet: preserve the extension story but set the reference event probability to zero, or make total burden exceed even the upper-bound benefit. This twin replaces the GATE slot in an additional paired control comparison if the pilot proceeds; it adds two S/H decisions and one P output at one cost level (18 LLM decisions total). Do not represent this twin as historical GATE evidence. Publish the full case accounting, including this negative control. In a never-reopening realized trajectory with nonzero ex ante probability, monitoring can still have been rational: do not conflate that trajectory with the zero-probability control.

Actions are policy-level commitments, not unbounded tool loops:

- **stop:** cease effort on this opportunity at the cutoff; utility reference 0.
- **monitor:** check only an approved channel at a declared cadence, up to a fixed horizon, then stop; act only if a legitimate opening is detected in time. Include that conditional application in the policy value.
- **prepare:** a bounded preparation task plus that same finite monitoring policy; preparation improves conditional completion probability, if justified, at additional cost. Preparation does not create permission.
- **apply:** submit now only if an eligible actor has an open or rule-preserved route. Compare net utility with stop.
- **appeal:** invoke an explicitly authorized route before its deadline. No invented contact campaign or presumed exception.

For historical GATE, cadence, horizon, and detection/completion probabilities are scenario assumptions fixed before scoring, not fitted to the October reopening dates. Conditional follow-up stops after success, horizon, exhaustion of budget, loss of eligibility, or terminal notice. Monitoring itself has no power to cause reopening. The initial unit implementation evaluates already enumerated policies; it does not simulate portal actions or claim optimality over every possible schedule.

## Cost-sensitive pre-outcome score

Let V >= 0 be the actor's net value of a successful opportunity relative to stopping, including ordinary downstream fees and opportunity costs consistently. Let p be the probability of a legitimate usable opening within the fixed horizon given cutoff information, d the conditional probability of detecting it in time, q completion probability conditional on detection and eligibility, c_m total monitoring burden, c_p preparation burden, and h a non-event burden from maintaining hope/deferring alternatives. All monetary/time/psychological burdens must be converted to the same declared utility scale; set h=0 unless an independently justified value is available. Never double-count costs already included in V. The simple model assumes bounded nonnegative V, nonnegative costs, and no other benefits from preparation.

For baseline q0 and prepared q1:

    U(stop)    = 0
    U(monitor) = p*d*q0*V - c_m - (1-p)*h
    U(prepare) = p*d*q1*V - c_m - c_p - (1-p)*h
    U(apply)   = q_apply*V - c_apply                 [if permitted now]
    U(appeal)  = p_appeal*V - c_appeal               [if explicitly authorized]

Probabilities are conditional definitions; the product p*d*q needs no unconditional independence claim. Appeal success includes any downstream completion risk. Costs here are fixed policy budgets paid regardless of event; for contingent costs, replace these terms by preregistered expected costs rather than silently reusing this formula. Do not add mutually exclusive success probabilities. A terminal rule removes monitor/prepare/apply/appeal from the action set. Other scenarios can have different action masks.

Primary score: **reference expected regret** R(a)=max over feasible b of U(b) minus U(a), computed before outcome release. Report feasibility violations separately (they fail that decision), not as a convenient small penalty. For strict reproducibility, policies tied within epsilon=1e-9 are value-equivalent; the deterministic comparator breaks ties toward stop, then monitor, prepare, apply, appeal. This tie rule is a convention, not a psychological claim. For a future empirical pilot, precommit an actor-relevant practical regret tolerance as well; none is asserted in S1.

Also report ΔU relative to stop, monitoring/appeal burdens, rates of unsupported actions, and mechanism/evidence errors. With uncertain p, report regret and sign over the entire preregistered range. A historical recommendation is unresolved if plausible values cross the stop threshold. Reference inputs cannot be estimated from the single held outcome or from the evaluated agent's own convenient probabilities. The cost-threshold test for monitor is p*d*q0*V > c_m+(1-p)*h. Preparation beats monitoring only if p*d*(q1-q0)*V > c_p. This is standard option/value-of-information reasoning, not theoretical novelty.

For **realized hindsight utility**, replace p by event indicator y in the monitor/prepare expressions to obtain an expectation over detection/completion conditional on that event; label it conditional, not an observed payoff. A true realized payoff additionally requires actual detection, completion, and paid-cost observations. Report these separately when available. Do not rank ex ante rationality by a single realized outcome. `check_s1.py` implements reference expected utilities only.

## Analysis, leakage, and release gates

Primary pilot contrasts: S versus H regret under common numerical assumptions, and H versus P regret/feasibility. Publish each paired case and cost change, including ties and errors. P being optimal in its own finite action set is by construction, not an empirical win. Do not report confidence intervals or significance claims from this tiny purposive case set; future inference needs a sampling frame, sample-size justification, and independent cases, not repeated paraphrases counted as independent subjects.

Fatal leakage check: audit source availability and packet bytes before running; ensure evaluator-held outcomes, later site content, suggestive IDs, and metadata are absent. Review outputs for specific post-cutoff claims before releasing outcomes. Any discovered leakage invalidates the run regardless of score. No detected leak does not eliminate model-training memorization. A historical run without retrospective source-snapshot provenance fails validity even if answers look plausible.

No external model call is authorized or performed in this pass. The next single empirical experiment is this frozen-packet pilot, subject to source provenance, novelty review, and separately authorized execution. If H matches P, if both S/H are rational across admissible uncertainty, or if only hints/leakage produce an advantage, reject the candidate failure claim. If H fails with explicit values and legitimate actions, that supports a narrow action-selection failure under the supplied assumptions, not general real-world irrationality.
