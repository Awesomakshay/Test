#!/usr/bin/env python3
"""Generate a daily CA learning + public-connection brief from RSS feeds."""

from __future__ import annotations

import argparse
import datetime as dt
import html
import pathlib
import re
import textwrap
import urllib.request
import xml.etree.ElementTree as ET

PROFILE_PATH = pathlib.Path("profile_akshay.yaml")
OUTPUT_DIR = pathlib.Path("briefs")

FEEDS = {
    "Income Tax India Updates": "https://incometaxindia.gov.in/Lists/Press%20Releases/AllItems.rss",
    "SEBI Press Releases": "https://www.sebi.gov.in/sebirss.xml",
    "RBI Press Releases": "https://website.rbi.org.in/web/rbi/rss/pressreleases.xml",
    "LiveMint Markets": "https://www.livemint.com/rss/markets",
    "Economic Times Markets": "https://economictimes.indiatimes.com/markets/rssfeeds/1977021501.cms",
    "Psychology Today": "https://www.psychologytoday.com/intl/rss",
}

TRACKS = {
    "Tax & Compliance": ["tax", "gst", "compliance", "assessment", "income tax", "itr", "audit"],
    "Markets & Investing": ["market", "stocks", "nifty", "sensex", "ipo", "equity", "volatility"],
    "Behavioral Finance": ["bias", "behavior", "psychology", "emotion", "decision", "discipline"],
    "Public Connect": ["household", "middle class", "small business", "salary", "consumer", "retail"],
}

MAX_ITEMS_PER_TRACK = 3


def fetch(url: str) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=20) as resp:
        return resp.read().decode("utf-8", errors="ignore")


def parse_rss(xml_text: str) -> list[dict[str, str]]:
    root = ET.fromstring(xml_text)
    items = []
    for item in root.findall(".//item"):
        title = (item.findtext("title") or "").strip()
        link = (item.findtext("link") or "").strip()
        desc = html.unescape((item.findtext("description") or "").strip())
        pub = (item.findtext("pubDate") or item.findtext("date") or "").strip()
        if title and link:
            items.append({"title": title, "link": link, "description": strip_tags(desc), "pubDate": pub})
    return items


def strip_tags(text: str) -> str:
    no_tags = re.sub(r"<[^>]+>", " ", text)
    return re.sub(r"\s+", " ", no_tags).strip()


def score_item(item: dict[str, str], keywords: list[str]) -> int:
    hay = f"{item['title']} {item['description']}".lower()
    return sum(2 if kw in item["title"].lower() else 1 for kw in keywords if kw in hay)


def classify(all_items: list[dict[str, str]]) -> dict[str, list[dict[str, str]]]:
    output: dict[str, list[dict[str, str]]] = {track: [] for track in TRACKS}
    for track, keywords in TRACKS.items():
        scored = []
        for item in all_items:
            sc = score_item(item, keywords)
            if sc:
                scored.append((sc, item))
        scored.sort(key=lambda x: x[0], reverse=True)

        dedup = []
        seen_links = set()
        for _, item in scored:
            if item["link"] in seen_links:
                continue
            seen_links.add(item["link"])
            dedup.append(item)
            if len(dedup) >= MAX_ITEMS_PER_TRACK:
                break
        output[track] = dedup
    return output


def make_daily_actions(selections: dict[str, list[dict[str, str]]]) -> str:
    actions = [
        "1. Read Tax & Compliance section first (20 min).",
        "2. Pick ONE item and write a 100-word plain-language explanation for clients.",
        "3. Record one 60-second video hook from Markets/Behavioral section.",
        "4. Post on X: one chart/insight + one human impact takeaway.",
        "5. End of day: journal one decision bias you noticed in yourself or market participants.",
    ]

    if not any(selections.values()):
        actions.insert(0, "No feed items retrieved. Re-run script or check network.")

    return "\n".join(f"- {a}" for a in actions)


def summary_line(item: dict[str, str]) -> str:
    snippet = textwrap.shorten(item["description"], width=140, placeholder="...")
    date_bits = f" ({item['pubDate']})" if item["pubDate"] else ""
    return f"- [{item['title']}]({item['link']}){date_bits}\n  - Why it matters: {snippet}"


def generate_markdown(grouped: dict[str, list[dict[str, str]]]) -> str:
    today = dt.date.today().isoformat()
    sections = [
        f"# Akshay Daily CA Growth Brief — {today}",
        "",
        "## How to use this in 45 minutes",
        make_daily_actions(grouped),
        "",
    ]

    for track, items in grouped.items():
        sections.append(f"## {track}")
        if items:
            sections.extend(summary_line(item) for item in items)
        else:
            sections.append("- No strong matches today from configured feeds.")
        sections.append("")

    sections.extend(
        [
            "## Public Connection Prompt",
            "- Explain one finance/tax topic today using this frame: 'Problem → Why people feel stuck → Simple action step'.",
            "- Ask one audience question at the end to trigger comments.",
            "",
            "## Content Repurposing",
            "- Long post (X/LinkedIn): 5-7 bullets with one practical checklist.",
            "- Reel/Short: one myth-busting hook + one caution + one CTA.",
            "- YouTube: 6-minute explainer from the same topic.",
        ]
    )

    return "\n".join(sections)


def count_items(grouped: dict[str, list[dict[str, str]]]) -> int:
    return sum(len(v) for v in grouped.values())


def preview(out_path: pathlib.Path, lines: int = 20) -> None:
    print("\nPreview:")
    for idx, line in enumerate(out_path.read_text(encoding="utf-8").splitlines(), start=1):
        if idx > lines:
            print("... (truncated)")
            break
        print(line)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Generate a daily CA growth brief.")
    parser.add_argument("--preview", action="store_true", help="Print first lines of generated brief.")
    return parser


def main() -> None:
    args = build_parser().parse_args()

    all_items = []
    failures = 0
    for source, url in FEEDS.items():
        try:
            xml_text = fetch(url)
            entries = parse_rss(xml_text)
            for e in entries:
                e["source"] = source
            all_items.extend(entries)
            print(f"OK   {source}: fetched {len(entries)} items")
        except Exception as exc:  # broad to keep pipeline resilient
            failures += 1
            print(f"WARN {source}: {exc}")

    grouped = classify(all_items)
    md = generate_markdown(grouped)

    OUTPUT_DIR.mkdir(exist_ok=True)
    out_path = OUTPUT_DIR / f"{dt.date.today().isoformat()}.md"
    out_path.write_text(md, encoding="utf-8")

    print("\n=== Run summary ===")
    print(f"Feeds configured : {len(FEEDS)}")
    print(f"Feeds failed     : {failures}")
    print(f"Articles selected: {count_items(grouped)}")
    print(f"Brief file       : {out_path}")
    if PROFILE_PATH.exists():
        print(f"Profile          : {PROFILE_PATH}")

    if args.preview:
        preview(out_path)


if __name__ == "__main__":
    main()
