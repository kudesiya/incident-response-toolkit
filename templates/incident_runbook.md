# Incident Runbook — {{INCIDENT_ID}}

| Field            | Value                        |
|------------------|------------------------------|
| **Incident ID**  | {{INCIDENT_ID}}              |
| **Severity**     | {{SEVERITY}}                 |
| **Declared at**  | {{TIMESTAMP}}                |
| **Declared by**  | {{DECLARED_BY}}              |
| **Service**      | {{SERVICE}}                  |
| **Bridge**       | {{REQUIRES_BRIDGE}}          |
| **Notify**       | {{NOTIFY}}                   |
| **Response SLA** | {{RESPONSE_TIME_MIN}} min    |

---

## What's happening

{{DESCRIPTION}}

*Classified because:* {{CLASSIFIED_BY}}

---

## Impact

- **Users affected:** < estimate or unknown >
- **Features affected:** < list >
- **Revenue/data impact:** < yes / no / unknown >
- **Regions/environments:** < prod / specific region >

---

## Timeline

| Time (UTC) | Update |
|------------|--------|
| {{TIMESTAMP}} | Incident declared |
| | |
| | |

*Keep this updated every 30 min for CRITICAL/HIGH.*

---

## Investigation

### What we checked

- [ ] Dashboards reviewed — Datadog / Grafana
- [ ] Recent deployments in last 2h — check CI/CD
- [ ] Upstream dependencies — third party status pages
- [ ] Infrastructure health — AWS console / EKS
- [ ] Database performance — slow query logs
- [ ] Error logs — Splunk / CloudWatch

### Findings

< paste relevant log snippets, dashboard screenshots, or notes here >

---

## Mitigation steps

1. < first thing tried >
2. < second thing tried >
3.

---

## Resolution

- **Resolved at:** < timestamp >
- **Root cause:** < fill in after resolution >
- **Fix applied:** < what was done >
- **Postmortem needed:** < yes / no >
- **Postmortem owner:** < name >

---

## Comms sent

- [ ] Slack — #incidents
- [ ] Email — oncall DL
- [ ] Status page updated
- [ ] Stakeholders notified

---

*Archive this file to `closed_incidents/` once resolved.*
