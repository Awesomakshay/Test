# Akshay CA Daily Growth Setup

This setup gives you a **daily reading + action brief** so you improve as a CA and create public-facing content consistently.

## Why it looked like it "closed"

When the script finishes, terminal windows (especially double-click runs) can close immediately.
Now the launcher:

- prints a clear run summary,
- shows a short preview of the generated brief,
- writes a persistent log to `briefs/last_run.log`,
- waits for Enter before closing (interactive runs).

## Quick start (2 minutes)

```bash
cd /workspace/Test
chmod +x run_daily_brief.sh daily_brief.py
./run_daily_brief.sh
```

## What you will see now

- `OK ... fetched N items` for successful sources
- `WARN ...` for blocked sources (e.g., 403)
- `=== Run summary ===` with counts
- a preview of the generated brief
- output file location

Generated file:

- `briefs/YYYY-MM-DD.md`

## If websites fail sometimes

Some networks/VPN/proxy setups block RSS with `403`. The script is built to:

- continue running,
- generate the daily brief file,
- show warnings and log details.

Check the last run anytime:

```bash
cat briefs/last_run.log
```

## Daily automation (cron)

For automation (no pause because cron is non-interactive):

```cron
30 6 * * * cd /workspace/Test && /workspace/Test/run_daily_brief.sh >> /workspace/Test/briefs/cron.log 2>&1
```

## Manual alternatives

```bash
python3 daily_brief.py
python3 daily_brief.py --preview
```
