#!/usr/bin/env python3
"""contactsheet.py - 24-frame contact sheet + pacing similarity check.

Two jobs, one ffmpeg pass:

1. PACING - sample the video densely (default 60 samples) and flag adjacent
   samples that are near-identical. Two alike samples mean nothing moved for
   at least that interval: a pacing failure, not a style choice.
2. REVIEW - build a labelled 24-frame grid a human can read in one glance.

Dense sampling is what makes the 1-second pacing bar measurable: a 24-frame
sheet only resolves ~1.25s per cell and would miss short stalls.

Exit 0 = pass, 1 = pacing failure. Requires ffmpeg, pillow.
"""
import argparse
import glob
import os
import shutil
import subprocess
import sys
import tempfile

from PIL import Image, ImageDraw, ImageStat

COLS, ROWS = 6, 4


def duration(path):
    r = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=nw=1:nk=1", path],
        capture_output=True, text=True)
    try:
        return float(r.stdout.strip())
    except ValueError:
        raise SystemExit("could not read duration")


def extract(path, dur, n, outdir):
    """One ffmpeg pass -> n evenly spaced frames."""
    os.makedirs(outdir, exist_ok=True)
    fps = max(n / dur, 0.01)
    subprocess.run(
        ["ffmpeg", "-nostats", "-loglevel", "error", "-i", path,
         "-vf", f"fps={fps:.6f}", "-q:v", "2", "-y",
         os.path.join(outdir, "%05d.png")],
        check=True, capture_output=True)
    files = sorted(glob.glob(os.path.join(outdir, "*.png")))
    times = [(dur * (i + 0.5) / len(files)) if files else 0.0 for i in range(len(files))]
    return files, times


def sig(img, size=16):
    """Colour signature. Grayscale would score a red->blue cut as zero change."""
    return img.convert("RGB").resize((size, size), Image.Resampling.BILINEAR)


def mad(a, b):
    from PIL import ImageChops
    diff = ImageChops.difference(a, b)
    return sum(ImageStat.Stat(diff).mean) / 3.0


def make_sheet(items, out):
    cell_w, cell_h, pad, label = 180, 320, 4, 14
    cols = COLS
    rows = (len(items) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * (cell_w + pad) + pad,
                              rows * (cell_h + label + pad) + pad), (18, 18, 18))
    draw = ImageDraw.Draw(sheet)
    for i, (t, img) in enumerate(items):
        r, c = divmod(i, cols)
        thumb = img.copy()
        thumb.thumbnail((cell_w, cell_h), Image.Resampling.LANCZOS)
        x = pad + c * (cell_w + pad)
        y = pad + r * (cell_h + label + pad)
        sheet.paste(thumb, (x, y))
        draw.text((x + 2, y + cell_h + 1), f"{t:5.1f}s", fill=(200, 200, 200))
    os.makedirs(os.path.dirname(out) or ".", exist_ok=True)
    sheet.save(out, quality=88)


def main():
    p = argparse.ArgumentParser(description="Contact sheet + pacing gate.")
    p.add_argument("--video", required=True)
    p.add_argument("--out", default="out/contactsheet.jpg")
    p.add_argument("--frames", type=int, default=COLS * ROWS,
                   help="frames in the visual sheet")
    p.add_argument("--metric-frames", type=int, default=60,
                   help="dense samples for pacing; needs >1/s to see a 1s stall")
    p.add_argument("--static-thresh", type=float, default=3.0,
                   help="mean abs gray diff below this counts as static (0-255)")
    p.add_argument("--max-static", type=int, default=1,
                   help="near-static adjacent pairs tolerated")
    a = p.parse_args()

    dur = duration(a.video)
    tmp = tempfile.mkdtemp(prefix="shotgate_")
    try:
        files, times = extract(a.video, dur, max(a.metric_frames, 2), tmp)
        if not files:
            raise SystemExit("no frames extracted")
        imgs = [Image.open(f).convert("RGB") for f in files]
        sigs = [sig(i) for i in imgs]

        static_pairs = []
        for i in range(1, len(sigs)):
            d = mad(sigs[i - 1], sigs[i])
            if d < a.static_thresh:
                static_pairs.append((times[i - 1], times[i], round(d, 2)))

        blanks = [(round(t, 2), round(ImageStat.Stat(i.convert("L")).stddev[0], 1))
                  for t, i in zip(times, imgs)
                  if ImageStat.Stat(i.convert("L")).stddev[0] < 2.0]

        # pick evenly spaced frames for the visual sheet
        n_sheet = min(a.frames, len(imgs))
        idx = [round(i * (len(imgs) - 1) / max(n_sheet - 1, 1)) for i in range(n_sheet)]
        make_sheet([(times[i], imgs[i]) for i in idx], a.out)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    print(f"contact sheet -> {a.out}  ({n_sheet} frames, {dur:.2f}s)")
    print(f"pacing samples: {len(imgs)} over {dur:.2f}s "
          f"(~{dur / max(len(imgs), 1):.2f}s apart)")
    if static_pairs:
        print(f"STATIC PAIRS ({len(static_pairs)}):")
        for t1, t2, d in static_pairs:
            print(f"  {t1:6.2f}s ~ {t2:6.2f}s   diff={d}")
    else:
        print("STATIC PAIRS: none")
    if blanks:
        print(f"BLANK FRAMES: {blanks}")

    failed = len(static_pairs) > a.max_static or bool(blanks)
    print("GATE: " + ("PASS" if not failed else "FAIL (pacing)"))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
