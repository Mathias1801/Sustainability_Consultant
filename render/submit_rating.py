from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)

DB_PATH = 'data/sustainability.db'

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
