#!/usr/bin/env python3
"""gate.py - one command, all checks. Exit 1 means do not post.

Runs:
  qa.py           resolution, fps, duration, audio, yuv420p, loudness
  contactsheet.py 24-frame grid + static-frame (pacing) detection
  stills.py       key-timestamp stills + blank detection
  claims.py       script numbers vs source of truth

Any check that fails makes the whole gate fail. Skipped checks are reported,
never silently passed.
"""
import argparse
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SHOT_ROW = re.compile(r"^\|\s*(\d+)\s*\|\s*([\d.]+)\s*\|\s*([\d.]+)\s*\|")


def run(script, args, label):
    cmd = [sys.executable, os.path.join(HERE, script)] + args
    print(f"\n--- {label} ---")
    r = subprocess.run(cmd)
    return r.returncode == 0


def still_times(brief):
    try:
        with open(brief, encoding="utf-8", errors="replace") as f:
            starts = [float(m.group(2)) for line in f
                      if (m := SHOT_ROW.match(line.strip()))]
    except OSError:
        starts = []
    starts = sorted(set(starts))
    return ",".join(f"{t:.2f}" for t in starts[:10]) if starts else "0,1.5,3,6,10"


def main():
    p = argparse.ArgumentParser(description="Run every gate check on a rendered video.")
    p.add_argument("--video", required=True)
    p.add_argument("--brief", default=None, help="brief.md (used for still timestamps)")
    p.add_argument("--script", default=None, help="narration text for the claims check")
    p.add_argument("--source", default=None,
                   help="source-of-truth file (defaults to the brief if it has a claims table)")
    p.add_argument("--width", type=int, default=1080)
    p.add_argument("--height", type=int, default=1920)
    p.add_argument("--skip", default="", help="comma list: qa,sheet,stills,claims")
    p.add_argument("--warn-claims", action="store_true")
    a = p.parse_args()

    if not os.path.exists(a.video):
        raise SystemExit(f"no such file: {a.video}")

    skip = {s.strip() for s in a.skip.split(",") if s.strip()}
    results = {}

    if "qa" not in skip:
        results["qa"] = run("qa.py", ["--video", a.video, "--width", str(a.width),
                                      "--height", str(a.height)], "qa")
    if "sheet" not in skip:
        results["contactsheet"] = run("contactsheet.py", ["--video", a.video], "contactsheet")
    if "stills" not in skip:
        at = still_times(a.brief) if a.brief else "0,1.5,3,6,10"
        results["stills"] = run("stills.py", ["--video", a.video, "--at", at], "stills")
    if "claims" not in skip and a.script and (a.source or a.brief):
        args = ["--script", a.script, "--source", a.source or a.brief]
        if a.warn_claims:
            args.append("--warn-only")
        results["claims"] = run("claims.py", args, "claims")

    print("\n================ GATE SUMMARY ================")
    for k, ok in results.items():
        print(f"  {'PASS' if ok else 'FAIL'}  {k}")
    for key, skip_key in (("qa", "qa"), ("contactsheet", "sheet"),
                          ("stills", "stills"), ("claims", "claims")):
        if key not in results and skip_key not in skip:
            print(f"  SKIP  {key} (no input supplied)")

    passed = all(results.values()) and bool(results)
    print("==============================================")
    print("VERDICT: " + ("PASS - safe to post" if passed else "FAIL - do not post"))
    return 0 if passed else 1


if __name__ == "__main__":
    sys.exit(main())
