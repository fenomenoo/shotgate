#!/usr/bin/env python3
"""claims.py - fail the script if any number on screen is not in the source of truth.

This is the check almost nobody implements, and the one that keeps a page
from publishing an invented statistic. It is deterministic: no model involved.

Exit 0 = all numbers traced, 1 = untraced numbers found.

Scope: numbers, percentages, currency and years only. It does NOT check
wording, implied promises or medical/financial claims - see
reference/06-compliance.md for what still needs a human.
"""
import argparse
import re
import sys

NUM = re.compile(r"\d[\d,]*(?:\.\d+)?")
CTX = 40


def numbers(text):
    """Return {value: [positions]} with commas stripped."""
    out = {}
    for m in NUM.finditer(text):
        raw = m.group(0).replace(",", "")
        try:
            val = float(raw)
        except ValueError:
            continue
        out.setdefault(round(val, 3), []).append(m.start())
    return out


def context(text, pos):
    lo = max(0, pos - CTX)
    hi = min(len(text), pos + CTX)
    return " ".join(text[lo:hi].split())


def read(path):
    try:
        with open(path, encoding="utf-8", errors="replace") as f:
            return f.read()
    except OSError as e:
        raise SystemExit(f"cannot read {path}: {e}")


def main():
    p = argparse.ArgumentParser(description="Lint a script against a source-of-truth file.")
    p.add_argument("--script", required=True, help="narration / on-screen text (txt, srt, md)")
    p.add_argument("--source", required=True, help="source-of-truth file (md)")
    p.add_argument("--min-value", type=float, default=10.0,
                   help="ignore numbers below this (ordinals, list indices); 0 = check all")
    p.add_argument("--warn-only", action="store_true", help="never exit 1")
    a = p.parse_args()

    script = read(a.script)
    source = read(a.source)

    src = numbers(source)
    scr = numbers(script)

    missing = []
    for val, positions in sorted(scr.items()):
        if abs(val) < a.min_value:
            continue
        if val not in src:
            missing.append((val, [context(script, pos) for pos in positions[:2]]))

    print(f"source numbers traced: {len(src)}")
    print(f"script numbers:        {len(scr)}")
    if missing:
        print(f"\nUNTRACED ({len(missing)}):")
        for val, ctxs in missing:
            for c in ctxs:
                print(f"  {val:>12}  ...{c}...")
        print("\nAdd these to the source of truth with a citation, or remove them.")
    else:
        print("\nUNTRACED: none")

    ok = not missing
    print("\nGATE: " + ("PASS" if ok else "FAIL (untraced numbers)"))
    if a.warn_only:
        return 0
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
