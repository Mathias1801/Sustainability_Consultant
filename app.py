import os
import json
import sqlite3
from datetime import datetime
from dotenv import load_dotenv
from crewai import Crew

from agents import CustomAgents
from tasks import CustomTasks
from serper_search import fetch_sustainability_articles

load_dotenv()

def main():
    # === 1. Run Serper Search and Save Raw JSON ===
    os.makedirs("summaries", exist_ok=True)
    serper_results = fetch_sustainability_articles()
    summary_date = datetime.now().strftime('%Y-%m-%d')
    json_filename = f"summaries/sustainability_sources_{summary_date}.json"

    with open(json_filename, "w", encoding="utf-8") as f:
        json.dump(serper_results, f, indent=2)
    print(f"\n✅ Serper results saved to: {json_filename}")

    # === 2. Format Data for CrewAI Input ===
    news_items = serper_results["serper_results"]
    eea_items = serper_results["eea_context_sources"]

    serper_data_text = "\n\n".join(
        f"Title: {item['title']}\nDate: {item['date']}\nLink: {item['link']}\nSnippet: {item['snippet']}"
        for item in news_items
    )
    serper_data_text += "\n\nEEA Sources:\n" + "\n".join(f"{item['title']} - {item['url']}" for item in eea_items)

    # === 3. CrewAI Setup ===
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
    final_output_text = str(final_output)

    # === 4. Save Summary to SQLite ===
    db_path = "summaries/sustainability.db"
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO sustainability_reports (date, content)
        VALUES (?, ?)
    """, (summary_date, final_output_text))

    conn.commit()
    conn.close()

    print(f"\n📦 Summary for {summary_date} saved to {db_path}")

    # === 5. Export All Summaries to JSON ===
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT date, content FROM sustainability_reports ORDER BY date DESC")
    rows = cursor.fetchall()
    conn.close()

    summaries_json = [
        {"date": row[0], "content": row[1]} for row in rows
    ]

    json_export_path = "summaries/summaries.json"
    with open(json_export_path, "w", encoding="utf-8") as f:
        json.dump(summaries_json, f, indent=2)

    print(f"📤 Exported all summaries to JSON: {json_export_path}")

if __name__ == "__main__":
    main()
