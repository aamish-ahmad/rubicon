#!/usr/bin/env python3
"""Synthetic UNIT TESTS for EXPERIMENT_1.md, never empirical findings.

Finite-policy expected utility only. Parameters are illustrative, not GATE
estimates. This code does not fetch sources, call models, or modify the app.
Run: python3 -B research/check_s1.py
"""

from dataclasses import dataclass, replace
import math
import unittest


ACTIONS = ("stop", "monitor", "prepare", "apply", "appeal")
EPSILON = 1e-9


@dataclass(frozen=True)
class Scenario:
    value: float = 100.0
    p: float = 0.2
    detection: float = 1.0
    q_base: float = 0.5
    q_prepared: float = 0.9
    monitor_cost: float = 2.0
    preparation_cost: float = 3.0
    false_hope_cost: float = 0.0
    q_apply: float = 1.0
    application_cost: float = 1.0
    appeal_success: float = 0.1
    appeal_cost: float = 2.0
    monitor_allowed: bool = True
    prepare_allowed: bool = True
    apply_allowed: bool = False
    appeal_allowed: bool = False
    terminal: bool = False

    def __post_init__(self):
        for name in ("p", "detection", "q_base", "q_prepared", "q_apply",
                     "appeal_success"):
            number = getattr(self, name)
            if not math.isfinite(number) or not 0 <= number <= 1:
                raise ValueError(f"{name} must be finite and in [0, 1]")
        for name in ("value", "monitor_cost", "preparation_cost",
                     "false_hope_cost", "application_cost", "appeal_cost"):
            number = getattr(self, name)
            if not math.isfinite(number) or number < 0:
                raise ValueError(f"{name} must be finite and nonnegative")


def utilities(s):
    """Return values only for feasible, enumerated policies.

    Costs are fixed budgets. Conditional probabilities and action masks are
    inputs; they are not inferred from an eventual outcome or deadline history.
    Preparation here includes the monitoring policy and its cost.
    """
    result = {"stop": 0.0}
    if s.terminal:
        return result
    if s.monitor_allowed:
        common_cost = s.monitor_cost + (1 - s.p) * s.false_hope_cost
        result["monitor"] = s.p * s.detection * s.q_base * s.value - common_cost
        if s.prepare_allowed:
            result["prepare"] = (s.p * s.detection * s.q_prepared * s.value
                                 - common_cost - s.preparation_cost)
    if s.apply_allowed:
        result["apply"] = s.q_apply * s.value - s.application_cost
    if s.appeal_allowed:
        result["appeal"] = s.appeal_success * s.value - s.appeal_cost
    if not all(math.isfinite(number) for number in result.values()):
        raise ValueError("Utility overflow; rescale inputs")
    return result


def best_action(s):
    values = utilities(s)
    maximum = max(values.values())
    # EPSILON-equivalent policies use the documented stable tie ordering.
    return next(a for a in ACTIONS if a in values
                and maximum - values[a] <= EPSILON)


def regret(s, action):
    values = utilities(s)
    if action not in values:
        raise ValueError(f"Infeasible or unknown action: {action}")
    return max(values.values()) - values[action]


class SyntheticScoringTests(unittest.TestCase):
    def test_reference_arithmetic(self):
        values = utilities(Scenario())
        self.assertAlmostEqual(values["monitor"], 8.0)
        self.assertAlmostEqual(values["prepare"], 13.0)
        self.assertEqual(best_action(Scenario()), "prepare")

    def test_regret_uses_feasible_best(self):
        self.assertAlmostEqual(regret(Scenario(), "monitor"), 5.0)
        self.assertAlmostEqual(regret(Scenario(), "stop"), 13.0)
        self.assertAlmostEqual(regret(Scenario(), "prepare"), 0.0)

    def test_high_cost_stop(self):
        self.assertEqual(best_action(Scenario(monitor_cost=30)), "stop")

    def test_false_hope_zero_event_probability(self):
        s = Scenario(p=0)
        self.assertEqual(best_action(s), "stop")
        self.assertLess(utilities(s)["monitor"], 0)
        self.assertLess(utilities(s)["prepare"], 0)

    def test_terminal_overrides_all_permissions(self):
        s = Scenario(terminal=True, apply_allowed=True, appeal_allowed=True)
        self.assertEqual(utilities(s), {"stop": 0.0})
        self.assertEqual(best_action(s), "stop")
        with self.assertRaises(ValueError):
            regret(s, "monitor")

    def test_infeasible_actions_are_not_small_penalties(self):
        for action in ("apply", "appeal", "invented_exception"):
            with self.subTest(action=action), self.assertRaises(ValueError):
                regret(Scenario(), action)

    def test_open_entitlement_allows_apply(self):
        s = Scenario(apply_allowed=True)
        self.assertEqual(best_action(s), "apply")
        self.assertAlmostEqual(utilities(s)["apply"], 99.0)

    def test_authorized_appeal_can_win(self):
        s = Scenario(appeal_allowed=True, appeal_success=0.8)
        self.assertEqual(best_action(s), "appeal")
        self.assertAlmostEqual(utilities(s)["appeal"], 78.0)

    def test_authorized_appeal_can_be_bad(self):
        s = Scenario(monitor_allowed=False, appeal_allowed=True,
                     appeal_success=0.01, appeal_cost=2)
        self.assertEqual(best_action(s), "stop")
        self.assertLess(utilities(s)["appeal"], 0)

    def test_preparation_increment_threshold(self):
        s = Scenario(preparation_cost=9)
        self.assertAlmostEqual(utilities(s)["prepare"]
                               - utilities(s)["monitor"], -1.0)
        self.assertEqual(best_action(s), "monitor")

    def test_monitor_threshold_and_tie(self):
        s = Scenario(p=0.04, prepare_allowed=False)
        self.assertAlmostEqual(utilities(s)["monitor"], 0.0)
        self.assertEqual(best_action(s), "stop")
        self.assertEqual(best_action(replace(s, p=0.05)), "monitor")
        self.assertEqual(best_action(replace(s, p=0.03)), "stop")

    def test_false_hope_burden(self):
        s = Scenario(false_hope_cost=5)
        self.assertAlmostEqual(utilities(s)["monitor"], 4.0)
        self.assertAlmostEqual(utilities(s)["prepare"], 9.0)

    def test_detection_failure_cannot_create_value(self):
        s = Scenario(detection=0)
        self.assertEqual(best_action(s), "stop")

    def test_no_preparation_benefit_means_no_preparation(self):
        s = Scenario(q_prepared=0.5)
        self.assertEqual(best_action(s), "monitor")

    def test_unknown_outcome_is_not_a_scoring_input(self):
        # A rational stop at these inputs remains rational whether the actual
        # world later reopens or stays closed. Outcomes are never passed in.
        s = Scenario(p=0.01, prepare_allowed=False)
        self.assertEqual(best_action(s), "stop")
        self.assertAlmostEqual(regret(s, "stop"), 0.0)

    def test_parameter_validation(self):
        for kwargs in ({"p": -0.1}, {"p": 1.1}, {"p": math.nan},
                       {"value": math.inf}, {"monitor_cost": -1},
                       {"q_prepared": math.inf}):
            with self.subTest(kwargs=kwargs), self.assertRaises(ValueError):
                Scenario(**kwargs)


if __name__ == "__main__":
    print("SYNTHETIC UNIT TESTS ONLY — no empirical findings or GATE estimates.",
          flush=True)
    unittest.main(verbosity=2)
