# shotgate

**A faceless short-form video pipeline where the gate is the product.**

Most AI video workflows automate rendering and leave judgment to vibes. Shotgate does the opposite of what's fashionable: it treats production as the cheap, commoditised half, and puts the engineering effort into the two things that actually decide whether a page works — a **brief the model cannot drift from**, and an **automated gate that refuses to let a broken video get posted**.

```
FORMAT → BRIEF → RENDER → GATE → POST → LEARN ↺
  ↑__________________________________________|
```

## Why this exists

The published playbooks stop at "Claude writes the video as code, Playwright captures frames, ffmpeg encodes it." That is real and it is reproducible — which is exactly why it is worth nothing as a differentiator. What almost nobody ships is:

- a deterministic **claims linter** that checks every number on screen against a source-of-truth file
- a **pacing check** that flags repeated frames, so slow videos are caught before posting, not after
- a **loudness gate** so your video isn't 6dB quiet next to everything else in the feed
- **per-video attribution**, so you learn which video produced installs instead of which page did
- a **retention → brief** loop that rewrites next week's scripts from where people actually left

These are the parts that are boring, unglamorous, easy to verify, and hard to fake. They are the product.

## What it does not do

- It does not render video. Rendering is a commodity — route it per shot, see `reference/03-renderers.md`.
- It does not write your creative direction. Somebody still has to choose the format and approve a script. Budget three minutes per video for that.
- It does not guarantee reach. Platform policy, account health and algorithmic luck are outside anyone's control.

## Install

```bash
git clone https://github.com/fenomenoo/shotgate.git
cd shotgate
pip install pillow
# ffmpeg + ffprobe must be on PATH
```

Python 3.9+. No other dependencies. No API keys.

### As a Claude skill

Clone it into your skills directory so Claude picks it up automatically:

```bash
git clone https://github.com/fenomenoo/shotgate.git ~/.claude/skills/shotgate
```

Claude will then load `SKILL.md` and the reference files whenever you ask it to plan, build or QA short-form video content.

## Use

```bash
# One command, all checks, exit code 1 means do not post
python scripts/gate.py --video out/EP012.mp4 --brief briefs/EP012.md --script out/EP012.txt
```

Individual checks:

```bash
python scripts/qa.py          --video out/EP012.mp4 --width 1080 --height 1920
python scripts/contactsheet.py --video out/EP012.mp4 --out out/sheet.jpg
python scripts/stills.py      --video out/EP012.mp4 --at 0,1.5,4,8,15
python scripts/claims.py      --script out/EP012.txt --source briefs/EP012.md
python scripts/retention.py   --csv data/retention.csv --brief briefs/EP012.md
python scripts/cost.py        --log data/video-log.csv
```

## The three rules that matter

1. **Nothing posts that the gate has not passed.**
2. **No number on screen that is not in the source-of-truth file.**
3. **One link per video, not per page.**

## Structure

```
reference/   the thinking — format choice, brief spec, renderers, hooks, cost, compliance, attribution, retention
templates/   brief, series bible, source of truth, video log
scripts/     the gate and its checks
```

## Credit

The deterministic-render pipeline idea (HTML frame → headless capture → ffmpeg) is not mine and predates this repo. The pipeline is commodity. The gate, the claims linter, the pacing check and the retention loop are the contribution.

## License

MIT
