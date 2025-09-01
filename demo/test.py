import os
import google.generativeai as genai
import requests
import textwrap

# 🔑 API Keys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

NEWS_API_KEY = os.getenv("NEWS_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

NEWS_URL = "https://newsapi.org/v2/everything"

# Configure Gemini
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

def fetch_news(query="technology"):
    """Fetch recent technology news articles"""
    params = {
        "q": query,
        "apiKey": NEWS_API_KEY,
        "language": "en",
        "pageSize": 5,
        "sortBy": "publishedAt"
    }
    response = requests.get(NEWS_URL, params=params)
    data = response.json()
    if "articles" not in data:
        return []

    return [f"{a['title']}. {a['description'] or ''}" for a in data["articles"]]

def summarize_articles(articles):
    """Summarize each article with Gemini"""
    if not articles:
        return ["No relevant updates found."]

    summaries = []
    for i, article in enumerate(articles, start=1):
        text = article[:2000]  # limit input size
        prompt = f"Summarize this news article in 3-4 concise sentences:\n\n{text}"
        response = model.generate_content(prompt)
        summary = response.text.strip()
        formatted = textwrap.fill(f"📰 Article {i}: {summary}", width=80)
        summaries.append(formatted)
    return summaries

def techbot():
    print("🤖 TechBot (Gemini-powered): Ask me about the latest in technology (type 'exit' to quit).")
    while True:
        query = input("\nYou: ")
        if query.lower() in ["exit", "quit"]:
            print("TechBot: Goodbye! 👋")
            break
        articles = fetch_news(query)
        replies = summarize_articles(articles)
        print("\nTechBot:\n")
        for para in replies:
            print(para + "\n")

if __name__ == "__main__":
    techbot()
