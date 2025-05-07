import sqlite3
import requests
import os

API_URL = "https://sustainability-ratings-api.onrender.com/download-ratings"
DB_PATH = "data/sustainability.db"

def main():
    response = requests.get(API_URL)
    response.raise_for_status()
    new_ratings = response.json()

    if not new_ratings:
        print("No new ratings to insert.")
        return

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS ratings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            report_date TEXT NOT NULL,
            rating INTEGER CHECK(rating BETWEEN 1 AND 5),
            timestamp TEXT,
            UNIQUE(report_date, timestamp)
        )
    """)

    inserted = 0
    for entry in new_ratings:
        try:
            c.execute("""
                INSERT OR IGNORE INTO ratings (report_date, rating, timestamp)
                VALUES (?, ?, ?)
            """, (entry["report_date"], entry["rating"], entry["timestamp"]))
            inserted += c.rowcount
        except Exception as e:
            print(f"Error inserting row: {e}")

    conn.commit()
    conn.close()
    print(f"✅ Inserted {inserted} new ratings.")

if __name__ == "__main__":
    main()
