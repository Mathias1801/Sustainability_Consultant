from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import os

app = Flask(__name__)
CORS(app)

DB_PATH = 'data/sustainability.db'
os.makedirs('data', exist_ok=True)

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS ratings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            type TEXT NOT NULL,
            content_date TEXT NOT NULL,
            rating INTEGER CHECK(rating BETWEEN 1 AND 5),
            timestamp TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()
    print("✅ ratings table ensured")

init_db()

@app.route('/submit-rating', methods=['POST'])
def submit_rating():
    data = request.get_json()
    rating_type = data.get('type')  # 'weekly_news' or 'business_consultancy'
    content_date = data.get('content_date')
    rating = data.get('rating')

    if not (rating_type and content_date and rating and 1 <= int(rating) <= 5):
        return jsonify({'status': 'error', 'message': 'Invalid input'}), 400

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        INSERT INTO ratings (type, content_date, rating)
        VALUES (?, ?, ?)
    """, (rating_type, content_date, int(rating)))
    conn.commit()
    conn.close()

    return jsonify({'status': 'success'}), 200

@app.route('/average-rating', methods=['GET'])
def average_rating():
    rating_type = request.args.get('type')
    content_date = request.args.get('content_date')
    if not (rating_type and content_date):
        return jsonify({'average': None})

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        SELECT AVG(rating) FROM ratings
        WHERE type = ? AND content_date = ?
    """, (rating_type, content_date))
    avg = c.fetchone()[0]
    conn.close()

    return jsonify({'average': round(avg, 2) if avg else None})

@app.route('/download-ratings', methods=['GET'])
def download_ratings():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT type, content_date, rating, timestamp FROM ratings ORDER BY timestamp DESC")
    rows = c.fetchall()
    conn.close()

    return jsonify([
        {
            "type": row[0],
            "content_date": row[1],
            "rating": row[2],
            "timestamp": row[3]
        }
        for row in rows
    ])

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
