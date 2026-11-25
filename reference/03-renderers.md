# 03 — Renderer routing

The biggest mistake in faceless video is committing to one renderer and then forcing every idea through it. Code rendering (HTML/CSS/three.js → headless browser → ffmpeg) is superb for some shots and structurally incapable of others. Route **per shot** and assemble on one timeline.

## The routing matrix

| Substrate | Excellent at | Structurally bad at | Determinism | Relative cost |
|---|---|---|---|---|
| **Code render** (HTML/three.js/Remotion → Playwright → ffmpeg) | text, numbers, data-viz, diagrams, motion graphics, UI, transitions, anything with exact typography | character acting, faces, painted texture, cinematic realism, organic motion | full — every frame is a pure function of `t` | low |
| **Generative video** (text/image → video) | cinematic, painterly, texture, atmosphere, stylised worlds | legible text, exact numbers, consistency across shots, precise timing | none — regenerate to change anything | high |
| **Archival / stock** | credibility, real events, real footage, documentary tone | anything specific to your product | full (file is fixed) | low |
| **Screen capture** | proving the product works, workflows, UI detail | emotion, story, abstraction | full if scripted | very low |
| **2D vector / motion** (After Effects-style, code or keyframe) | explainers, icons, infographics, brand consistency | realism, emotion | full | low–medium |

## How to combine

1. **Choose a primary substrate** for the video from `01-format-decision.md`. That is 70–90% of the runtime.
2. **Choose one accent substrate** for at most 20% of shots — usually the hook and the turn. Generative for the cinematic beat, screen capture for the proof beat.
3. **Unify with typography and grade.** One font system, one palette, one LUT. Mixed substrates look intentional when the type and colour are locked; they look cheap when they are not.
4. **Cut on the same beat grid** regardless of substrate. The timeline does not care where a frame came from.

## Why this matters

The published playbooks pick code rendering because it keeps text clean, then quietly accept that they can never make a cinematic or painted video. That is a real ceiling, and it is self-imposed. The fix is not a better renderer — it is refusing to have only one.

The reverse error is just as common: generating everything, then fighting unreadable text and characters that change clothes between shots. Code render for anything that must be exact; generative for anything that must feel like something.

## Determinism rule

Whatever the substrate, the video must be reproducible:

- **Code render:** every frame a pure function of `t`. No `Math.random()` without a fixed seed. No wall-clock reads.
- **Generative:** keep the seed, the prompt, the model version and the settings in the brief. If you cannot reproduce a shot, you cannot fix it — only re-roll it.
- **Capture:** scripted, not improvised. Same clicks, same window size, same state.
- **Archival:** the exact file, with its source URL and licence recorded.

Reproducibility is what makes "fix one shot and re-render" possible. Without it, every fix costs a full rebuild and the quality bar quietly collapses to "good enough, ship it".

## Assembly

```bash
# per-shot renders, then one concat + one audio mix
ffmpeg -f concat -safe 0 -i shots.txt -i mix.wav -c:v libx264 -crf 18 -pix_fmt yuv420p -c:a aac -b:a 192k out/EP012.mp4
```

Encode the final file at **1080×1920, 30fps, yuv420p, CRF 18**. Do not upscale a 720p render — the gate will catch it, and the platforms will punish it.

## Cost note

Generative shots are the expensive ones. Route them to the hook and the turn only, and read `07-cost.md` before you make generative the default. The published figure of ~$158 for one 55s reel at frontier-model prices is an argument for routing, not for avoiding the substrate.
