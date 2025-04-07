# serper_search.py

import requests
import os
import json
from datetime import datetime

def fetch_sustainability_articles():
    # === CONFIG ===
    API_KEY = os.getenv("SERPER_API_KEY")
    if not API_KEY:
        raise ValueError("Please set the SERPER_API_KEY environment variable.")

    # === QUERY ===
    query = (
        "sustainability OR 'green transition' OR climate OR biodiversity "
        "site:.dk OR site:euractiv.com OR site:theguardian.com "
        "Denmark (policy OR goals OR SDGs OR environment)"
    )

    payload = {
        "q": query,
        "type": "news",
        "gl": "dk",
        "hl": "en",
        "tbs": "qdr:w"
    }

    headers = {
        "X-API-KEY": API_KEY,
        "Content-Type": "application/json"
    }

    print("🔍 Fetching sustainability news from Serper.dev...")
    response = requests.post("https://google.serper.dev/news", json=payload, headers=headers)

    if response.status_code != 200:
        raise Exception(f"Serper API error {response.status_code}: {response.text}")

    results = response.json().get("news", [])

    # === ADDITIONAL SOURCES ===
    eea_sources = [
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

    # === STRUCTURE DATA ===
    structured_output = {
        "timestamp": datetime.now().isoformat(),
        "query": query,
        "serper_results": [
            {
                "title": item["title"],
                "link": item["link"],
                "snippet": item.get("snippet", ""),
                "date": item.get("date", "")
            } for item in results
        ],
        "eea_context_sources": eea_sources
    }

    return structured_output
