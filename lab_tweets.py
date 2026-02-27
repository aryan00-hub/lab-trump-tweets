#!/usr/bin/env python3

'''
# Lab: Analyzing Trump Tweets
(keep your lab instructions here if you want)
'''

import json
import glob
import matplotlib.pyplot as plt


# -----------------------------
# 1) Load all tweets (CONDENSED files)
# -----------------------------
tweets = []
files = sorted(glob.glob("condensed_*.json"))

if len(files) == 0:
    raise SystemExit(
        "No condensed_*.json files found. Make sure condensed_2009.json ... condensed_2018.json "
        "are in this folder (and you unzipped condensed_*.json.zip)."
    )

for fn in files:
    with open(fn, "r", encoding="utf-8") as f:
        tweets.extend(json.load(f))

print("len(tweets)=", len(tweets))


# -----------------------------
# 2) Choose phrases (required + 3 extra)
# -----------------------------
phrases = [
    "obama",
    "trump",
    "mexico",
    "russia",
    "fake news",
    "china",            # extra
    "wall",             # extra
    "mainstream media"  # extra
]


# -----------------------------
# 3) Count tweets containing each phrase (case-insensitive)
#    Each tweet counts at most once per phrase
# -----------------------------
counts = {p: 0 for p in phrases}

for t in tweets:
    text = t.get("text", "")
    text_lower = text.lower()
    for p in phrases:
        if p in text_lower:
            counts[p] += 1

print("counts=", counts)


# -----------------------------
# 4) Compute percent of tweets containing each phrase
# -----------------------------
total = len(tweets)
percents = {p: (100.0 * counts[p] / total) for p in phrases}


# -----------------------------
# 5) Print markdown table (matches lab format)
# -----------------------------
col_width = max(len(p) for p in phrases)

print(f"| {'phrase':<{col_width}} | percent of tweets |")
print(f"| {'-'*col_width} | ----------------- |")

for p in sorted(phrases):
    pct_str = f"{percents[p]:05.2f}"  # e.g. 00.17
    print(f"| {p:>{col_width}} | {pct_str:<15} |")


# -----------------------------
# 6) Bar chart + save image
# -----------------------------
labels = sorted(phrases)
values = [percents[p] for p in labels]

plt.figure(figsize=(10, 5))
plt.bar(labels, values)
plt.xticks(rotation=45, ha="right")
plt.ylabel("Percent of tweets")
plt.title("Percent of Trump's tweets containing each phrase")
plt.tight_layout()
plt.savefig("tweet_counts.png")
plt.close()

print("Saved plot as tweet_counts.png")

# -----------------------------
# EXTRA CREDIT
# Plot tweets by hour of day
# -----------------------------
from collections import Counter
from datetime import datetime

hour_counts = Counter()

for t in tweets:
    created = t.get("created_at")
    if not created:
        continue
    
    # Example format: 'Wed Oct 10 20:19:24 +0000 2018'
    dt = datetime.strptime(created, "%a %b %d %H:%M:%S %z %Y")
    hour_counts[dt.hour] += 1

# Prepare data for plot
hours = list(range(24))
counts_by_hour = [hour_counts[h] for h in hours]

plt.figure(figsize=(10,5))
plt.bar(hours, counts_by_hour)
plt.xlabel("Hour of Day (24-hour format)")
plt.ylabel("Number of Tweets")
plt.title("Number of Trump's Tweets by Hour of Day")
plt.tight_layout()
plt.savefig("tweets_by_hour.png")
plt.close()

print("Saved plot as tweets_by_hour.png")