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
    os.makedirs("summaries", exist_ok=True)

    # === 1. Set up date and paths
    summary_date = datetime.now().strftime('%Y-%m-%d')
    db_path = "summaries/sustainability.db"
    txt_path = f"summaries/sustainability_summary_{summary_date}.txt"
    json_filename = f"summaries/sustainability_sources_{summary_date}.json"
    json_export_path = "summaries/summaries.json"

    # === 2. DEBUG: Check environment and files
    print(f"📅 Summary date: {summary_date}")
    print(f"🔍 Using DB path: {os.path.abspath(db_path)}")
    print(f"📂 Contents of summaries/: {os.listdir('summaries')}")

    # === 3. Run Serper search and save raw JSON
    serper_results = fetch_sustainability_articles()

    with open(json_filename, "w", encoding="utf-8") as f:
        json.dump(serper_results, f, indent=2)
    print(f"\n✅ Serper results saved to: {json_filename}")

    # === 4. Prepare input for summarization
    news_items = serper_results["serper_results"]
    eea_items = serper_results["eea_context_sources"]

    serper_data_text = "\n\n".join(
        f"Title: {item['title']}\nDate: {item['date']}\nLink: {item['link']}\nSnippet: {item['snippet']}"
        for item in news_items
    )
    serper_data_text += "\n\nEEA Sources:\n" + "\n".join(f"{item['title']} - {item['url']}" for item in eea_items)

    # === 5. CrewAI summarization
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

    # === 6. Write output to .txt file
    with open(txt_path, "w", encoding="utf-8") as f:
        f.write(final_output_text)
    print(f"📝 Backup .txt saved to: {txt_path}")

    # === 7. Insert into SQLite DB
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        cursor.execute("""
            INSERT INTO sustainability_reports (date, content)
            VALUES (?, ?)
        """, (summary_date, final_output_text))
        conn.commit()
        print(f"📦 Summary inserted into DB for date: {summary_date}")
    except Exception as e:
        print(f"❌ Failed to insert into DB: {e}")

    # === 8. Debug: How many records are in DB now?
    try:
        cursor.execute("SELECT COUNT(*) FROM sustainability_reports")
        count = cursor.fetchone()[0]
        print(f"\n🧠 Total summaries in DB: {count}")

        cursor.execute("SELECT date, substr(content, 1, 100) FROM sustainability_reports ORDER BY id DESC LIMIT 5")
        recent = cursor.fetchall()
        print("\n📝 Last 5 entries:")
        for date, snippet in recent:
            print(f"- {date}: {snippet.strip()}...")
    except Exception as e:
        print(f"❌ Failed DB inspection: {e}")

    conn.close()

    # === 9. Export DB to JSON for GitHub Pages
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT date, content FROM sustainability_reports ORDER BY date DESC")
        rows = cursor.fetchall()
        conn.close()

        summaries_json = [{"date": row[0], "content": row[1]} for row in rows]

        with open(json_export_path, "w", encoding="utf-8") as f:
            json.dump(summaries_json, f, indent=2)

        print(f"📤 Exported all summaries to JSON: {json_export_path}")
    except Exception as e:
        print(f"❌ Failed to export summaries.json: {e}")

if __name__ == "__main__":
    main()
