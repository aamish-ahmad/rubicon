# S1 scientific decision

Status: protocol and synthetic scoring checks only. No empirical finding, source validation, model evaluation, or paper validation has occurred. This is one bounded local pass on `research/open-world-s1`, based on original `24bfde81ed877aaa90220f3486623a17652e94fc`. No application changes, commits, pushes, paid API calls, or external LLM evaluations are part of S1.

## Candidate contribution

Propose a cutoff-audited evaluation of whether an agent converts historically available governing evidence into a *legitimate, cost-sensitive policy that preserves an opportunity after an observed closure*. The candidate contribution is the evaluation construction and causal diagnostic comparison, conditional on a prior-art audit; it is not a new solution to sequential decision making. A useful result would identify when an agent says “closed” correctly yet chooses a dominated action under explicitly supplied costs and mechanism assumptions, and distinguish that from missing evidence or rational stopping.

“Recoverable” describes a possible state transition supported by rules or history, not an entitlement to success. External reopening (GATE), automatic entitlement/grace (subscription), and authorized appeal (VIT) have different transition kernels and action permissions. They motivate strata, not three causal samples. Neither all closures nor all domains warrant monitoring. A finite budget and a stopping rule are central.

The present repository is provenance, not evidence for this candidate: its tiny fraud environment has fixed truths and clues and investigate/commit actions. In `src/rubicon_openenv/environment.py`, reaching `max_steps` overwrites any same-step commitment reward and observation with a timeout; app-level reward clipping also exists. Do not use these scores as scientific results or claim this implementation evaluates recovery mechanisms. Preserve the code unchanged.

## Three tough prior-art collisions

1. **POMDP / belief MDP / value of information.** A closed observation can coexist with uncertainty over future availability; monitoring is an information-gathering action, and preparation changes later action feasibility. Standard belief-state control already represents this. A renaming of latent state or belief updating fails originality. Possible residue: a reproducible test isolating evidence-to-action failures with legal action masks and cutoff provenance. Pending: find whether existing agent evaluations already make exactly this distinction.
2. **Real options / optimal stopping / search under deadlines.** Paying a small cost to retain an uncertain future opportunity is an ordinary option-value calculation; finite-horizon monitoring and abandonment are textbook decision problems. Threshold behavior alone is no discovery. Possible residue: measuring language-agent deviations from independently specified thresholds, especially rule-authorized actions versus unsupported persistence. Pending: compare existing sequential advice and option-preservation evaluations.
3. **Nonstationary environments / temporal and retrieval evaluations.** Time-indexed facts, stale answers, policy change, temporal QA, tool use, and historical replay may already cover observed closure followed by changed availability. A benchmark that just rewards knowing a later reopening fails novelty and validity. Possible residue: a source-audited historical cutoff plus separated retrieval, mechanism recognition, and action-value diagnostics. Pending: determine whether that full combination is already established and whether any observed gap is material.

No external bibliography has been verified in this pass. These are collision classes, not claims that any named work omitted the proposal. A subsequent primary-source literature audit must record exact works, overlapping claims, and the smallest remaining distinction before submission.

## Competing hypotheses and discriminators

| Hypothesis | Distinguishing observation | What would weaken it |
|---|---|---|
| Retrieval failure | Status-only agents stop; supplying admissible history improves evidence use and decisions | No improvement with a verified complete evidence packet |
| Model/mechanism failure | With the same history, an agent fails to distinguish external reopening, automatic grace, authorized appeal, and final closure | Correct mechanism and feasible action set identified reliably |
| Action-value failure | Agent identifies mechanism and permissions but chooses a dominated policy under supplied probability/cost inputs | Decisions track thresholds and costs once values are explicit |
| Rational stopping under randomness | Stopping maximizes expected utility, or lies within the predeclared ambiguity band, despite eventual reopening | Dominance or positive regret under every admissible parameter setting |

These can coexist. A history packet can improve salience as well as retrieval, so the initial comparison does not by itself identify a latent cognitive cause. A simple policy is a normative comparator under assumptions, not evidence of model intelligence or a guarantee of real-world success.

## Falsification and rejection criteria

Precommit the source cutoff, action masks, parameter ranges, primary contrasts, and cost normalization before seeing agent outputs. Reject the proposed failure claim if supplied-evidence agents choose feasible, near-optimal policies under those inputs, if gains disappear after equalizing evidence/prompt budget, or if outcome knowledge accounts for gains. If admissible probability ranges straddle the stop threshold, label the historical recommendation unresolved; do not call stopping an error. A later reopening cannot falsify an ex ante rational stop.

Reject the scientific use of the GATE case if no trustworthy pre-cutoff source snapshots can be recovered. Reject any empirical run with a leaked outcome or unfiltered current website in its input. An undetectable memorization risk restricts historical LLM results to exploratory evidence, even after a clean packet audit. One selected reopening cannot establish prevalence, calibration, or general superiority.

## Veto checks

- **Significance:** Would the effect change a consequential, cost-sensitive decision beyond a trivial “check again” reminder? Require a preregistered practically meaningful regret difference and terminal-case specificity. No threshold or effect size is established yet.
- **Validity:** Are action permissions and transition assumptions justified at the cutoff? Are opportunity, burden, delay, and false hope valued consistently? Were both reopening and never-reopening controls included? Any hindsight-derived prior, invented appeal right, or fatal leakage vetoes the claim.
- **Originality:** Can a primary-source audit distinguish this evaluation from the three collision classes? If the only distinction is a new story, do not claim an original scientific contribution.
- **Reproducibility:** Can another reader reconstruct packet bytes, publication and capture times, hashes, redactions, model inputs, settings, outputs, and scores? Missing retrospective provenance vetoes historical inference. Synthetic tests establish arithmetic only.

## Go / no-go

**GO:** make the protocol and scoring assumptions reviewable and run local synthetic unit tests. **NO-GO:** submit a paper claiming novelty, empirical model failure, a validated benchmark, or real-world utility. No model result is currently available. The next single experiment, after admissible snapshots and the literature gate are satisfied, is the small frozen-evidence comparison in `EXPERIMENT_1.md`. If provenance cannot be recovered, stop the historical claim and explicitly redesign a prospective or synthetic study; do not silently substitute it as historical evidence.

Biggest rejection risk: this is a selected hindsight anecdote dressed as standard option-value reasoning, with no new phenomenon or evaluation advantage. The protocol only becomes defensible if it survives the prior-art audit and shows a reproducible, practically meaningful, cost-sensitive gap with equally visible negative controls.

## Local verification record

`python3 -B research/check_s1.py` completed with exit code 0: **16 synthetic unit tests passed**. This verifies only the declared finite-policy scoring arithmetic and action-mask checks, not empirical hypotheses. Repository inspection after the run found only the five new files under `research/`; tracked application files have no diff. HEAD, local `main`, and `research/open-world-s1` remain at `24bfde81ed877aaa90220f3486623a17652e94fc`. No commit, push, network access, or external model evaluation was performed. Final bounded-pass status: **VERIFIED_PASS** for artifact creation and synthetic checks; scientific submission remains **NO-GO** pending the stated gates.
