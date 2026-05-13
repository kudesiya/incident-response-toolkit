#!/usr/bin/env python3
"""
create_incident.py — spin up a new incident doc from template

Reads config.yaml for defaults, classifies severity, generates a
populated runbook file, and prints the Slack/email notification draft.

Usage:
    python scripts/create_incident.py --config config.yaml
    python scripts/create_incident.py --config config.yaml --dry-run

    # pass metrics directly if you have them
    python scripts/create_incident.py \
        --error-rate 0.08 \
        --latency-p99 5500 \
        --description "elevated errors on /api/checkout"
"""

import argparse
import os
import sys
import yaml
import json
from datetime import datetime, timezone

# allow running from repo root
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from classifier.severity import classify, get_notification_config


def load_config(path):
    if not os.path.exists(path):
        print(f"[error] config file not found: {path}")
        sys.exit(1)
    with open(path) as f:
        return yaml.safe_load(f)


def load_template(template_path):
    with open(template_path) as f:
        return f.read()


def render_template(template: str, substitutions: dict) -> str:
    out = template
    for k, v in substitutions.items():
        out = out.replace(f"{{{{{k}}}}}", str(v))
    return out


def build_slack_message(incident_id, severity, description, runbook_path, cfg):
    sev_emoji = {
        "CRITICAL": ":red_circle:",
        "HIGH":     ":large_orange_circle:",
        "MEDIUM":   ":large_yellow_circle:",
        "LOW":      ":white_circle:",
    }
    emoji = sev_emoji.get(severity.level, ":white_circle:")
    bridge = " | Bridge required — start a call now" if severity.requires_bridge else ""

    return f"""
{emoji} *Incident {incident_id}* — {severity.level}{bridge}

*Description:* {description}
*Response SLA:* {severity.response_time_minutes} min
*Classified by:* {severity.matched_rule}

*Notify:* {", ".join(severity.notify)}
*Runbook:* {runbook_path}

_Update this thread every 30 min until resolved._
""".strip()


def build_email_body(incident_id, severity, description, ts, cfg):
    team = cfg.get("team", {})
    return f"""Subject: [{severity.level}] Incident {incident_id} — {description}

Team,

A new incident has been declared. Details below.

Incident ID   : {incident_id}
Severity      : {severity.level}
Declared at   : {ts}
Description   : {description}
Response SLA  : {severity.response_time_minutes} minutes
Bridge needed : {"Yes — please join the call" if severity.requires_bridge else "No"}

Classified because: {severity.matched_rule}

Please acknowledge within {severity.response_time_minutes} minutes.
Live updates will be posted in Slack.

-- Incident Command
""".strip()


def main():
    parser = argparse.ArgumentParser(description="Create a new incident")
    parser.add_argument("--config", default="config.yaml", help="Path to config.yaml")
    parser.add_argument("--description", "-d", default="", help="Short incident description")
    parser.add_argument("--error-rate", type=float, default=None, help="Current error rate (0.0–1.0)")
    parser.add_argument("--latency-p99", type=float, default=None, help="p99 latency in ms")
    parser.add_argument("--latency-p95", type=float, default=None, help="p95 latency in ms")
    parser.add_argument("--availability", type=float, default=None, help="Current availability (0.0–1.0)")
    parser.add_argument("--keywords", nargs="*", default=[], help="Keywords from alert text")
    parser.add_argument("--dry-run", action="store_true", help="Print output, don't write files")
    parser.add_argument("--output-dir", default="active_incidents", help="Where to write runbook")
    args = parser.parse_args()

    cfg = load_config(args.config)
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    date_str = datetime.now(timezone.utc).strftime("%Y%m%d")
    incident_id = f"INC-{date_str}-{datetime.now(timezone.utc).strftime('%H%M')}"

    # classify
    severity = classify(
        error_rate=args.error_rate,
        availability=args.availability,
        latency_p99_ms=args.latency_p99,
        latency_p95_ms=args.latency_p95,
        keywords=args.keywords or ([args.description] if args.description else []),
    )

    description = args.description or "< add description >"

    # populate runbook template
    template_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "templates", "incident_runbook.md"
    )
    template = load_template(template_path)
    runbook_content = render_template(template, {
        "INCIDENT_ID":         incident_id,
        "SEVERITY":            severity.level,
        "DESCRIPTION":         description,
        "TIMESTAMP":           ts,
        "RESPONSE_TIME_MIN":   severity.response_time_minutes,
        "REQUIRES_BRIDGE":     "Yes" if severity.requires_bridge else "No",
        "NOTIFY":              ", ".join(severity.notify),
        "CLASSIFIED_BY":       severity.matched_rule,
        "DECLARED_BY":         cfg.get("defaults", {}).get("declared_by", "< your name >"),
        "SERVICE":             cfg.get("defaults", {}).get("service", "< service name >"),
    })

    # output paths
    runbook_filename = f"{incident_id}.md"
    runbook_path = os.path.join(args.output_dir, runbook_filename)

    slack_msg = build_slack_message(incident_id, severity, description, runbook_path, cfg)
    email_body = build_email_body(incident_id, severity, description, ts, cfg)

    if args.dry_run:
        print("=" * 60)
        print(f"DRY RUN — nothing written to disk")
        print("=" * 60)
        print(f"\n[Incident ID]  {incident_id}")
        print(f"[Severity]     {severity.level}")
        print(f"[Matched rule] {severity.matched_rule}")
        print(f"\n--- SLACK MESSAGE ---\n{slack_msg}")
        print(f"\n--- EMAIL BODY ---\n{email_body}")
        print(f"\n--- RUNBOOK PREVIEW (first 30 lines) ---")
        print("\n".join(runbook_content.splitlines()[:30]))
        return

    # write runbook
    os.makedirs(args.output_dir, exist_ok=True)
    with open(runbook_path, "w") as f:
        f.write(runbook_content)

    # write notification drafts alongside the runbook
    notif_path = os.path.join(args.output_dir, f"{incident_id}_notifications.txt")
    with open(notif_path, "w") as f:
        f.write("=== SLACK ===\n\n")
        f.write(slack_msg + "\n\n")
        f.write("=== EMAIL ===\n\n")
        f.write(email_body + "\n")

    print(f"[ok] Runbook created: {runbook_path}")
    print(f"[ok] Notifications:   {notif_path}")
    print(f"\nSeverity: {severity.level} — {severity.description}")
    print(f"Matched:  {severity.matched_rule}")
    if severity.requires_bridge:
        print("\n[!] Bridge call required — start one now")


if __name__ == "__main__":
    main()
