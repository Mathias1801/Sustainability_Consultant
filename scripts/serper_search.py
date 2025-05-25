import os
import json
import requests
from datetime import datetime
from newspaper import Article

def fetch_sustainability_articles():
    api_key = os.getenv("SERPER_API_KEY")
    if not api_key:
        raise ValueError("Environment variable SERPER_API_KEY is not set.")

    # Define all queries and payloads
    queries_payloads = [
        (
            "shipping OR logistik OR containere OR "
            "bæredygtighed OR 'grøn omstilling' OR klima OR energi OR brændstof "
            "site:shippingwatch.dk OR site:borsen.dk OR site:finans.dk OR site:dr.dk OR "
            "site:ing.dk OR site:energywatch.dk OR site:altinget.dk",
            {
                "q": "shipping OR logistik OR containere OR bæredygtighed OR 'grøn omstilling' OR klima OR energi OR brændstof "
                     "site:shippingwatch.dk OR site:borsen.dk OR site:finans.dk OR site:dr.dk OR "
                     "site:ing.dk OR site:energywatch.dk OR site:altinget.dk",
                "type": "news",
                "gl": "dk",
                "hl": "da",
                "tbs": "qdr:w"
            }
        ),
        (
            "shipping OR logistics OR containerships OR maritime OR sustainability OR "
            "'green transition' OR decarbonization OR net-zero OR climate OR fuels OR energy "
            "site:lloydslist.maritimeintelligence.informa.com OR "
            "site:hellenicshippingnews.com OR site:marinelink.com OR site:gcaptain.com OR "
            "site:splash247.com",
            {
                "q": "shipping OR logistics OR containerships OR maritime OR sustainability OR "
                     "'green transition' OR decarbonization OR net-zero OR climate OR fuels OR energy "
                     "site:lloydslist.maritimeintelligence.informa.com OR "
                     "site:hellenicshippingnews.com OR site:marinelink.com OR site:gcaptain.com OR "
                     "site:splash247.com",
                "type": "news",
                "hl": "en",
                "gl": "us",
                "tbs": "qdr:w"
            }
        ),
        (
            "sustainability OR bæredygtighed OR shipping OR logistik OR logistics OR containerships OR containere OR "
            "climate OR klima OR 'green transition' OR 'grøn omstilling' OR fuels OR brændstof OR maritime OR energi "
            "site:danishshipping.dk OR site:transport.ec.europa.eu OR site:mission-innovation.net OR site:maersk.com/sustainability/",
            {
                "q": "sustainability OR bæredygtighed OR shipping OR logistik OR logistics OR containerships OR containere OR "
                     "climate OR klima OR 'green transition' OR 'grøn omstilling' OR fuels OR brændstof OR maritime OR energi "
                     "site:danishshipping.dk OR site:transport.ec.europa.eu OR site:mission-innovation.net OR site:maersk.com/sustainability/",
                "type": "news",
                "hl": "en",
                "tbs": "qdr:w"
            }
        )
    ]

    seen_links = set()
    combined_results = []

    for query, payload in queries_payloads:
        print(f"🔍 Fetching articles for query:\n{query[:80]}...")
        headers = {
            "X-API-KEY": api_key,
            "Content-Type": "application/json"
        }

        response = requests.post("https://google.serper.dev/news", json=payload, headers=headers)
        if response.status_code != 200:
            print(f"❌ Error {response.status_code}: {response.text}")
            continue

        for item in response.json().get("news", []):
            link = item.get("link")
            if link and link not in seen_links:
                combined_results.append({
                    "title": item.get("title"),
                    "link": link,
                    "date": item.get("date", ""),
                    "snippet": item.get("snippet", "")
                })
                seen_links.add(link)

    # 🔗 Add direct URLs from known sources
    direct_urls = [
        "https://danishshipping.dk/en/about/danish-shipping/annual-report-2024/",
        "https://transport.ec.europa.eu/transport-modes/maritime/decarbonising-maritime-transport-fueleu-maritime_en#:~:text=The%20FuelEU%20maritime%20regulation%20will,2025%3A%20%2D2%25%3B",
        "https://mission-innovation.net/missions/shipping/",
        "https://mission-innovation.net/news_mission/mis-technical-advisory-group-completes-first-annual-review-of-missions/",
        "https://www.maersk.com/sustainability/all-the-way-to-net-zero"
    ]

    for url in direct_urls:
        if url not in seen_links:
            combined_results.append({
                "title": "",       # Will be filled during enrichment
                "link": url,
                "date": "",
                "snippet": ""
            })
            seen_links.add(url)

    # 🧠 Enrich all articles with full content
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
            if article.title:
                enriched["title"] = article.title
        except Exception as e:
            print(f"⚠️ Failed to parse {url}: {e}")

        enriched_articles.append(enriched)

    return {
        "timestamp": datetime.now().isoformat(),
        "query": "Combined strategic Danish, global, and sustainability shipping sources",
        "serper_results": enriched_articles,
    }
