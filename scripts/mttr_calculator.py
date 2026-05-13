#!/usr/bin/env python3
"""
mttr_calculator.py — compute MTTR, MTTD, MTTF from an incident log

Expects a JSON file with incident records (see examples/sample_incidents.json).
Outputs summary stats and per-severity breakdown.

Usage:
    python scripts/mttr_calculator.py --log examples/sample_incidents.json
    python scripts/mttr_calculator.py --log examples/sample_incidents.json --output report.json
    python scripts/mttr_calculator.py --log examples/sample_incidents.json --since 2024-01-01
"""

import argparse
import json
import sys
import os
from datetime import datetime, timezone
from collections import defaultdict
from statistics import mean, median


def load_log(path):
    with open(path) as f:
        return json.load(f)


def parse_ts(ts_str):
    # handle both Z and +00:00 suffix
    ts_str = ts_str.replace("Z", "+00:00")
    return datetime.fromisoformat(ts_str)


def compute_duration_minutes(start_str, end_str):
    if not start_str or not end_str:
        return None
    start = parse_ts(start_str)
    end = parse_ts(end_str)
    delta = (end - start).total_seconds() / 60
    return round(delta, 1)


def filter_since(incidents, since_str):
    if not since_str:
        return incidents
    cutoff = parse_ts(since_str + "T00:00:00+00:00")
    return [i for i in incidents if parse_ts(i["detected_at"]) >= cutoff]


def summarize(incidents):
    """
    Returns overall stats and per-severity breakdown.
    Only counts resolved incidents for MTTR — open ones skew numbers.
    """
    resolved = [i for i in incidents if i.get("resolved_at")]
    by_severity = defaultdict(list)

    mttd_vals, mttr_vals = [], []

    for inc in resolved:
        # MTTD = detected_at - started_at (how long before we knew)
        mttd = compute_duration_minutes(inc.get("started_at"), inc.get("detected_at"))
        # MTTR = resolved_at - started_at (total time to recover)
        mttr = compute_duration_minutes(inc.get("started_at"), inc.get("resolved_at"))

        if mttd is not None:
            mttd_vals.append(mttd)
            inc["_mttd_min"] = mttd
        if mttr is not None:
            mttr_vals.append(mttr)
            inc["_mttr_min"] = mttr

        sev = inc.get("severity", "UNKNOWN")
        by_severity[sev].append(inc)

    overall = {
        "total_incidents": len(incidents),
        "resolved": len(resolved),
        "open": len(incidents) - len(resolved),
        "avg_mttd_min": round(mean(mttd_vals), 1) if mttd_vals else None,
        "median_mttd_min": round(median(mttd_vals), 1) if mttd_vals else None,
        "avg_mttr_min": round(mean(mttr_vals), 1) if mttr_vals else None,
        "median_mttr_min": round(median(mttr_vals), 1) if mttr_vals else None,
        "p95_mttr_min": sorted(mttr_vals)[int(len(mttr_vals) * 0.95)] if mttr_vals else None,
    }

    per_severity = {}
    for sev, incs in by_severity.items():
        mttr_s = [i["_mttr_min"] for i in incs if "_mttr_min" in i]
        per_severity[sev] = {
            "count": len(incs),
            "avg_mttr_min": round(mean(mttr_s), 1) if mttr_s else None,
            "median_mttr_min": round(median(mttr_s), 1) if mttr_s else None,
        }

    return overall, per_severity


def print_report(overall, per_severity, since=None):
    print("\n" + "=" * 50)
    print("INCIDENT METRICS REPORT")
    if since:
        print(f"Since: {since}")
    print("=" * 50)

    print(f"\nOverall ({overall['total_incidents']} incidents, {overall['resolved']} resolved)")
    print(f"  Avg MTTD   : {overall['avg_mttd_min']} min")
    print(f"  Median MTTD: {overall['median_mttd_min']} min")
    print(f"  Avg MTTR   : {overall['avg_mttr_min']} min")
    print(f"  Median MTTR: {overall['median_mttr_min']} min")
    print(f"  p95 MTTR   : {overall['p95_mttr_min']} min")
    if overall["open"]:
        print(f"  Open       : {overall['open']} (excluded from MTTR)")

    print("\nBy Severity:")
    for sev in ["CRITICAL", "HIGH", "MEDIUM", "LOW"]:
        if sev not in per_severity:
            continue
        s = per_severity[sev]
        print(f"  {sev:<10} count={s['count']}  avg_mttr={s['avg_mttr_min']} min  median={s['median_mttr_min']} min")

    print()


def main():
    parser = argparse.ArgumentParser(description="Compute MTTR/MTTD from incident log")
    parser.add_argument("--log", required=True, help="Path to incident JSON log")
    parser.add_argument("--output", default=None, help="Write JSON report to file")
    parser.add_argument("--since", default=None, help="Filter incidents from date (YYYY-MM-DD)")
    args = parser.parse_args()

    if not os.path.exists(args.log):
        print(f"[error] log file not found: {args.log}")
        sys.exit(1)

    incidents = load_log(args.log)
    incidents = filter_since(incidents, args.since)

    if not incidents:
        print("[warn] no incidents found after filtering")
        sys.exit(0)

    overall, per_severity = summarize(incidents)
    print_report(overall, per_severity, since=args.since)

    if args.output:
        report = {"overall": overall, "by_severity": per_severity}
        with open(args.output, "w") as f:
            json.dump(report, f, indent=2)
        print(f"[ok] JSON report written to {args.output}")


if __name__ == "__main__":
    main()
