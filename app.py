from flask import Flask, render_template, request, jsonify
from detector import GroqDetector

app = Flask(__name__)

# Initialize Groq detector
print("Initializing Groq LLM detector for sentiment analysis...")
detector = GroqDetector()

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.get_json()
    text = data.get("text", "").strip()
    
    if not text or len(text) < 5:
        return jsonify({"error": "Please enter a longer text for analysis."}), 400

    # Use Groq LLM for sentiment analysis
    llm_result = detector.analyze(text)
    
    result = {
        "text": text,
        "method": "groq_llm",
        "verdict": llm_result.get("verdict", "error"),
        "confidence": llm_result.get("confidence", 0.0),
        "reasoning": llm_result.get("reasoning", "Analysis completed.")
    }

    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
