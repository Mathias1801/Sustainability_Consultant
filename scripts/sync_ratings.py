import sqlite3
import requests
import os

API_URL = "https://sustainability-ratings-api.onrender.com/download-ratings"
DB_PATH = "data/sustainability.db"

def ensure_ratings_table(conn):
    c = conn.cursor()

    # Check if table exists
    c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='ratings'")
    if c.fetchone() is None:
        print("🛠 'ratings' table not found. Creating it...")
        c.execute("""
            CREATE TABLE ratings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                consultation_upload_date TEXT,
                rating INTEGER CHECK(rating BETWEEN 1 AND 5),
                timestamp TEXT DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(rating, timestamp)
            )
        """)
        conn.commit()
        print("✅ 'ratings' table created.")
    else:
        print("✅ 'ratings' table exists.")

def main():
    print("📥 Fetching ratings from API...")
    response = requests.get(API_URL)
    response.raise_for_status()
    new_ratings = response.json()

    if not new_ratings:
        print("No new ratings to insert.")
        return

    conn = sqlite3.connect(DB_PATH)
    ensure_ratings_table(conn)
    c = conn.cursor()

    inserted = 0
    for entry in new_ratings:
        try:
            print(f"\n🔍 Trying to insert: rating={entry['rating']} | timestamp={entry['timestamp']}")
            c.execute("""
                INSERT OR IGNORE INTO ratings (consultation_upload_date, rating, timestamp)
                VALUES (?, ?, ?)
            """, (
                entry["consultation_upload_date"],
                entry["rating"],
                entry["timestamp"]
            ))

            if c.rowcount == 0:
                print("⚠️  Skipped (rating + timestamp already exists)")
            else:
                print("✅ Inserted")
                inserted += 1

        except Exception as e:
            print(f"❌ Error inserting row: {e}")

    conn.commit()
    conn.close()
    print(f"\n✅ Done. Inserted {inserted} new rating(s).")

if __name__ == "__main__":
    main()
