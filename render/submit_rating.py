import os
import sqlite3
from flask import Flask, request, jsonify
from flask_cors import CORS

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
            report_date TEXT NOT NULL,
            rating INTEGER CHECK(rating BETWEEN 1 AND 5),
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()
    print("✅ ratings table ensured")

init_db()


@app.route('/submit-rating', methods=['POST'])
def submit_rating():
    data = request.get_json()
    report_date = data.get('report_date')
    rating = data.get('rating')

    if not (report_date and rating and 1 <= int(rating) <= 5):
        return jsonify({'status': 'error', 'message': 'Invalid input'}), 400

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO ratings (report_date, rating) VALUES (?, ?)", (report_date, int(rating)))
    conn.commit()
    conn.close()

    return jsonify({'status': 'success'}), 200

@app.route('/average-rating', methods=['GET'])
def average_rating():
    report_date = request.args.get('report_date')
    if not report_date:
        return jsonify({'average': None})
    
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT AVG(rating) FROM ratings WHERE report_date = ?", (report_date,))
    avg = c.fetchone()[0]
    conn.close()

    return jsonify({'average': round(avg, 2) if avg else None})

@app.route('/debug-ratings', methods=['GET'])
def debug_ratings():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT id, report_date, rating, timestamp FROM ratings ORDER BY timestamp DESC LIMIT 10")
    rows = c.fetchall()
    conn.close()
    return '<br>'.join([f"{row[0]} | {row[1]} | {row[2]} | {row[3]}" for row in rows])

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

