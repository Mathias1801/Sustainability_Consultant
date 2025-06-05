# 🌱 Sustainability Consultant

A modular system that uses LLMs and curated sustainability data to generate insightful weekly sustainability reports, business consultations, and source attribution for corporate strategy teams—tailored to companies like Maersk.

---

## 🔗 Live Application

[Explore the Live Application](https://mathias1801.github.io/Sustainability_Consultant/)

---

## 🧭 Project Overview

This project automatically:

1. **Fetches Weekly Sustainability News**
2. **Summarizes Articles using LLMs**
3. **Analyzes Strategic Business Relevance**
4. **Performs Attribution to Original Sources**
5. **Stores Data in SQLite**
6. **Provides a Flask API for User Ratings**

All components are automated and can run as a scheduled workflow.

---

## 📊 Application Flow

![Application Flowchart](images/flowchart.png)

---

## 📂 Folder Structure

```
.
├── data/                          # Weekly JSON logs and source data
│   ├── weekly_log/
│   ├── weekly_summary/
│   ├── weekly_consultation/
│   ├── attribution/
│   └── sustainability.db         # SQLite storage
├── docs/_data/                   # Live JSON data for frontend rendering
├── render/submit_rating.py       # Flask API to handle feedback and ratings
├── scripts/                      # Main automation scripts
│   ├── app.py                    # End-to-end pipeline runner
│   ├── attribution_module.py
│   ├── consultation_module.py
│   ├── summarize_module.py       # (external)
│   └── llm_utils.py              # Gemini API wrapper
└── .github/workflows/            # GitHub Actions automation
```

---

## ⚙️ Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/Mathias1801/Sustainability_Consultant.git
cd Sustainability_Consultant
```

### 2. Install Requirements
```bash
pip install -r requirements.txt
```

### 3. Add Environment Variables

Create a `.env` file with your Google Gemini API key:
```
GEMINI_API_KEY=your_api_key_here
```

### 4. Run the Pipeline
```bash
python scripts/app.py
```

This will populate the `data/` and `docs/_data/` folders with summaries, consultations, and attributions.

---

## 🖥️ Run the Flask Rating API

To start the rating server:
```bash
python render/submit_rating.py
```

Endpoints:
- `POST /submit-rating`
- `GET /average-rating`
- `GET /download-ratings`

---

## 🔁 GitHub Actions

Two workflows are included:
- `run-sustainability-summary.yml`: Automates the weekly pipeline.
- `sync_ratings.yml`: Manages ratings data.

---

## 🧠 Tech Stack

- **LLMs**: Google Gemini 2.5
- **Flask**: API for feedback
- **SQLite**: Lightweight local storage
- **GitHub Actions**: Automation
- **Python**: Core scripting and orchestration

---

## 📌 Notes

- Example company: **Maersk**
- Attribution is LLM-assisted but flags unsupported claims
- Output is saved both in JSON and SQLite for flexible use

---

## 🤝 Contributions

Feel free to fork and extend this project to support more companies or integrate other data sources. PRs welcome!
