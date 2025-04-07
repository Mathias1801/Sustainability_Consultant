# app.py
import os
import json
from datetime import datetime
from dotenv import load_dotenv
from crewai import Crew

from agents import CustomAgents
from tasks import CustomTasks
from serper_search import fetch_sustainability_articles

load_dotenv()

def main():
    # === 1. Run Serper Search and Save JSON ===
    serper_results = fetch_sustainability_articles()
    json_filename = f"sustainability_sources_{datetime.now().strftime('%Y-%m-%d')}.json"
    with open(json_filename, "w", encoding="utf-8") as f:
        json.dump(serper_results, f, indent=2)
    print(f"\n✅ Serper results saved to: {json_filename}")

    # === 2. Convert Search Results to Text Block ===
    news_items = serper_results["serper_results"]
    eea_items = serper_results["eea_context_sources"]

    serper_data_text = "\n\n".join(
        f"Title: {item['title']}\nDate: {item['date']}\nLink: {item['link']}\nSnippet: {item['snippet']}"
        for item in news_items
    )
    serper_data_text += "\n\nEEA Sources:\n" + "\n".join(f"{item['title']} - {item['url']}" for item in eea_items)

    # === 3. Initialize Agents and Tasks ===
    agents = CustomAgents()
    tasks = CustomTasks()

    summarize_agent = agents.summarize_agent()
    summarize_task = tasks.summarize_task(summarize_agent, serper_data_text)

    crew = Crew(
        agents=[summarize_agent],
        tasks=[summarize_task],
        verbose=True
    )

    print("\n🚀 Running the Crew...\n")
    final_output = crew.kickoff()

    # === 4. Save Final Output ===
    txt_filename = f"sustainability_summary_{datetime.now().strftime('%Y-%m-%d')}.txt"
    with open(txt_filename, "w", encoding="utf-8") as f:
        f.write(str(final_output))

    print(f"\n📄 Final summary saved to: {txt_filename}")

if __name__ == "__main__":
    main()
