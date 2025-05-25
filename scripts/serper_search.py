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

    # Fetch and deduplicate articles
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

    # Enrich with full article text
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

    # Final output structure
    return {
        "timestamp": datetime.now().isoformat(),
        "query_summary": "Combined strategic, global, and sustainability shipping sources",
        "query_details": [payload["q"] for _, payload in queries_payloads],
        "serper_results": enriched_articles,
    }
