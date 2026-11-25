#!/usr/bin/env python3
"""cost.py - roll up the video log into unit economics.

Answers the only cost questions that matter:
  cost per video, cost per 1k views, cost per install, and margin.

Reads templates/video-log.csv (or your own copy). Missing columns are
treated as zero, so partial logs still work.
"""
import argparse
import csv
import sys
from collections import defaultdict


def num(v):
    try:
        return float(str(v).replace(",", "").strip())
    except (ValueError, AttributeError):
        return 0.0


def load(path):
    rows = []
    with open(path, newline="", encoding="utf-8", errors="replace") as f:
        for r in csv.DictReader(f):
            rows.append({
                "id": (r.get("video_id") or "?").strip(),
                "page": (r.get("page") or "").strip(),
                "format": (r.get("format") or "").strip(),
                "cost": num(r.get("cost_usd")),
                "views": num(r.get("views")),
                "clicks": num(r.get("link_clicks")),
                "installs": num(r.get("installs")),
                "revenue": num(r.get("revenue_usd")),
            })
    return rows


def safe_div(a, b):
    return a / b if b else 0.0


def report(label, rows):
    cost = sum(r["cost"] for r in rows)
    views = sum(r["views"] for r in rows)
    clicks = sum(r["clicks"] for r in rows)
    installs = sum(r["installs"] for r in rows)
    revenue = sum(r["revenue"] for r in rows)
    print(f"\n== {label} ==  n={len(rows)}")
    print(f"  cost total        ${cost:,.2f}")
    print(f"  cost / video      ${safe_div(cost, len(rows)):,.2f}")
    print(f"  views total       {views:,.0f}")
    print(f"  cost / 1k views   ${safe_div(cost, views / 1000):,.2f}")
    print(f"  link CTR          {safe_div(clicks, views) * 100:.2f}%")
    print(f"  installs          {installs:,.0f}")
    print(f"  cost / install    ${safe_div(cost, installs):,.2f}")
    print(f"  revenue           ${revenue:,.2f}")
    print(f"  margin            {safe_div(revenue - cost, cost) * 100:+.0f}%"
          if cost else "  margin            n/a")


def main():
    p = argparse.ArgumentParser(description="Unit economics from the video log.")
    p.add_argument("--log", required=True)
    p.add_argument("--by", choices=["page", "format"], default=None,
                   help="also break down by this column")
    a = p.parse_args()

    rows = load(a.log)
    if not rows:
        raise SystemExit("no rows")

    report("ALL", rows)

    if a.by:
        groups = defaultdict(list)
        for r in rows:
            groups[r[a.by] or "(blank)"].append(r)
        for key in sorted(groups):
            report(f"{a.by}={key}", groups[key])

    worst = sorted(rows, key=lambda r: -safe_div(r["cost"], r["installs"] or 1e-9))[:3]
    print("\n== most expensive per install ==")
    for r in worst:
        cpi = safe_div(r["cost"], r["installs"])
        print(f"  {r['id']:<10} ${cpi:,.2f}/install   cost ${r['cost']:.2f}  installs {r['installs']:.0f}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
