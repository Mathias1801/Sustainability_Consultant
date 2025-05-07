import sqlite3
import requests
import os

API_URL = "https://sustainability-ratings-api.onrender.com/download-ratings"
DB_PATH = "data/sustainability.db"

def ensure_schema(conn):
    c = conn.cursor()

    # Create table if it doesn't exist
    c.execute("""
        CREATE TABLE IF NOT EXISTS ratings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            consultation_upload_date TEXT,
            rating INTEGER CHECK(rating BETWEEN 1 AND 5),
            timestamp TEXT DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(consultation_upload_date, timestamp)
        )
    """)

    c.execute("PRAGMA table_info(ratings)")
    existing_columns = [row[1] for row in c.fetchall()]
    if "consultation_upload_date" not in existing_columns:
        c.execute("ALTER TABLE ratings ADD COLUMN consultation_upload_date TEXT")
    if "timestamp" not in existing_columns:
        c.execute("ALTER TABLE ratings ADD COLUMN timestamp TEXT")

    conn.commit()

def main():
    print("📥 Fetching ratings from API...")
    response = requests.get(API_URL)
    response.raise_for_status()
    new_ratings = response.json()

    if not new_ratings:
        print("No new ratings to insert.")
        return

    conn = sqlite3.connect(DB_PATH)
    ensure_schema(conn)
    c = conn.cursor()

    inserted = 0
    for entry in new_ratings:
        try:
            c.execute("""
                INSERT OR IGNORE INTO ratings (consultation_upload_date, rating, timestamp)
                VALUES (?, ?, ?)
            """, (
                entry["consultation_upload_date"],
                entry["rating"],
                entry["timestamp"]
            ))
            inserted += c.rowcount
        except Exception as e:
            print(f"❌ Error inserting row: {e}")

    conn.commit()
    conn.close()
    print(f"✅ Inserted {inserted} new ratings.")

if __name__ == "__main__":
    main()
