#!/usr/bin/env python3

'''
Lab: Analyzing Trump Tweets
This script loads condensed tweet JSON files, counts phrase frequency by tweet,
prints a markdown table, saves plots, and updates README.md.
'''

import json
import glob
import matplotlib.pyplot as plt
from collections import Counter
from datetime import datetime


# -----------------------------
# SETTINGS
# -----------------------------
FILE_GLOB = "condensed_*.json"          # change to "master_*.json" if needed
PHRASES = [
    "obama",
    "trump",
    "mexico",
    "russia",
    "fake news",
    "china",            # extra
    "wall",             # extra
    "mainstream media"  # extra
]

MAIN_PLOT = "tweet_counts.png"
HOUR_PLOT = "tweets_by_hour.png"
TABLE_FILE = "table.md"


# -----------------------------
# 1) Load tweets
# -----------------------------
files = sorted(glob.glob(FILE_GLOB))
if not files:
    raise SystemExit(
        f"No files matched {FILE_GLOB}. Make sure you unzipped the condensed/master json files into this folder."
    )

tweets = []
for fn in files:
    with open(fn, "r", encoding="utf-8") as f:
        tweets.extend(json.load(f))

print("len(tweets)=", len(tweets))


# -----------------------------
# 2) Count phrases (case-insensitive; once per tweet per phrase)
# -----------------------------
phrases = [p.lower() for p in PHRASES]
counts = {p: 0 for p in phrases}

for t in tweets:
    text = t.get("text", "")
    text_lower = text.lower()
    for p in phrases:
        if p in text_lower:
            counts[p] += 1

print("counts=", counts)


# -----------------------------
# 3) Compute percents
# -----------------------------
total = len(tweets)
percents = {p: (100.0 * counts[p] / total) for p in phrases}


# -----------------------------
# 4) Build markdown table text (and print it)
# -----------------------------
col_width = max(len(p) for p in phrases)

table_lines = []
table_lines.append(f"| {'phrase':<{col_width}} | percent of tweets |")
table_lines.append(f"| {'-'*col_width} | ----------------- |")
for p in sorted(phrases):
    pct_str = f"{percents[p]:05.2f}"  # e.g. 00.17
    table_lines.append(f"| {p:>{col_width}} | {pct_str:<15} |")

table_text = "\n".join(table_lines) + "\n"
print("\n" + table_text)

with open(TABLE_FILE, "w", encoding="utf-8") as f:
    f.write(table_text)
print(f"Saved table as {TABLE_FILE}")


# -----------------------------
# 5) Main bar chart (phrases)
# -----------------------------
labels = sorted(phrases)
values = [percents[p] for p in labels]

plt.figure(figsize=(10, 5))
plt.bar(labels, values)
plt.xticks(rotation=45, ha="right")
plt.ylabel("Percent of tweets")
plt.title("Percent of Trump's tweets containing each phrase")
plt.tight_layout()
plt.savefig(MAIN_PLOT)
plt.close()

print(f"Saved plot as {MAIN_PLOT}")


# -----------------------------
# 6) Extra credit: tweets by hour of day (uses created_at, not text)
# -----------------------------
hour_counts = Counter()

for t in tweets:
    created = t.get("created_at")
    if not created:
        continue
    # Example format: 'Wed Oct 10 20:19:24 +0000 2018'
    dt = datetime.strptime(created, "%a %b %d %H:%M:%S %z %Y")
    hour_counts[dt.hour] += 1

hours = list(range(24))
counts_by_hour = [hour_counts[h] for h in hours]

plt.figure(figsize=(10, 5))
plt.bar(hours, counts_by_hour)
plt.xlabel("Hour of Day (24-hour format)")
plt.ylabel("Number of Tweets")
plt.title("Number of Trump's Tweets by Hour of Day")
plt.tight_layout()
plt.savefig(HOUR_PLOT)
plt.close()

print(f"Saved plot as {HOUR_PLOT}")


# -----------------------------
# 7) Auto-write README.md with table + images
# -----------------------------
readme = (
    "# Trump Tweet Phrase Analysis (2009–2018)\n\n"
    f"This table shows the percent of tweets containing each phrase (n = {len(tweets)} tweets).\n\n"
    + table_text +
    "\n"
    f"![Tweet phrase percentages]({MAIN_PLOT})\n\n"
    "## Extra Credit: Tweets by Hour of Day\n\n"
    f"![Tweets by hour]({HOUR_PLOT})\n"
)

with open("README.md", "w", encoding="utf-8") as f:
    f.write(readme)

print("Updated README.md with table + images")