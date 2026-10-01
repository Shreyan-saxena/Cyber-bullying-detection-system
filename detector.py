from groq import Groq
from config import GROQ_API_KEY
import json

SYSTEM_PROMPT = """
You are an expert sentiment analysis system.
Analyze the sentiment of the provided text and classify it as positive, negative, or neutral.

Respond ONLY in this exact JSON, no extra text:
{
  "verdict": "positive" | "negative" | "neutral",
  "confidence": 0.0-1.0,
  "reasoning": "one sentence max description of the sentiment"
}
"""

class GroqDetector:
    def __init__(self):
        self.client = Groq(api_key=GROQ_API_KEY)

    def analyze(self, text: str) -> dict:
        try:
            response = self.client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                temperature=0.1,
                max_tokens=300,
                response_format={"type": "json_object"},
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": f"Text to analyze:\n\"{text}\""}
                ]
            )
            return json.loads(response.choices[0].message.content)

        except Exception as e:
            print(f"Groq error: {e}")
            return {"verdict": "error", "confidence": 0.0, "reasoning": str(e)}
