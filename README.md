# incident-response-toolkit

Practical incident management tools for cloud-native platforms.

Built and iterated on across SRE roles in Fintech, Healthcare, and EdTech — this is the toolkit I kept rebuilding for every organization. Decided to put it somewhere reusable. All configurations and examples are sanitized and generic — no proprietary or company-specific information is included.

Not trying to replace PagerDuty or Jira. This handles the stuff that falls between your alerting tool and your ticketing system — severity classification, runbook generation, postmortems, and MTTR tracking from a simple JSON log.

---

## What's in here

```
classifier/     severity engine — classify incidents by metrics or keywords
templates/      runbook, postmortem, comms, oncall handoff templates
scripts/        create_incident.py, mttr_calculator.py
examples/       sample incident log for the MTTR calculator
docs/           severity classification guide
```

---

## Quickstart

```bash
git clone https://github.com/yourusername/incident-response-toolkit
cd incident-response-toolkit
pip install pyyaml

# copy and edit config
cp config.yaml my-config.yaml

# dry run — see what would be created
python scripts/create_incident.py \
  --config my-config.yaml \
  --description "elevated 503s on auth service" \
  --error-rate 0.08 \
  --dry-run

# create a real incident runbook
python scripts/create_incident.py \
  --config my-config.yaml \
  --description "checkout API errors" \
  --error-rate 0.12 \
  --latency-p99 6000

# compute MTTR from an incident log
python scripts/mttr_calculator.py \
  --log examples/sample_incidents.json \
  --since 2024-01-01
```

---

## Severity classifier

Classifies incidents as `CRITICAL / HIGH / MEDIUM / LOW` based on metrics or keywords.

Rules live in `classifier/rules.yaml` — edit them to match your SLOs. The defaults are starting points, not gospel.

```python
from classifier.severity import classify

# by metrics
result = classify(error_rate=0.08, latency_p99_ms=5500)
print(result.level)          # HIGH
print(result.matched_rule)   # error_rate >= 0.05 (got 0.08)
print(result.response_time_minutes)  # 30

# by keywords from an alert
result = classify(keywords=["authentication down", "login failing"])
print(result.level)   # CRITICAL
```

Rule evaluation is top-down, first match wins. If nothing matches, it defaults to LOW — better to be safe.

---

## create_incident.py

Generates a populated runbook file + notification drafts (Slack message and email body) for a new incident.

```bash
python scripts/create_incident.py \
  --config config.yaml \
  --description "payment gateway timeouts" \
  --error-rate 0.06 \
  --output-dir active_incidents
```

Output:
```
active_incidents/
  INC-20240315-1423.md           # runbook, ready to fill in
  INC-20240315-1423_notifications.txt   # pre-drafted Slack + email
```

Options:
```
--description    Short incident description
--error-rate     Current error rate (0.0–1.0)
--latency-p99    p99 latency in ms
--latency-p95    p95 latency in ms
--availability   Current availability (0.0–1.0)
--keywords       Keywords from alert text
--dry-run        Print output without writing files
--output-dir     Where to write runbooks (default: active_incidents)
```

---

## mttr_calculator.py

Computes MTTR, MTTD from an incident log JSON file.

```bash
python scripts/mttr_calculator.py --log examples/sample_incidents.json
```

```
==================================================
INCIDENT METRICS REPORT
==================================================

Overall (8 incidents, 8 resolved)
  Avg MTTD   : 10.4 min
  Median MTTD: 7.0 min
  Avg MTTR   : 71.4 min
  Median MTTR: 56.5 min
  p95 MTTR   : 157.0 min

By Severity:
  CRITICAL   count=2  avg_mttr=90.5 min  median=90.5 min
  HIGH       count=3  avg_mttr=75.7 min  median=57.0 min
  MEDIUM     count=2  avg_mttr=47.5 min  median=47.5 min
  LOW        count=1  avg_mttr=40.0 min  median=40.0 min
```

Incident log format (see `examples/sample_incidents.json`):
```json
{
  "id": "INC-20240115-1423",
  "severity": "HIGH",
  "description": "...",
  "started_at": "2024-01-15T14:10:00Z",
  "detected_at": "2024-01-15T14:23:00Z",
  "resolved_at": "2024-01-15T15:47:00Z",
  "root_cause": "...",
  "postmortem": true
}
```

---

## Templates

| Template | When to use |
|----------|-------------|
| `incident_runbook.md` | Live incident — tracks timeline, findings, comms |
| `postmortem.md` | After resolution — blameless, action-item focused |
| `comms_template.md` | Slack/email drafts for stakeholder updates |
| `oncall_handoff.md` | Shift handoff — active incidents, things to watch |

The postmortem template has a "where we got lucky" section that most templates skip. I find that's often where the most useful signal lives.

---

## Configuration

Copy `config.yaml` and edit for your team. Sensitive values (webhook URLs, email DLs) should come from environment variables — the config references env var names, not values.

```yaml
defaults:
  service: "my-platform"
  declared_by: "oncall-eng"

notifications:
  slack:
    critical_channel: "#incidents-critical"
    webhook_env_var: "SLACK_WEBHOOK_URL"
  email:
    critical_dl: "sre-critical@company.com"
```

---

## Requirements

```
python >= 3.8
pyyaml
```

No other dependencies. Intentional — this should run anywhere without a virtualenv dance.

---

## Contributing

If you find something wrong or have a better template pattern, open an issue. Especially interested in:
- Additional classifier rules for common failure modes
- Postmortem template improvements
- Integration examples (PagerDuty webhook → auto-classify)

---

## License

MIT
