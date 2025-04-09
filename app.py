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
    # === 1. Set up folders
    os.makedirs("data/weekly_log", exist_ok=True)
    os.makedirs("data/weekly_summary", exist_ok=True)
    os.makedirs("data/active", exist_ok=True)

    # === 2. Define paths
    summary_date = datetime.now().strftime('%Y-%m-%d')
    db_path = "data/sustainability.db"
    txt_filename = f"sustainability_summary_{summary_date}.txt"
    txt_path = os.path.join("data", "weekly_summary", txt_filename)
    active_path = os.path.join("data", "active", txt_filename)
    json_filename = f"sustainability_sources_{summary_date}.json"
    json_path = os.path.join("data", "weekly_log", json_filename)
    json_export_path = "data/summaries.json"

    print(f"📅 Summary date: {summary_date}")
    print(f"🔍 Using DB path: {os.path.abspath(db_path)}")

    # === 3. Run Serper + enrich + save to JSON
    serper_results = fetch_sustainability_articles()

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(serper_results, f, indent=2)
    print(f"✅ Serper results saved to: {json_path}")

    # === 4. Prepare input for LLM summarization
    news_items = serper_results["serper_results"]
    eea_items = serper_results["eea_context_sources"]

    serper_data_text = "\n\n".join(
        f"Title: {item['title']}\nDate: {item['date']}\nLink: {item['link']}\nSnippet: {item['snippet']}\nText: {item.get('text', '')}"
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

    # === 6. Save summary .txt to weekly_summary
    with open(txt_path, "w", encoding="utf-8") as f:
        f.write(final_output_text)
    print(f"📝 Saved summary to: {txt_path}")

    # === 7. Also copy it to active/
    with open(active_path, "w", encoding="utf-8") as f:
        f.write(final_output_text)
    print(f"📥 Copied summary to active folder: {active_path}")

    # === 8. Prune active folder to max 4 entries
    try:
        active_files = [
            f for f in os.listdir("data/active")
            if f.startswith("sustainability_summary_") and f.endswith(".txt")
        ]
        if len(active_files) > 4:
            active_files.sort()  # Sorted by filename = date
            files_to_delete = active_files[:-4]
            for old_file in files_to_delete:
                full_path = os.path.join("data/active", old_file)
                os.remove(full_path)
                print(f"🗑️ Deleted old active file: {full_path}")
        else:
            print(f"✅ Active folder has {len(active_files)} file(s); no cleanup needed.")
    except Exception as e:
        print(f"⚠️ Active folder cleanup error: {e}")

    # === 9. Insert into SQLite
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

    # === 10. Summary count + DB Export
    try:
        cursor.execute("SELECT COUNT(*) FROM sustainability_reports")
        count = cursor.fetchone()[0]
        print(f"\n🧠 Total summaries in DB: {count}")

        cursor.execute("SELECT date, substr(content, 1, 100) FROM sustainability_reports ORDER BY id DESC LIMIT 5")
        recent = cursor.fetchall()
        print("\n📝 Last 5 entries:")
        for date, snippet in recent:
            print(f"- {date}: {snippet.strip()}...")

        cursor.execute("SELECT date, content FROM sustainability_reports ORDER BY date DESC")
        rows = cursor.fetchall()
        summaries_json = [{"date": row[0], "content": row[1]} for row in rows]

        with open(json_export_path, "w", encoding="utf-8") as f:
            json.dump(summaries_json, f, indent=2)

        print(f"📤 Exported all summaries to JSON: {json_export_path}")
    except Exception as e:
        print(f"❌ Failed summary export: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    main()
