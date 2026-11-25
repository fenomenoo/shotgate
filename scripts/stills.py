#!/usr/bin/env python3
"""stills.py - extract stills at chosen timestamps for human inspection.

Flags near-blank frames automatically. Readable text, overlaps and cut-off
elements still need eyes: this tool gets a human to the right frames fast.

Exit 0 = pass, 1 = blank frame detected. Requires ffmpeg, pillow.
"""
import argparse
import os
import subprocess
import sys

from PIL import Image, ImageStat


def duration(path):
    r = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=nw=1:nk=1", path],
        capture_output=True, text=True)
    try:
        return float(r.stdout.strip())
    except ValueError:
        raise SystemExit("could not read duration")


def main():
    p = argparse.ArgumentParser(description="Extract stills at key timestamps.")
    p.add_argument("--video", required=True)
    p.add_argument("--at", default="0,1.5,3,6,10",
                   help="comma-separated timestamps in seconds")
    p.add_argument("--outdir", default="out/stills")
    p.add_argument("--blank-stddev", type=float, default=2.0)
    a = p.parse_args()

    dur = duration(a.video)
    os.makedirs(a.outdir, exist_ok=True)

    times = []
    for tok in a.at.split(","):
        tok = tok.strip()
        if not tok:
            continue
        try:
            t = float(tok)
        except ValueError:
            print(f"skip bad timestamp: {tok}")
            continue
        if 0 <= t <= dur:
            times.append(t)
        else:
            print(f"skip out-of-range: {t} (duration {dur:.2f}s)")

    if not times:
        raise SystemExit("no valid timestamps")

    blank = []
    for t in times:
        fp = os.path.join(a.outdir, f"still_{t:06.2f}s.png")
        subprocess.run(
            ["ffmpeg", "-nostats", "-loglevel", "error", "-ss", f"{t:.3f}",
             "-i", a.video, "-frames:v", "1", "-y", fp],
            check=True, capture_output=True)
        if not os.path.exists(fp):
            print(f"MISSING  {t:.2f}s")
            continue
        img = Image.open(fp).convert("L")
        std = ImageStat.Stat(img).stddev[0]
        mean = ImageStat.Stat(img).mean[0]
        flag = ""
        if std < a.blank_stddev:
            flag = "  <- BLANK"
            blank.append(t)
        print(f"{t:6.2f}s  stddev={std:5.1f}  mean={mean:5.1f}{flag}  {fp}")

    print()
    print("GATE: " + ("PASS" if not blank else f"FAIL (blank frames at {blank})"))
    return 1 if blank else 0


if __name__ == "__main__":
    sys.exit(main())
