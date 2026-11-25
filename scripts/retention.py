#!/usr/bin/env python3
"""retention.py - find where people leave, and which shot was on screen.

Reads a retention CSV and flags every interval that lost more than a
threshold of the remaining audience. If a brief is supplied, maps each drop
to the shot number from its shot list.

CSV columns: video_id,t,retention
  t          seconds from start
  retention  percentage of viewers still watching (0-100)
Optional column: hook_pattern growth  (enables the hook ranking table)

Exit 0 always (this is analysis, not a gate), unless the file is unusable.
"""
import argparse
import csv
import re
import sys
from collections import defaultdict

SHOT_ROW = re.compile(r"^\|\s*(\d+)\s*\|\s*([\d.]+)\s*\|\s*([\d.]+)\s*\|")


def load(path):
    rows = []
    with open(path, newline="", encoding="utf-8", errors="replace") as f:
        for r in csv.DictReader(f):
            try:
                rows.append({
                    "video": (r.get("video_id") or "").strip(),
                    "t": float(r["t"]),
                    "ret": float(r["retention"]),
                    "hook": (r.get("hook_pattern") or "").strip(),
                })
            except (KeyError, ValueError, TypeError):
                continue
    return rows


def shots(brief):
    out = []
    try:
        with open(brief, encoding="utf-8", errors="replace") as f:
            for line in f:
                m = SHOT_ROW.match(line.strip())
                if m:
                    out.append((int(m.group(1)), float(m.group(2)), float(m.group(3))))
    except OSError:
        pass
    return out


def which_shot(shots_, t):
    for n, start, end in shots_:
        if start <= t < end:
            return n
    return None


def main():
    p = argparse.ArgumentParser(description="Score retention and find the shots that lose people.")
    p.add_argument("--csv", required=True)
    p.add_argument("--brief", default=None, help="brief.md with a shot list table")
    p.add_argument("--drop", type=float, default=8.0,
                   help="flag any interval losing more than this many points")
    a = p.parse_args()

    rows = load(a.csv)
    if not rows:
        raise SystemExit("no usable rows (need video_id,t,retention)")

    table = shots(a.brief) if a.brief else []

    by_video = defaultdict(list)
    for r in rows:
        by_video[r["video"]].append(r)

    flagged_total = 0
    for vid, rs in by_video.items():
        rs.sort(key=lambda x: x["t"])
        print(f"\n== {vid or '(unnamed)'} ==")
        print(f"  ret@3s: {next((x['ret'] for x in rs if x['t'] >= 3), rs[0]['ret']):.1f}%"
              f"   end: {rs[-1]['ret']:.1f}%   points: {len(rs)}")
        for i in range(1, len(rs)):
            drop = rs[i - 1]["ret"] - rs[i]["ret"]
            if drop > a.drop:
                flagged_total += 1
                s = which_shot(table, rs[i]["t"]) if table else None
                where = f"  shot #{s}" if s is not None else ""
                print(f"  DROP {drop:5.1f}u  at {rs[i]['t']:6.1f}s"
                      f"  ({rs[i-1]['ret']:.1f}% -> {rs[i]['ret']:.1f}%){where}")

    # hook ranking
    hooks = defaultdict(list)
    for vid, rs in by_video.items():
        rs.sort(key=lambda x: x["t"])
        h = next((x["hook"] for x in rs if x["hook"]), "")
        r3 = next((x["ret"] for x in rs if x["t"] >= 3), rs[0]["ret"])
        if h:
            hooks[h].append(r3)
    if hooks:
        print("\n== hook ranking (mean retention at 3s) ==")
        for h, vals in sorted(hooks.items(), key=lambda kv: -sum(kv[1]) / len(kv[1])):
            print(f"  {h:<28} {sum(vals)/len(vals):5.1f}%   n={len(vals)}")

    print(f"\nflagged intervals: {flagged_total}")
    print("Look at what the flagged shots have in common - the pattern, not the topic.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
