# Severity Classification Guide

Quick reference for declaring incident severity.
When in doubt, go higher — it's easier to downgrade than to escalate late.

---

## Severity Levels

### CRITICAL
**Wake people up. Start a bridge call. Update every 30 min.**

- Full service outage or near-full
- Authentication / login is broken
- Data loss or data corruption
- Payment processing down
- Availability below 95% on any critical API

Response SLA: **15 minutes**

---

### HIGH
**Page oncall. No bridge required unless it escalates. Update every hour.**

- 5%+ error rate on any customer-facing API
- Significant latency degradation (p99 > 5s)
- A major feature broken for a subset of users
- Database performance severely degraded
- Availability between 95–99%

Response SLA: **30 minutes**

---

### MEDIUM
**Oncall handles during business hours unless it escalates. No bridge.**

- 1–5% error rate
- Latency elevated but not severe (p95 2–3s)
- Non-critical feature degraded
- Workaround exists
- No immediate revenue or data risk

Response SLA: **2 hours**

---

### LOW
**Handle next business day. Ticket it and move on.**

- Cosmetic issues
- Affects single user or very small subset
- Non-production environment
- Known flaky test or alert

Response SLA: **Next business day**

---

## The "When in Doubt" Rule

If you're debating between CRITICAL and HIGH — declare CRITICAL.
If you're debating between HIGH and MEDIUM — declare HIGH.

Downgrading is fast. Slow escalation has real cost.

---

## Common Misclassifications

| Situation | Wrong | Right | Why |
|-----------|-------|-------|-----|
| 3% error rate, 1am | LOW | MEDIUM | Time of day doesn't change severity |
| Login broken for internal users only | MEDIUM | HIGH | Auth systems are blast-radius high |
| Flaky alert, fourth time this week | MEDIUM | LOW + fix the alert | Repeated noise is a reliability debt |
| "We think it might be fixed" | RESOLVED | MEDIUM/monitoring | Don't close until you've confirmed it |

---

## Adjusting thresholds

Default thresholds are in `classifier/rules.yaml`.
Change them to match your actual SLOs — these defaults are starting points.

If your p99 SLO is 3s, set `latency_p99_ms: 3000` for HIGH.
Don't let the defaults drift from your real SLO targets or the classifier becomes noise.
