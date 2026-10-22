# After Observed Closure: A Cutoff-Audited Protocol for Cost-Sensitive Opportunity Preservation

**Working paper skeleton. Protocol proposal; no empirical results.**

## Abstract

An observed application closure may coexist with uncertainty about future availability, an existing grace entitlement, or an authorized appeal. An agent advising an actor must distinguish these mechanisms and weigh the cost of preserving an opportunity against the value of stopping. We propose an evaluation protocol that separates current status recognition, use of historically available governing evidence, action feasibility, and expected utility under declared assumptions. The protocol compares status-only and history-informed agents with a simple finite-policy comparator, includes terminal and false-hope controls, and separates pre-outcome decision quality from subsequent outcomes. A candidate GATE historical case requires verification of source snapshots available at a specified cutoff; its later outcome is held by the evaluator. No historical packet, model behavior, or empirical effect has yet been validated. The proposed contribution, if distinct from existing work, would be a reproducible diagnostic evaluation rather than a new theory of sequential decisions.

## 1. Introduction

“Closed” is a statement about an observed route at a time. Depending on governing rules and actor eligibility, it can imply an absorbing endpoint, a currently unavailable route subject to external policy change, or an ordinary route replaced by a preexisting entitlement or authorized procedure. Advice can therefore be factually correct about status while incomplete as a policy. Conversely, advice to keep checking can waste attention, delay alternatives, or encourage unsupported expectations.

The scientific question is not whether agents should be optimistic. It is whether they map cutoff-available evidence and explicit actor costs to feasible finite policies. A potentially important failure is recognizing both closure and a relevant mechanism yet failing to take a cost-justified reversible action. That hypothesis must compete with absent retrieval, mistaken mechanisms, uncertain preferences, rational stopping, and hindsight bias.

POMDPs, value of information, optimal stopping, and real options already explain why actions preserving uncertain opportunities can be rational. Temporal and nonstationary evaluations may already test similar reasoning. The candidate contribution is narrower: an auditable evaluation that separates historical evidence access, mechanism permissions, and action value without treating a later reopening as the correct answer. Whether this distinction is original remains unestablished.

The motivating mechanisms are external policy reopening, automatic entitlement/grace, and authorized appeal. GATE, subscription, and VIT examples motivate the distinction but are not a verified cross-domain dataset. This paper must not present them as causal evidence.

## 2. Formal problem

At decision time t0, an actor observes a history H restricted to evidence publicly available by t0. The latent state x includes current availability, eligibility, the governing mechanism, preparation, and remaining time. An observation of closure need not identify x or future transition probabilities. A belief b(x|H) and a transition kernel determine the probability of a usable future opportunity within a finite horizon T.

A policy maps admissible observations to authorized actions. The action set includes stopping, bounded monitoring, preparation, immediate application, and appeal where permitted. A rule-dependent mask A(H, actor) excludes actions without legal or procedural authority. Monitoring observes transitions; external reopening is not an intervention by the monitoring actor. An appeal is an intervention only if a governing procedure permits it. Stopping is absorbing for this evaluated opportunity, even if a counterfactual world later changes.

For a finite declared policy set Π, evaluate

    U(π | H, θ) = E[net opportunity value - effort - delay burden | H, θ, π]
    R(π | H, θ) = max_{π' feasible in Π} U(π' | H, θ) - U(π | H, θ).

θ contains preferences, conditional event/detection/completion probabilities, and costs fixed before outcome disclosure. For a closed but potentially recoverable route, a simple policy value is p*d*q*V-c_m-(1-p)*h. Preparation may increase q at cost c_p. This is an illustrative conventional decision model; it does not identify θ from anecdotes. Report sensitivity over plausible θ rather than treating an arbitrary point estimate as historical truth. Infeasible actions are explicit violations. Finite-policy regret does not establish global optimality over all schedules.

Counterfactual expected utility and observed outcome are distinct. A later reopening can coexist with a rational ex ante stop, and a never-reopening trajectory can coexist with rational monitoring. Historical outcome labels are insufficient labels of decision quality.

## 3. Related-work topics and collision audit

Bibliography pending a primary-source audit; no external citations are asserted here.

- **Belief-state planning and value of information:** observation versus latent state, active information acquisition, costly sensing, and belief updates. Establish what, if anything, this protocol tests beyond existing belief-sensitive agent evaluations.
- **Real options, optimal stopping, and finite-horizon search:** option preservation, abandonment thresholds, preparation investment, and deadlines. The utility equations belong to this established family.
- **Temporal evaluation and nonstationary tool environments:** cutoff QA, fact changes, historical retrieval, policy-dependent permissions, and contamination from future evidence. Audit whether existing benchmarks already jointly cover provenance and cost-sensitive action selection.

Also compare practical language-agent planning and calibration studies where they intersect these classes. A final paper needs precise citations and direct overlap analysis before making any originality claim. If no distinct contribution remains, do not submit this skeleton as a novel benchmark.

## 4. Minimal experiment

Use the frozen-packet protocol in `EXPERIMENT_1.md`: status-only agent S, history-informed agent H, and a deterministic mechanism-aware comparator P with shared numerical assumptions. The historical candidate cutoff is 2026-10-13 12:00 Asia/Kolkata. All historical chronology and exact source URLs currently await verification. Current web pages are not admissible substitutes for proven pre-cutoff snapshots.

The pilot pairs the historical candidate with synthetic automatic-grace, authorized-appeal, final-closure, and false-hope controls. Cross costs around predeclared utility thresholds. Measure paired reference regret, feasibility, threshold sensitivity, and evidence/mechanism errors. Preserve fresh contexts and isolate evaluator-held outcomes. The small pilot can diagnose individual failure patterns; it cannot estimate population prevalence or establish statistical significance.

Retrospective source-snapshot provenance is a prerequisite. Capture hashes, availability evidence, transformations, and packet manifests must permit reconstruction. Leakage invalidates a run. Model training may contain historical outcomes even with perfect packet filtering, motivating neutralized synthetic and eventually prospective replication.

## 5. Results — unfilled

- Primary-source and historical packet verification: **pending**.
- Prior-art distinction: **pending**.
- Empirical model outputs, regret contrasts, feasibility rates, and practical effect sizes: **not collected**.
- Controls and uncertainty sensitivity on actual agent decisions: **not run**.
- Local scoring arithmetic: synthetic unit tests are provided separately; they do not measure agents, mechanisms, or real-world benefit.

Do not fill this section with invented counts, illustrative model quotes presented as data, or assertions of successful validation. Retain null, mixed, or disconfirming results if an experiment is later conducted.

## 6. Limitations and validity threats

A chosen reopening case creates severe selection and hindsight bias. Historical publication times may be unverifiable, edited pages can conceal future information, and retrospective models may have memorized the outcome. A previous extension supplies no stable estimate of reopening probability. Actor values and burden conversions may dominate recommendations. Appeals and entitlements differ across domains and cannot be treated as interchangeable recoveries.

A comparator using its own declared utility is optimal by construction. Beating an LLM under that model may reflect arithmetic, prompt compliance, or missing inputs rather than a deep planning deficit. History prompts may alter salience as well as retrieval. A tiny purposive pilot offers neither causal identification of a cognitive failure nor external validity. Strong claims require independent cases, adverse controls, credible utility assumptions, and a prior-art distinction.

The original repository implements a static fraud investigate/commit task, with a final-step score-overwrite defect and fixed clues. It remains unchanged as provenance. It neither implements this proposed experiment nor validates this paper. No deployed decision system, benchmark suite, or new framework is delivered here.

## 7. Discussion and publication gate

A defensible positive result would show a reproducible evidence-to-action gap under explicit assumptions while preserving correct stopping on terminal and low-value cases. An equally informative negative result would show that supplied-evidence agents already track the simple policy or that historical uncertainty prevents labeling a failure. Neither supports a universal instruction to monitor after closure.

Proceed toward an article only if the significance, validity, originality, and reproducibility vetoes in `S1_DECISION.md` pass. Until then, this is a reviewable protocol and an untested scientific hypothesis.
