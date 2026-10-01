import json
import os
from datetime import datetime

LOG_FILE = "sentiment_logs.json"

def log_sentiment(item, result: dict, method: str):
    # Handle both Reddit items (praw) and simple strings/dicts
    is_reddit = hasattr(item, 'permalink')
    
    entry = {
        "timestamp": datetime.now().isoformat(),
        "text": (item.body[:500] if hasattr(item, 'body') else item.title) if is_reddit else str(item),
        "verdict": result.get("verdict"),
        "confidence": result.get("confidence"),
        "reasoning": result.get("reasoning"),
        "detected_by": method
    }
    
    if is_reddit:
        entry["url"] = f"https://reddit.com{item.permalink}"
        entry["subreddit"] = str(item.subreddit)
        entry["author"] = str(item.author)

    # Load existing logs
    logs = []
    if os.path.exists(LOG_FILE):
        try:
            with open(LOG_FILE, "r") as f:
                logs = json.load(f)
        except json.JSONDecodeError:
            logs = []

    logs.append(entry)

    with open(LOG_FILE, "w") as f:
        json.dump(logs, f, indent=2)

    print(f"\n📊 SENTIMENT [{method}]")
    print(f"   Verdict    : {entry['verdict']} ({entry.get('confidence', 0)})")
    print(f"   Reasoning  : {entry['reasoning']}")
