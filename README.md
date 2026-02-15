# Akshay CA Daily Growth Setup

This setup generates a daily reading brief from internet sources relevant to a practicing CA in India.

## What it does

- Fetches fresh RSS articles from tax, regulation, markets, and psychology sources.
- Sorts content into 4 tracks:
  - Tax & Compliance
  - Markets & Investing
  - Behavioral Finance
  - Public Connect
- Generates a daily markdown brief at `briefs/YYYY-MM-DD.md`.
- Adds execution prompts so reading turns into content + better decision habits.

## Run manually

```bash
python3 daily_brief.py
```

## Set daily automation (Linux cron)

```bash
crontab -e
```

Add this line (runs at 6:30 AM daily):

```cron
30 6 * * * cd /workspace/Test && /usr/bin/python3 daily_brief.py >> /workspace/Test/briefs/cron.log 2>&1
```

## Recommended daily loop (45–60 min)

1. Read top 3 Tax/Markets articles.
2. Convert one article to a plain-language client explainer.
3. Record one short video hook.
4. Post one insight on X with a public-impact angle.
5. Journal one decision error (bias) you noticed that day.

## Extra ideas to improve faster

- Keep a `decision_journal.md` with 3 entries/day: market, creator, personal.
- Use a weekly review every Sunday: what performed, what to drop, what to double-down.
- Build a "topic bank" from recurring audience comments and turn that into next week's scripts.
