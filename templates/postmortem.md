# Postmortem — {{INCIDENT_ID}}

> Blameless. We're here to learn what happened and prevent recurrence,
> not to assign fault. Systems fail. The goal is to make them fail less.

---

## Summary

| Field            | Value             |
|------------------|-------------------|
| **Incident ID**  | {{INCIDENT_ID}}   |
| **Severity**     | {{SEVERITY}}      |
| **Date**         |                   |
| **Duration**     |                   |
| **Author**       |                   |
| **Reviewers**    |                   |
| **Status**       | Draft / In Review / Final |

**One-paragraph summary:**
< What happened, what was the impact, how was it resolved. Write this last. >

---

## Impact

- **Duration:** < start > to < end > (X hours Y minutes)
- **Users affected:** < number or estimate >
- **Error rate during incident:** < % >
- **Requests impacted:** < approximate count >
- **Revenue/SLA impact:** < if applicable >

---

## Timeline

*All times UTC. Be specific — "around noon" is not useful for a postmortem.*

| Time       | Event |
|------------|-------|
|            | First sign of the issue (alert fired / customer report) |
|            | Engineer paged / incident declared |
|            | Investigation started |
|            | Root cause identified |
|            | Mitigation applied |
|            | Service recovered |
|            | Incident closed |

---

## Root Cause

< One clear sentence. Not "the server crashed" — why did it crash? >

### Contributing factors

*These are systems/processes that made the impact worse, not the root cause itself.*

1.
2.
3.

---

## What went well

*Be genuine here. Acknowledging what worked helps reinforce good practices.*

-
-
-

## What went poorly

*Also be genuine. This is not a blame list — it's a process improvement list.*

-
-
-

## Where we got lucky

*The honest section most postmortems skip. Did something happen to limit the blast radius that we can't rely on next time?*

-
-

---

## Action Items

| Action | Owner | Due Date | Priority |
|--------|-------|----------|----------|
| | | | |
| | | | |
| | | | |

*Action items without owners and due dates don't get done. Assign them before this postmortem is closed.*

---

## Detection

- **How was this detected?** < alert / customer report / monitoring >
- **How long between incident start and detection?** < minutes >
- **Could detection have been faster?** < yes/no and how >

---

## Lessons Learned

< 3–5 sentences on what the team learned. Write this for a new engineer who joins 6 months from now. >

---

*Postmortem should be completed within 5 business days of incident resolution.*
*Share with the broader engineering team once finalized.*
