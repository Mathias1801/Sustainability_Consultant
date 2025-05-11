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
    # === Directory Setup ===
    os.makedirs("data", exist_ok=True)
    os.makedirs("data/weekly_log", exist_ok=True)
    os.makedirs("data/weekly_summary", exist_ok=True)
    os.makedirs("data/weekly_consultation", exist_ok=True)
    os.makedirs("data/attribution", exist_ok=True)
    os.makedirs("docs/_data", exist_ok=True)

    # === Paths ===
    summary_date = datetime.now().strftime('%Y-%m-%d')
    db_path = "data/sustainability.db"

    json_log_path = f"data/weekly_log/sustainability_sources_{summary_date}.json"
    json_summary_path = f"data/weekly_summary/sustainability_summary_{summary_date}.json"
    json_consultation_path = f"data/weekly_consultation/business_consultation_{summary_date}.json"
    json_attribution_path = f"data/attribution/attribution_{summary_date}.json"

    current_summary_path = "docs/_data/current_summary.json"
    current_consultation_path = "docs/_data/current_consultation.json"

    # === Fetch Articles ===
    serper_results = fetch_sustainability_articles()
    with open(json_log_path, "w", encoding="utf-8") as f:
        json.dump(serper_results, f, indent=2)

    news_items = serper_results["serper_results"]
    serper_data_text = "\n\n".join(
        f"Title: {item['title']}\nDate: {item['date']}\nLink: {item['link']}\nSnippet: {item['snippet']}\nText: {item.get('text', '')}"
        for item in news_items
    )

    # === Run Summarization ===
    agents = CustomAgents()
    tasks = CustomTasks()

    summarize_agent = agents.summarize_agent()
    summarize_task = tasks.summarize_task(summarize_agent, serper_data_text)

    crew = Crew(agents=[summarize_agent], tasks=[summarize_task], verbose=True)
    print("\n🚀 Running the Crew...\n")
    final_output = crew.kickoff()
    final_output_text = str(final_output)

    with open(json_summary_path, "w", encoding="utf-8") as f:
        json.dump({"date": summary_date, "content": final_output_text}, f, indent=2)
    with open(current_summary_path, "w", encoding="utf-8") as f:
        json.dump({"date": summary_date, "content": final_output_text}, f, indent=2)

    # === Run Business Consultation ===
    business_agent = agents.business_alignment_agent()
    business_task = tasks.business_alignment_task(business_agent, final_output_text)

    business_crew = Crew(agents=[business_agent], tasks=[business_task], verbose=True)
    print("\n🏢 Running Business Consultation Crew...\n")
    business_output = business_crew.kickoff()
    business_output_text = str(business_output)

    with open(json_consultation_path, "w", encoding="utf-8") as f:
        json.dump({"date": summary_date, "content": business_output_text}, f, indent=2)
    with open(current_consultation_path, "w", encoding="utf-8") as f:
        json.dump({"date": summary_date, "content": business_output_text}, f, indent=2)

    # === Run Attribution ===
    attribution_agent = agents.attribution_agent()

    with open(json_log_path, "r", encoding="utf-8") as f:
        raw_source_data = json.load(f)

    source_data_text = "\n\n".join(
        f"Title: {item['title']}\nDate: {item['date']}\nSnippet: {item['snippet']}\nText: {item.get('text', '')}"
        for item in raw_source_data["serper_results"]
    )

    attribution_task = tasks.attribution_task(
        agent=attribution_agent,
        summary_text=final_output_text,
        consultation_text=business_output_text,
        source_data_text=source_data_text
    )

    attribution_crew = Crew(agents=[attribution_agent], tasks=[attribution_task], verbose=True)
    print("\n🔎 Running Attribution Crew...\n")
    attribution_output = attribution_crew.kickoff()
    attribution_output_text = str(attribution_output)

    with open(json_attribution_path, "w", encoding="utf-8") as f:
        json.dump({"date": summary_date, "content": attribution_output_text}, f, indent=2)
    print(f"📎 Attribution file saved for {summary_date}")

    # === Save to Database ===
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # === Table Creation ===
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
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS consultancy (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT UNIQUE,
            content TEXT
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS attribution (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT UNIQUE,
            content TEXT
        )
    """)

    # === Insert Summary ===
    cursor.execute("SELECT COUNT(*) FROM summary_reports WHERE date = ?", (summary_date,))
    if cursor.fetchone()[0] == 0:
        cursor.execute("""
            INSERT INTO summary_reports (date, content)
            VALUES (?, ?)
        """, (summary_date, final_output_text))
        print(f"📦 Summary inserted for {summary_date}")
    else:
        print(f"⚠️ Summary for {summary_date} already exists. Skipping insert.")

    # === Insert Consultation ===
    cursor.execute("SELECT COUNT(*) FROM consultancy WHERE date = ?", (summary_date,))
    if cursor.fetchone()[0] == 0:
        cursor.execute("""
            INSERT INTO consultancy (date, content)
            VALUES (?, ?)
        """, (summary_date, business_output_text))
        print(f"📦 Business consultation inserted for {summary_date}")
    else:
        print(f"⚠️ Consultation for {summary_date} already exists. Skipping insert.")

    # === Insert Attribution ===
    cursor.execute("SELECT COUNT(*) FROM attribution WHERE date = ?", (summary_date,))
    if cursor.fetchone()[0] == 0:
        cursor.execute("""
            INSERT INTO attribution (date, content)
            VALUES (?, ?)
        """, (summary_date, attribution_output_text))
        print(f"📘 Attribution inserted for {summary_date}")
    else:
        print(f"⚠️ Attribution for {summary_date} already exists. Skipping insert.")

    # === Insert Sources ===
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

    print(f"📥 Inserted {inserted_count} new source entries for {summary_date}")

    conn.commit()
    conn.close()

if __name__ == "__main__":
    main()
