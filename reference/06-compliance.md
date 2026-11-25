# 06 — Compliance

The fastest way to lose a page that took three months to build is a policy violation or a rights claim. This is the least glamorous file in the repo and the one that most protects the asset.

**This is an operating checklist, not legal advice.** Where money or health claims are involved, get the actual review.

## 1. AI disclosure

Platforms increasingly require disclosure of realistic AI-generated content. Rules change; verify before each campaign rather than trusting this file forever.

Operating rules:

- **Set the AI-generated flag on every upload**, on every platform, by default. Turning it off to look more organic is how accounts get actioned.
- Disclosure is triggered by *realistic* depiction — photoreal people, real places, events presented as real. Stylised/cartoon/motion-graphics content is generally lower risk, but the flag costs nothing.
- Never present AI-generated footage as real archival footage, real testimony, or a real event. That is the line that gets accounts removed, not throttled.
- Keep the flag **on** even when the platform makes it optional. Optional today, required after the next policy update.

## 2. Music and audio rights

Every track needs a recorded licence before the video posts:

| Source | Safe? | Condition |
|---|---|---|
| Platform native library (TikTok/IG/YT) | yes, in-app only | does not survive reposting off-platform |
| Paid stock (Artlist, Epidemic, etc.) | yes | keep the invoice and the track ID |
| AI-generated music | usually | check the generator's commercial terms per plan tier |
| "Royalty-free" from a random site | **no** | unattributed uploads are the most common claim source |
| Commercial music | **no** | unless you have written sync rights |

Log per video: `track_id, source, licence_ref`. If you cannot fill `licence_ref`, do not use the track.

## 3. Claims

The claims linter (`scripts/claims.py`) is a **floor**, not a legal review. It catches invented numbers. It does not catch:

- implied promises ("this will double your income")
- medical or health outcomes
- financial advice framed as fact
- testimonials that cannot be substantiated
- comparative claims about named competitors

Rules:

- Any number or date on screen must exist in the source-of-truth file. Mechanically enforced.
- No guaranteed outcome, ever. "Can" and "may" over "will" and "does".
- Health and finance: describe the mechanism, not the result. "Tracks spending" not "saves you money".
- No before/after that implies a medical or financial transformation you cannot evidence.

## 4. Likeness, logos and other creators' work

- **No real faces** without written release — including faces scraped from the internet, including "public figures in a non-defamatory context".
- **No logos** you do not have rights to use. Quoting a brand in commentary is one thing; using its logo as decoration is another.
- **No frames, clips or audio from other creators.** Even a two-second clip is a claim waiting to happen. Recreate the idea; do not lift the file.
- Trademarks in comparison content: name the competitor in text if it is factual and fair; do not use their visual identity.

## 5. Pre-post checklist

Copy into every brief's approval:

```
[ ] AI disclosure flag set on every platform
[ ] every track has a licence_ref
[ ] every number on screen is in source-of-truth.md
[ ] no guaranteed medical/financial/earnings outcome
[ ] no real faces, no unlicensed logos, no third-party frames
[ ] claims linter passed (scripts/claims.py exit 0)
```

Six lines. Ninety seconds. It is the difference between a page that compounds and a page that disappears.

## When it goes wrong

Do not delete the video and hope. Platforms escalate on repeated violations faster than on a single bad upload.

1. Take the video down yourself.
2. Identify which of the six checks it failed.
3. Add the missing check to `gate.py` or to this file so the class of error cannot recur.
4. Only then resume posting.
