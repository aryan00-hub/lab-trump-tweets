import json
import glob
import matplotlib.pyplot as plt

# -----------------------------
# 1) Load all tweets (ONCE)
# -----------------------------
tweets = []

for filename in sorted(glob.glob("master_*.json")):
    with open(filename, "r", encoding="utf-8") as f:
        data = json.load(f)          # each file is a list of tweet dicts
        tweets.extend(data)

print("len(tweets)=", len(tweets))

# -----------------------------
# 2) Choose phrases to count
#    (required + 3 extra)
# -----------------------------
phrases = [
    "obama",
    "trump",
    "mexico",
    "russia",
    "fake news",
    "china",          # extra
    "wall",           # extra
    "mainstream media"  # extra
]

# -----------------------------
# 3) Count tweets containing each phrase (case-insensitive)
#    Each tweet counts at most once per phrase
# -----------------------------
counts = {phrase: 0 for phrase in phrases}

for tweet in tweets:
    text = tweet.get("text", "")
    text_lower = text.lower()

    for phrase in phrases:
        if phrase in text_lower:
            counts[phrase] += 1

print("counts=", counts)

# -----------------------------
# 4) Compute percents
# -----------------------------
total = len(tweets)
percents = {phrase: (100.0 * counts[phrase] / total) for phrase in phrases}

# -----------------------------
# 5) Print markdown table (match lab format)
col_width = max(len(p) for p in phrases)

print(f"| {'phrase':<{col_width}} | percent of tweets |")
print(f"| {'-'*col_width} | ----------------- |")

for phrase in sorted(phrases):
    pct_str = f"{percents[phrase]:05.2f}"  # like 00.17
    print(f"| {phrase:>{col_width}} | {pct_str:<15} |")

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