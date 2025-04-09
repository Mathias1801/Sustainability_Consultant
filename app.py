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
    os.makedirs("data", exist_ok=True)
    os.makedirs("data/weekly_log", exist_ok=True)
    os.makedirs("data/weekly_summary", exist_ok=True)
    os.makedirs("docs/_data", exist_ok=True)

    summary_date = datetime.now().strftime('%Y-%m-%d')
    db_path = "data/sustainability.db"
    json_summary_path = f"data/weekly_summary/sustainability_summary_{summary_date}.json"
    json_log_path = f"data/weekly_log/sustainability_sources_{summary_date}.json"
    current_summary_path = "docs/_data/current_summary.json"

    serper_results = fetch_sustainability_articles()

    with open(json_log_path, "w", encoding="utf-8") as f:
        json.dump(serper_results, f, indent=2)

    news_items = serper_results["serper_results"]
    eea_items = serper_results["eea_context_sources"]

    serper_data_text = "\n\n".join(
        f"Title: {item['title']}\nDate: {item['date']}\nLink: {item['link']}\nSnippet: {item['snippet']}\nText: {item.get('text', '')}"
        for item in news_items
    )
    serper_data_text += "\n\nEEA Sources:\n" + "\n".join(f"{item['title']} - {item['url']}" for item in eea_items)

    agents = CustomAgents()
    tasks = CustomTasks()
    summarize_agent = agents.summarize_agent()
    summarize_task = tasks.summarize_task(summarize_agent, serper_data_text)

    crew = Crew(agents=[summarize_agent], tasks=[summarize_task], verbose=True)

    print("\n🚀 Running the Crew...\n")
    final_output = crew.kickoff()
    final_output_text = str(final_output)

    with open(json_summary_path, "w", encoding="utf-8") as f:
        json.dump({
            "date": summary_date,
            "content": final_output_text
        }, f, indent=2)

    with open(current_summary_path, "w", encoding="utf-8") as f:
        json.dump({
            "date": summary_date,
            "content": final_output_text
        }, f, indent=2)

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Create tables if they don't exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS summary_reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT UNIQUE,
            content TEXT
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS source_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            report_date TEXT,
            title TEXT,
            date TEXT,
            link TEXT,
            snippet TEXT,
            text TEXT,
            source_type TEXT,
            UNIQUE(report_date, title, link)
        )
    """)

    # Insert summary only if it doesn’t already exist
    cursor.execute("SELECT COUNT(*) FROM summary_reports WHERE date = ?", (summary_date,))
    if cursor.fetchone()[0]:
        print(f"⚠️ Summary for {summary_date} already exists. Skipping insert.")
    else:
        cursor.execute("""
            INSERT INTO summary_reports (date, content)
            VALUES (?, ?)
        """, (summary_date, final_output_text))
        print(f"📦 Summary inserted for {summary_date}")

    # Insert sources, avoiding duplicates
    inserted_count = 0
    for item in news_items:
        try:
            cursor.execute("""
                INSERT OR IGNORE INTO source_log (report_date, title, date, link, snippet, text, source_type)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                summary_date,
                item.get('title', ''),
                item.get('date', ''),
                item.get('link', ''),
                item.get('snippet', ''),
                item.get('text', ''),
                "serper"
            ))
            inserted_count += cursor.rowcount
        except Exception as e:
            print(f"❌ Failed to insert serper source: {e}")

    for item in eea_items:
        try:
            cursor.execute("""
                INSERT OR IGNORE INTO source_log (report_date, title, date, link, snippet, text, source_type)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                summary_date,
                item.get('title', ''),
                '',
                item.get('url', ''),
                '',
                '',
                "eea"
            ))
            inserted_count += cursor.rowcount
        except Exception as e:
            print(f"❌ Failed to insert EEA source: {e}")

    print(f"📥 Inserted {inserted_count} new source entries for {summary_date}")

    conn.commit()
    conn.close()

if __name__ == "__main__":
    main()
