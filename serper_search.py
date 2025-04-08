# fetch_articles.py

import os
import json
import requests
from datetime import datetime
from newspaper import Article

# -------------------- STATIC EEA LINKS --------------------

EEA_SOURCES = [
    {
        "title": "EEA – Denmark Country Overview",
        "link": "https://www.eea.europa.eu/en/countries/eea-member-countries/denmark"
    },
    {
        "title": "EEA – Denmark Country Profile on SDGs",
        "link": "https://www.eea.europa.eu/themes/sustainability-transitions/sustainable-development-goals-and-the/country-profiles/denmark-country-profile-sdgs-and"
    }
]

# -------------------- FETCH FROM SERPER --------------------

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

    serper_results = response.json().get("news", [])

    # Combine with static EEA links
    all_results = [
        {"title": item["title"], "link": item["link"]}
        for item in serper_results + EEA_SOURCES
    ]

    return all_results

# -------------------- EXTRACT FULL ARTICLES --------------------

def enrich_articles_with_full_text(article_list):
    enriched = []

    for item in article_list:
        url = item.get("link")
        print(f"📰 Processing: {url}")

        enriched_data = {
            "title": item.get("title"),
            "url": url,
            "authors": [],
            "text": ""
        }

        try:
            article = Article(url)
            article.download()
            article.parse()

            enriched_data.update({
                "title": article.title or enriched_data["title"],
                "authors": article.authors,
                "text": article.text
            })
        except Exception as e:
            print(f"⚠️ Error processing {url}: {e}")

        enriched.append(enriched_data)

    return enriched

# -------------------- MAIN --------------------

def main():
    articles = fetch_sustainability_articles()
    enriched = enrich_articles_with_full_text(articles)

    # Ensure output directory exists
    output_dir = os.path.join("data", "weekly_log")
    os.makedirs(output_dir, exist_ok=True)

    # Save file in the folder
    output_filename = f"enriched_articles_{datetime.now().date()}.json"
    output_path = os.path.join(output_dir, output_filename)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(enriched, f, ensure_ascii=False, indent=4)

    print(f"✅ Saved {len(enriched)} enriched articles to {output_path}")


if __name__ == "__main__":
    main()
