import os
import json
import requests
from datetime import datetime
from newspaper import Article

# -------------------- STATIC EEA LINKS --------------------

EEA_SOURCES = [
    {
        "title": "EEA – Denmark Country Overview",
        "url": "https://www.eea.europa.eu/en/countries/eea-member-countries/denmark"
    },
    {
        "title": "EEA – Denmark Country Profile on SDGs",
        "url": "https://www.eea.europa.eu/themes/sustainability-transitions/sustainable-development-goals-and-the/country-profiles/denmark-country-profile-sdgs-and"
    },
    {
        "title": "EEA – Editorials",
        "url": "https://www.eea.europa.eu/en/newsroom/editorial"
    },
    {
        "title": "EEA – Newsroom",
        "url": "https://www.eea.europa.eu/en/newsroom/news"
    }
]

# -------------------- MAIN FETCH FUNCTION --------------------

def fetch_sustainability_articles():
    api_key = os.getenv("SERPER_API_KEY")
    if not api_key:
        raise ValueError("Environment variable SERPER_API_KEY is not set.")

    query = (
        "bæredygtighed OR 'grøn omstilling' OR klima OR biodiversitet "
        "site:.dk OR site:dr.dk OR site:altinget.dk "
        "(politik OR mål OR SDG OR miljø)"
    )

    payload = {
        "q": query,
        "type": "news",
        "gl": "dk",
        "hl": "da",
        "tbs": "qdr:w"
    }

    headers = {
        "X-API-KEY": api_key,
        "Content-Type": "application/json"
    }

    print("🔍 Fetching sustainability news from Serper.dev...")
    response = requests.post("https://google.serper.dev/news", json=payload, headers=headers)

    if response.status_code != 200:
        raise Exception(f"Serper API error {response.status_code}: {response.text}")

    results = response.json().get("news", [])

    combined_results = [
        {"title": item["title"], "link": item["link"], "date": item.get("date", ""), "snippet": item.get("snippet", "")}
        for item in results
    ]

    # Add EEA sources (no snippet, no date)
    for item in EEA_SOURCES:
        combined_results.append({
            "title": item["title"],
            "link": item["url"],
            "date": "",
            "snippet": ""
        })

    # Enrich all articles with full text
    enriched_articles = []
    for item in combined_results:
        url = item["link"]
        print(f"📰 Processing: {url}")

        enriched = {
            "title": item.get("title"),
            "link": url,
            "date": item.get("date", ""),
            "snippet": item.get("snippet", ""),
            "text": "",
            "authors": []
        }

        try:
            article = Article(url)
            article.download()
            article.parse()
            enriched["text"] = article.text
            enriched["authors"] = article.authors
            # If newspaper detects a better title, update it
            if article.title:
                enriched["title"] = article.title
        except Exception as e:
            print(f"⚠️ Failed to parse {url}: {e}")

        enriched_articles.append(enriched)

    # Return structure compatible with `app.py`
    structured_output = {
        "timestamp": datetime.now().isoformat(),
        "query": query,
        "serper_results": enriched_articles,
        "eea_context_sources": EEA_SOURCES
    }

    return structured_output
