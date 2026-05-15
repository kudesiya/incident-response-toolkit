"""
severity.py — classify an incident based on metrics or keywords

Usage:
    from classifier.severity import classify

    sev = classify(error_rate=0.08, latency_p99_ms=6000)
    print(sev.level)   # HIGH

Or from CLI via create_incident.py
"""

import yaml
import os
from dataclasses import dataclass
from typing import Optional

RULES_FILE = os.path.join(os.path.dirname(__file__), "rules.yaml")


@dataclass
class SeverityResult:
    level: str
    description: str
    response_time_minutes: int
    requires_bridge: bool
    notify: list
    matched_rule: str   # why we picked this level — useful for postmortems


def load_rules(path=RULES_FILE):
    with open(path) as f:
        return yaml.safe_load(f)


def classify(
    error_rate: Optional[float] = None,
    availability: Optional[float] = None,
    latency_p99_ms: Optional[float] = None,
    latency_p95_ms: Optional[float] = None,
    keywords: Optional[list] = None,
    rules_path: str = RULES_FILE,
) -> SeverityResult:
    """
    Evaluate metrics/keywords against configured rules and return a severity.
    First match wins — rules are ordered CRITICAL → LOW in the config.

    Args:
        error_rate:      fraction (0.0–1.0), e.g. 0.05 = 5% errors
        availability:    fraction (0.0–1.0), e.g. 0.995 = 99.5%
        latency_p99_ms:  p99 response time in ms
        latency_p95_ms:  p95 response time in ms
        keywords:        list of strings from alert text or description
        rules_path:      override default rules.yaml location

    Returns:
        SeverityResult with level, description, response time, notifications
    """
    cfg = load_rules(rules_path)
    metrics = {
        "error_rate": error_rate,
        "availability": availability,
        "latency_p99_ms": latency_p99_ms,
        "latency_p95_ms": latency_p95_ms,
    }
    kw_lower = [k.lower() for k in (keywords or [])]

    ops = {
        ">=": lambda a, b: a >= b,
        "<=": lambda a, b: a <= b,
        ">":  lambda a, b: a > b,
        "<":  lambda a, b: a < b,
        "==": lambda a, b: a == b,
    }

    for level, spec in cfg["severity_levels"].items():
        for rule in spec.get("rules", []):
            # keyword match
            if "keyword_match" in rule:
                for kw in rule["keyword_match"]:
                    if any(kw.lower() in k for k in kw_lower):
                        return SeverityResult(
                            level=level,
                            description=spec["description"],
                            response_time_minutes=spec["response_time_minutes"],
                            requires_bridge=spec["requires_bridge"],
                            notify=spec["notify"],
                            matched_rule=f"keyword: '{kw}'",
                        )
                continue

            # metric threshold
            metric_name = rule.get("metric")
            val = metrics.get(metric_name)
            if val is None:
                continue

            op_fn = ops.get(rule["operator"])
            if op_fn and op_fn(val, rule["threshold"]):
                return SeverityResult(
                    level=level,
                    description=spec["description"],
                    response_time_minutes=spec["response_time_minutes"],
                    requires_bridge=spec["requires_bridge"],
                    notify=spec["notify"],
                    matched_rule=f"{metric_name} {rule['operator']} {rule['threshold']} (got {val})",
                )

    # nothing matched — default LOW, better to be safe than miss something
    low = cfg["severity_levels"]["LOW"]
    return SeverityResult(
        level="LOW",
        description=low["description"],
        response_time_minutes=low["response_time_minutes"],
        requires_bridge=low["requires_bridge"],
        notify=low["notify"],
        matched_rule="no rules matched — defaulted to LOW",
    )


def get_notification_config(rules_path=RULES_FILE):
    cfg = load_rules(rules_path)
    return cfg.get("notifications", {})
