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
            consultation_upload_date TEXT,
            rating INTEGER CHECK(rating BETWEEN 1 AND 5),
            timestamp TEXT DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(consultation_upload_date, timestamp)
        )
    """)
    conn.commit()
    conn.close()
    print("✅ ratings table ensured")

init_db()

@app.route('/submit-rating', methods=['POST'])
def submit_rating():
    data = request.get_json()
    consultation_upload_date = data.get('consultation_upload_date')
    rating = data.get('rating')

    if not (consultation_upload_date and rating and 1 <= int(rating) <= 5):
        return jsonify({'status': 'error', 'message': 'Invalid input'}), 400

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        INSERT OR IGNORE INTO ratings (consultation_upload_date, rating)
        VALUES (?, ?)
    """, (consultation_upload_date, int(rating)))
    conn.commit()
    conn.close()

    return jsonify({'status': 'success'}), 200

@app.route('/average-rating', methods=['GET'])
def average_rating():
    consultation_upload_date = request.args.get('consultation_upload_date')
    if not consultation_upload_date:
        return jsonify({'average': None})

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT AVG(rating) FROM ratings WHERE consultation_upload_date = ?", (consultation_upload_date,))
    avg = c.fetchone()[0]
    conn.close()

    return jsonify({'average': round(avg, 2) if avg else None})

@app.route('/download-ratings', methods=['GET'])
def download_ratings():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT consultation_upload_date, rating, timestamp FROM ratings ORDER BY timestamp DESC")
    rows = c.fetchall()
    conn.close()

    return jsonify([
        {
            "consultation_upload_date": r[0],
            "rating": r[1],
            "timestamp": r[2]
        }
        for r in rows
    ])

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
