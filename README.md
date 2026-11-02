# 🛡️ Cyberbullying Detection System

![Python](https://img.shields.io/badge/python-3.9+-blue.svg)
![Flask](https://img.shields.io/badge/flask-2.0+-green.svg)
![Groq](https://img.shields.io/badge/Groq-Llama3.3--70B-orange.svg)
![HuggingFace](https://img.shields.io/badge/HuggingFace-RoBERTa-yellow.svg)
![Reddit](https://img.shields.io/badge/Reddit-PRAW-red.svg)

## 📖 Table of Contents
- [Introduction](#introduction)
- [Problem Statement](#problem-statement)
- [System Architecture](#system-architecture)
    - [High-Level Overview](#high-level-overview)
    - [The Hybrid Detection Pipeline](#the-hybrid-detection-pipeline)
    - [Stage 1: Fast Classification](#stage-1-fast-classification)
    - [Stage 2: Deep Analysis](#stage-2-deep-analysis)
- [Technology Stack](#technology-stack)
- [Features](#features)
- [Installation & Setup](#installation--setup)
    - [Prerequisites](#prerequisites)
    - [Step-by-Step Installation](#step-by-step-installation)
    - [Environment Configuration](#environment-configuration)
- [Usage Guide](#usage-guide)
    - [Web Application](#web-application)
    - [Reddit Monitoring Bot](#reddit-monitoring-bot)
- [Detailed Component Analysis](#detailed-component-analysis)
    - [detector.py](#detectorpy)
    - [classifier.py](#classifierpy)
    - [bot.py](#botpy)
    - [app.py](#apppy)
- [ML Model Breakdown](#ml-model-breakdown)
    - [RoBERTa-base-sentiment-latest](#robertabase-sentiments-latest)
    - [Llama 3.3 70B via Groq](#llama-33-70b-via-groq)
- [Ethical Considerations & Privacy](#ethical-considerations--privacy)
- [Roadmap & Future Enhancements](#roadmap--future-enhancements)
- [Contributing](#contributing)
- [License](#license)

---

## 🌟 Introduction
The **Cyberbullying Detection System** is a sophisticated, hybrid AI-driven tool designed to identify, analyze, and monitor harmful content across digital platforms. In an era where social media interaction is ubiquitous, the prevalence of cyberbullying has grown exponentially, leading to severe psychological impacts on victims. 

This system doesn't just provide a binary "bully/not bully" label; it implements a tiered analysis approach that combines the efficiency of transformer-based sentiment analysis with the deep reasoning capabilities of Large Language Models (LLMs). By integrating both a local fast-classifier and a cloud-based LLM, the system achieves a balance between low-latency processing and high-accuracy contextual understanding.

## 🚩 Problem Statement
Traditional keyword-based filters are insufficient for detecting cyberbullying because they fail to understand:
1. **Sarcasm**: A sentence might use positive words to convey a negative, mocking meaning.
2. **Context**: The same word can be a friendly joke between friends or a targeted attack between strangers.
3. **Evolving Slang**: Bullies constantly change their terminology to bypass static filters.

To solve this, we need a system that understands **sentiment**, **intent**, and **context**. Our system addresses this by utilizing a RoBERTa-based model for initial screening and a Llama-3.3-70B model for nuanced final adjudication.

## 🏗️ System Architecture

### High-Level Overview
The system is designed as a modular pipeline. It can be deployed as a standalone web utility for manual checks or as an autonomous bot that streams data from social media (currently Reddit).

### The Hybrid Detection Pipeline
The core innovation of this project is the **Hybrid Pipeline**. Processing every single piece of social media data through a massive LLM is computationally expensive and slow. Conversely, using only a small model leads to high false-positive rates.

#### Stage 1: Fast Classification (The Filter)
When text enters the system, it is first passed to the `FastClassifier`. This uses a RoBERTa model trained specifically on Twitter data. 
- **Goal**: Quickly identify "Neutral" content.
- **Action**: If the model is highly confident (e.g., > 80%) that the text is neutral, the system can choose to skip the expensive LLM analysis, drastically reducing API costs and latency.

#### Stage 2: Deep Analysis (The Judge)
If the text is flagged as "Negative" or "Positive" (or if the neutral confidence is low), it is escalated to the `GroqDetector`.
- **Goal**: Provide a definitive verdict with reasoning.
- **Action**: The LLM analyzes the text, identifies the emotional tone, and returns a JSON object containing the verdict, a confidence score, and a one-sentence explanation of *why* the text was classified as such.

---

## 🛠️ Technology Stack

### Backend & API
- **Python 3.9+**: The primary language for all logic and integration.
- **Flask**: A lightweight WSGI web application framework used to create the user interface and API endpoints.
- **Groq Cloud**: Utilized for ultra-fast inference of Llama 3.3 70B, providing the "brain" of the system.
- **PRAW (Python Reddit API Wrapper)**: Used to interface with Reddit's API for real-time comment streaming.

### Machine Learning
- **Hugging Face Transformers**: The library providing access to the RoBERTa model.
- **PyTorch**: The underlying tensor library powering the local transformer models.
- **Llama 3.3 70B**: A state-of-the-art LLM used for deep semantic understanding.
- **cardiffnlp/twitter-roberta-base-sentiment-latest**: A specialized model trained on millions of tweets, making it ideal for short-form social media text.

### Data & Utilities
- **Python-dotenv**: For secure management of API keys and sensitive credentials.
- **Pandas/Scikit-Learn**: Used for data handling and evaluation metrics.

---

## ✨ Features
- **Real-time Monitoring**: Stream comments from specific subreddits in real-time.
- **Hybrid Inference**: Automatic escalation from local ML to cloud LLM.
- **Reasoning-based Detection**: Unlike "black box" models, the system provides a human-readable reason for its verdict.
- **Web Interface**: A clean, simple UI for analyzing specific snippets of text.
- **Multi-Subreddit Support**: Ability to track multiple communities simultaneously (e.g., r/teenagers, r/gaming).
- **Confidence Scoring**: Every analysis comes with a confidence percentage to help human moderators prioritize reviews.

---

## 🚀 Installation & Setup

### Prerequisites
Ensure you have the following installed:
- Python 3.9 or higher
- A Groq API Key (Get one at [console.groq.com](https://console.groq.com))
- Reddit API Credentials (Create an app at [reddit.com/prefs/apps](https://www.reddit.com/prefs/apps))

### Step-by-Step Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/yourusername/cyberbullying-detection-system.git
   cd cyberbullying-detection-system
   ```

2. **Create a Virtual Environment**
   ```bash
   python -m venv venv
   # On Windows:
   venv\\Scripts\\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

### Environment Configuration
Create a `.env` file in the root directory and populate it with your credentials:

```env
# Groq API Key
GROQ_API_KEY=your_groq_api_key_here

# Reddit API Credentials
REDDIT_CLIENT_ID=your_client_id
REDDIT_CLIENT_SECRET=your_client_secret
REDDIT_USERNAME=your_reddit_username
REDDIT_PASSWORD=your_reddit_password
```

---

## 📖 Usage Guide

### Web Application
To launch the manual analysis tool:
1. Run the application:
   ```bash
   python app.py
   ```
2. Open your browser and navigate to `http://127.0.0.1:5000`.
3. Enter the text you wish to analyze and click "Analyze". The system will return the verdict, confidence, and reasoning.

### Reddit Monitoring Bot
To start the real-time monitor:
1. Run the bot script:
   ```bash
   python bot.py
   ```
2. The bot will connect to the subreddits defined in `config.py` and begin streaming comments.
3. Results will be printed to the console and logged via `logger.py`.

---

## 🔍 Detailed Component Analysis

### `detector.py`
This module handles the integration with the Groq LLM. It defines a `SYSTEM_PROMPT` that forces the LLM to act as a professional sentiment analyst and output results in a strict JSON format. This ensures the rest of the application can parse the response programmatically.

### `classifier.py`
This module implements the `FastClassifier` class. It loads the RoBERTa model from Hugging Face. By using `truncation=True` and `max_length=512`, it ensures that very long posts don't crash the system, while still capturing the primary sentiment of the text.

### `bot.py`
The bot is the autonomous arm of the system. It uses `subreddit.stream.comments()` to listen for new posts. It implements the two-stage logic:
1. Call `classifier.score()`.
2. If the result is not clearly neutral, call `detector.analyze()`.
3. Log the final result.

### `app.py`
The Flask application provides the REST API. It handles the HTTP POST requests from the frontend, validates that the input text is of sufficient length, and coordinates the call to the `GroqDetector`.

---

## 🧠 ML Model Breakdown

### RoBERTa-base-sentiment-latest
We chose the `cardiffnlp` RoBERTa model because it is specifically fine-tuned on social media data. Unlike general-purpose BERT models, RoBERTa-sentiment understands the nuances of Twitter-style communication, including emojis and common internet shorthand, making it an ideal "first-pass" filter.

### Llama 3.3 70B via Groq
For the final verdict, we use Llama 3.3 70B. This model possesses a vast knowledge base and superior reasoning capabilities. By using the Groq LPU (Language Processing Unit) architecture, we get near-instantaneous responses, making the "deep analysis" stage feel as fast as a local model.

---

## ⚖️ Ethical Considerations & Privacy
Building a tool to monitor social media comes with significant ethical responsibilities:

1. **Privacy**: This system is designed for research and moderation. It should not be used to dox individuals or infringe upon the privacy of users.
2. **Bias in AI**: All ML models carry inherent biases from their training data. A "negative" sentiment doesn't always equal "bullying." Human oversight is always recommended for final disciplinary actions.
3. **False Positives**: The system provides a confidence score precisely because AI can be wrong. High-confidence negatives should be prioritized, while low-confidence ones should be reviewed by humans.

---

## 🗺️ Roadmap & Future Enhancements
- [ ] **Expanded Platform Support**: Integrate with Discord, X (Twitter), and Instagram APIs.
- [ ] **Multi-Language Support**: Implement multilingual transformers to detect bullying in Spanish, French, and Hindi.
- [ ] **Dashboard Integration**: Create a React-based dashboard to visualize bullying trends across different subreddits.
- [ ] **Automatic Reporting**: Add a feature to automatically flag highly confident bullying cases to platform moderators.
- [ ] **Fine-tuned Local Model**: Train a custom model on a labeled cyberbullying dataset (e.g., Kaggle Cyberbullying Dataset) to replace the general sentiment model.

---

## 🤝 Contributing
Contributions are welcome! If you'd like to improve the system:
1. Fork the repository.
2. Create a feature branch (`git checkout -b feature/AmazingFeature`).
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`).
4. Push to the branch (`git push origin feature/AmazingFeature`).
5. Open a Pull Request.

---

## 📜 License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
