#!/usr/bin/env python3
"""qa.py - technical gate: resolution, fps, duration, audio presence, loudness.

Exit 0 = pass, 1 = fail. Use --json for machine-readable output.
Requires ffprobe and ffmpeg on PATH.
"""
import argparse
import json
import re
import subprocess
import sys


def run(cmd):
    return subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")


def probe(path):
    r = run(["ffprobe", "-v", "error", "-print_format", "json",
             "-show_format", "-show_streams", path])
    if r.returncode != 0:
        raise SystemExit("ffprobe failed: " + r.stderr.strip())
    return json.loads(r.stdout)


def parse_fps(rate):
    try:
        num, den = rate.split("/")
        den = float(den)
        return float(num) / den if den else 0.0
    except (ValueError, AttributeError):
        return 0.0


def integrated_loudness(path):
    r = run(["ffmpeg", "-nostats", "-hide_banner", "-i", path,
             "-af", "ebur128=framelog=verbose", "-f", "null", "-"])
    hits = re.findall(r"I:\s*(-?\d+(?:\.\d+)?)\s*LUFS", r.stderr or "")
    return float(hits[-1]) if hits else None


def main():
    p = argparse.ArgumentParser(description="Technical QA gate for a rendered video.")
    p.add_argument("--video", required=True)
    p.add_argument("--width", type=int, default=1080)
    p.add_argument("--height", type=int, default=1920)
    p.add_argument("--fps", type=float, default=30.0, help="expected fps (default 30)")
    p.add_argument("--fps-tol", type=float, default=0.5)
    p.add_argument("--min-dur", type=float, default=8.0)
    p.add_argument("--max-dur", type=float, default=90.0)
    p.add_argument("--lufs", type=float, default=-16.0, help="target integrated loudness")
    p.add_argument("--lufs-tol", type=float, default=2.5)
    p.add_argument("--json", action="store_true")
    a = p.parse_args()

    info = probe(a.video)
    streams = info.get("streams", [])
    v = next((s for s in streams if s.get("codec_type") == "video"), None)
    aud = next((s for s in streams if s.get("codec_type") == "audio"), None)
    fmt = info.get("format", {})

    results = []

    def check(name, ok, detail):
        results.append({"check": name, "ok": bool(ok), "detail": detail})

    if not v:
        check("video stream", False, "no video stream")
        width = height = fps = 0.0
    else:
        width, height = int(v.get("width", 0)), int(v.get("height", 0))
        fps = parse_fps(v.get("r_frame_rate", "0/1"))
        check("video stream", True, f"{v.get('codec_name')} {width}x{height} @ {fps:.2f}fps")

    check("resolution", (width, height) == (a.width, a.height),
          f"got {width}x{height}, want {a.width}x{a.height}")

    fps_ok = abs(fps - a.fps) <= a.fps_tol
    check("frame rate", fps_ok, f"got {fps:.2f}, want {a.fps:.2f} +/-{a.fps_tol}")

    try:
        dur = float(fmt.get("duration", 0) or 0)
    except ValueError:
        dur = 0.0
    check("duration range", a.min_dur <= dur <= a.max_dur,
          f"{dur:.2f}s, want {a.min_dur}-{a.max_dur}s")

    check("audio track", aud is not None,
          f"{aud.get('codec_name')} {aud.get('channels')}ch" if aud else "missing")

    # pixel format matters for platform compatibility
    pix = (v or {}).get("pix_fmt", "")
    check("yuv420p", pix == "yuv420p", f"got {pix}")

    lufs = integrated_loudness(a.video) if aud else None
    if lufs is None:
        check("loudness", False, "could not measure")
    else:
        check("loudness", abs(lufs - a.lufs) <= a.lufs_tol,
              f"{lufs:.1f} LUFS, want {a.lufs} +/-{a.lufs_tol}")

    failed = [r for r in results if not r["ok"]]

    if a.json:
        print(json.dumps({"video": a.video, "pass": not failed,
                          "duration_s": round(dur, 2), "results": results}, indent=2))
    else:
        for r in results:
            print(("PASS  " if r["ok"] else "FAIL  ") + f"{r['check']:<16} {r['detail']}")
        print()
        print("GATE: " + ("PASS" if not failed else f"FAIL ({len(failed)} check(s))"))

    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
