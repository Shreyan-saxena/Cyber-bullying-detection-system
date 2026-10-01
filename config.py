import os
from dotenv import load_dotenv
load_dotenv()

REDDIT_CLIENT_ID     = os.getenv("REDDIT_CLIENT_ID")
REDDIT_CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET")
REDDIT_USERNAME      = os.getenv("REDDIT_USERNAME")
REDDIT_PASSWORD      = os.getenv("REDDIT_PASSWORD")
GROQ_API_KEY         = os.getenv("GROQ_API_KEY")

SUBREDDITS           = ["teenagers", "AskReddit", "gaming"]
CONFIDENCE_THRESHOLD = 0.75
