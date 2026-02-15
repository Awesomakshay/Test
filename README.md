# Akshay CA Daily Growth Setup

This setup gives you a **daily reading + action brief** so you improve as a CA and create public-facing content consistently.

## Do you get an executable file?

Yes — you now have **two ways**:

1. **Direct Python script**: `daily_brief.py`
2. **Executable launcher**: `run_daily_brief.sh` (double-click style for terminal use)

You can also make the Python file itself executable.

## Quick start (2 minutes)

```bash
cd /workspace/Test
chmod +x run_daily_brief.sh daily_brief.py
./run_daily_brief.sh
```

This creates a file like:

- `briefs/YYYY-MM-DD.md`

## How to use it daily

After running, open the generated brief and follow this sequence:

1. Read top items in **Tax & Compliance** and **Markets & Investing**.
2. Pick one topic and write a 100-word simple explanation for clients.
3. Record one 60-second reel/short from that same topic.
4. Post one insight on X with "public impact" angle.
5. Note one bias/mistake in your decision journal.

## Manual run

```bash
python3 daily_brief.py
```

## Daily automation (Linux cron)

```bash
crontab -e
```

Add this line (runs at 6:30 AM daily):

```cron
30 6 * * * cd /workspace/Test && /workspace/Test/run_daily_brief.sh >> /workspace/Test/briefs/cron.log 2>&1
```

## If feed links fail sometimes

Some networks/VPN/proxy setups block RSS with `403`. The script is built to:

- continue running,
- generate the daily brief file,
- show warnings so you can retry later.

## What this setup includes

- `daily_brief.py`: fetch + classify + generate daily brief.
- `run_daily_brief.sh`: executable launcher.
- `profile_akshay.yaml`: your profile/preferences reference.
- `briefs/`: output folder for daily briefs.

## Extra ideas to improve faster

- Keep `decision_journal.md` with 3 entries/day: market, creator, personal.
- Sunday weekly review: what worked, what to stop, what to double-down.
- Build a topic bank from comments and reuse for next week’s scripts.
