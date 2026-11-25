# 09 — The retention loop

This is the part that turns a pipeline into a system that improves. Everything else automates production; this automates *judgment*.

Once a week, not daily.

## What to read

From each platform's analytics, per video:

- **retention at 3 seconds** — the hook's score
- **retention curve** — percentage watching at each timestamp
- **the biggest single drop** — where you lost the most people at once
- drop timestamp → which shot was on screen

Retention at 3s is the only metric that reliably predicts a video's total reach. Views, likes and saves are consequences.

## The weekly ritual

1. Export the retention curve for every video posted in the last 7 days.
2. Run `python scripts/retention.py --csv data/retention.csv --brief briefs/EP012.md`.
3. It flags every interval that lost more than 8 points, and maps each to the shot number from your brief's shot list.
4. Look at what those shots have in common. Not the topic — the *pattern*: a wide static shot, a talking-head beat, a logo, a slow zoom, a text wall.
5. Rewrite next week's brief to remove that pattern and double whatever held people.

## Reading a drop

| Symptom | Likely cause | Fix |
|---|---|---|
| big drop in first 1.5s | hook promised something the video is not | change hook family, not wording |
| steady decline after 8s | pacing flattened; no new events | add a visual event every 0.5s |
| cliff at one timestamp | one shot is boring or confusing | cut or replace that shot type |
| drop at the end | end card too long or CTA weak | shorten to one beat |
| flat high retention, low views | format is good, distribution is wrong | posting time, platform, cover frame |

Notice that "views low" with good retention is a *distribution* problem and "views high" with a cliff is a *content* problem. They have completely different fixes and are constantly confused.

## Feeding it back

The output of this loop is not a report. It is **rewritten briefs**.

Concretely, at the end of each week:

- Add the top 3 holding shot patterns to a "keep" list at the top of the series bible.
- Add the top 3 dropping patterns to the avoid list in the brief template.
- Update the hook family ranked by retention at 3s.
- Retire any component whose videos are consistently under the page median.

Then the next five briefs start from evidence instead of from taste. That is the entire difference between a content page and a content *system*.

## Kill, hold, scale

Recompute monthly, using installs per 1k views and cost per install:

- **Scale** — beats page median by 2× on installs per 1k views → 3× output next cycle.
- **Hold** — within range → keep volume, test one hook family change.
- **Kill** — below 0.5% link CTR over its last 20 videos, or cost per install above value → stop, archive the style.

Write the decision down with the date. Decisions that live in your head get reversed by mood.

## The honest limit

This loop makes the *content* better. It cannot make the *offer* work. If installs are low because the app's landing page is bad, no amount of retention analysis will show you that — the chain in `08-attribution.md` will. Read the chain first, then reach for this file.

## Minimum viable version

If you do nothing else from this file, do this: **once a week, look at the 3-second retention of every video, and write down the best and worst hook.** Five minutes. It compounds faster than every other habit in the repo.
