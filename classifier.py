from transformers import pipeline

class FastClassifier:
    def __init__(self):
        print("Loading sentiment classifier...")
        self.model = pipeline(
            "text-classification",
            model="cardiffnlp/twitter-roberta-base-sentiment-latest",
            truncation=True,
            max_length=512
        )

    def score(self, text: str) -> dict:
        """Returns sentiment labels and scores"""
        if not text.strip():
            return {"label": "neutral", "score": 0.0}
        
        result = self.model(text)[0]
        # model returns 'negative', 'neutral', or 'positive'
        return {
            "label": result["label"],
            "score": result["score"]
        }
