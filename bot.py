import praw
from config import *
from classifier import FastClassifier
from detector import GroqDetector
from logger import log_sentiment

# Init Reddit
reddit = praw.Reddit(
    client_id=REDDIT_CLIENT_ID,
    client_secret=REDDIT_CLIENT_SECRET,
    user_agent="SentimentBot/1.0",
    username=REDDIT_USERNAME,
    password=REDDIT_PASSWORD
)

classifier = FastClassifier()
detector   = GroqDetector()

def process(item):
    text = item.body if hasattr(item, 'body') else item.title
    if not text or len(text) < 10:
        return

    # Stage 1: fast classifier for initial sentiment
    sentiment_data = classifier.score(text)
    
    # If it's neutral with high confidence, maybe we skip or log as is
    if sentiment_data["label"] == "neutral" and sentiment_data["score"] > 0.8:
        return

    # Stage 2: Groq LLM for detailed sentiment analysis
    result = detector.analyze(text)

    # Log the sentiment result
    log_sentiment(item, result, method="groq_llm")
    print(f"Sentiment: {result.get('verdict')} | Text: {text[:50]}...")

def run():
    subreddit = reddit.subreddit("+".join(SUBREDDITS))
    print(f"🤖 Sentiment Bot running on: r/{'+'.join(SUBREDDITS)}")
    print(f"   Stage 1: RoBERTa Sentiment classifier")
    print(f"   Stage 2: Groq Llama 3.3 70B\n")

    for comment in subreddit.stream.comments(skip_existing=True):
        try:
            process(comment)
        except Exception as e:
            print(f"Error: {e}")
            continue

if __name__ == "__main__":
    run()
