# Stakeholder Comms Templates

Use these for Slack messages and emails during an active incident.
Keep updates factual. Don't speculate on cause until you know.
Avoid percentages unless you're confident in the number.

---

## Initial notification

### Slack

```
:red_circle: We are currently investigating an issue affecting [FEATURE/SERVICE].
Users may experience [SYMPTOM — e.g. slow load times / login failures / errors].
Our team is actively working on this. Next update in 30 minutes.
— [YOUR NAME], SRE
```

### Email

```
Subject: [Investigating] Issue with [SERVICE] — [DATE]

Team,

We are currently investigating an issue with [SERVICE].

Impact: [WHAT USERS ARE SEEING]
Status: Under investigation
Next update: [TIME]

We will provide updates every 30 minutes until resolved.

— [YOUR NAME]
Engineering / SRE
```

---

## Progress update (every 30 min for CRITICAL, 1hr for HIGH)

### Slack

```
:large_yellow_circle: Update on [INCIDENT ID] — [TIME UTC]
Status: Still investigating / Mitigation in progress
Finding so far: [ONE SENTENCE — factual only]
ETA: [Time if known, "under investigation" if not]
Next update: [TIME]
```

### Email

```
Subject: [Update] Issue with [SERVICE] — [TIME]

Team,

Update on the ongoing incident with [SERVICE].

Current status : [Investigating / Mitigating / Monitoring]
Finding so far : [What you know — factual, no speculation]
User impact    : [Still affected / Partially restored / Monitoring]
Next update    : [TIME]

— [YOUR NAME]
```

---

## Resolution

### Slack

```
:white_check_mark: Resolved — [INCIDENT ID]
[SERVICE] is fully restored as of [TIME UTC].
Duration: [X hours Y minutes]
Impact: [Brief summary]
A postmortem will follow within 5 business days.
Thank you for your patience.
```

### Email

```
Subject: [Resolved] Issue with [SERVICE] — [DATE]

Team,

The incident affecting [SERVICE] has been resolved.

Resolved at   : [TIME UTC]
Total duration: [X hours Y minutes]
Root cause    : [Brief — 1 sentence. Or "TBD — postmortem in progress"]
Current status: Service fully restored and stable

A postmortem will be shared with the team within 5 business days.

— [YOUR NAME]
Engineering / SRE
```

---

## Executive summary (for VP/C-level — after resolution)

```
Subject: Incident Summary — [SERVICE] — [DATE]

[EXEC NAME],

Brief summary of today's incident.

What happened : [1–2 sentences — plain English, no jargon]
Duration      : [X hours]
User impact   : [Approximate number of users or % affected]
Resolution    : [What fixed it]
Prevention    : [Top action item to prevent recurrence]

Full postmortem available on request.

— [YOUR NAME]
```

---

*Notes:*
- *Never send a comms update that says "we don't know what's happening" — say "we are actively investigating" instead*
- *Don't promise ETAs unless you're confident. "Under investigation" is better than a missed ETA*
- *Always include a next-update time — it stops people from pinging you every 5 minutes*
