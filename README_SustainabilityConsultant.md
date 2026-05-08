# Sustainability Consultant

An automated LLM pipeline that generates weekly sustainability intelligence reports, strategic business consultations, and source attribution — designed for corporate strategy teams and demonstrated with Maersk as an example company.

**Live application:** [mathias1801.github.io/Sustainability_Consultant](https://mathias1801.github.io/Sustainability_Consultant/)

---

## What This Project Demonstrates

- End-to-end LLM pipeline orchestration: web search, summarisation, business analysis, and attribution as modular stages
- Automated scheduling via GitHub Actions (weekly summary pipeline + daily ratings sync)
- Hosted REST API on Render for user feedback and ratings collection
- Structured JSON data architecture feeding both a SQLite store and a static GitHub Pages frontend
- Prompt engineering for domain-specific outputs: sustainability summaries, strategic business relevance analysis, and citation attribution with unsupported-claim flagging
- Separation of live data (`/data/`) from frontend-served data (`/docs/_data/`) for clean static site deployment

---

## Overview

The system runs on two automated schedules. Once a week, it searches for current sustainability news using the Serper API, summarises the articles with Google Gemini, generates a strategic business consultation relevant to the target company, and attributes all claims back to their original sources. Outputs are written to dated JSON files and a SQLite database, with the current summary and consultation copied to `/docs/_data/` for the live frontend.

A separate daily workflow syncs user ratings submitted through the Render-hosted API back into the repository, keeping the frontend up to date with any feedback made since the last weekly run.

---

## Application Flow

```
Weekly trigger (GitHub Actions)
        │
        ▼
serper_search.py          Fetches current sustainability news articles
        │
        ▼
summarize_module.py       Summarises articles via Gemini LLM
consultation_module.py    Generates strategic business relevance analysis
attribution_module.py     Attributes claims to source documents
        │
        ▼
app.py                    Orchestrates all modules end-to-end
        │
        ├──▶ /data/        Dated JSON logs + SQLite storage
        └──▶ /docs/_data/  Current summary + consultancy for frontend


Daily trigger (GitHub Actions)
        │
        ▼
sync_ratings.yml          Pulls new user ratings from Render API
        └──▶ /data/        Updates attribution and feedback records
```

---

## Project Structure

```
.
├── data/
│   ├── weekly_log/                              # Raw fetched sources (dated JSON)
│   ├── weekly_summary/                          # LLM summaries (dated JSON)
│   ├── weekly_consultation/                     # Business consultations (dated JSON)
│   ├── attribution/                             # Source attribution (dated JSON)
│   └── sustainability.db                        # SQLite storage
│
├── docs/
│   ├── _data/
│   │   ├── current_summary.json                 # Live data for frontend
│   │   └── current_consultancy.json
│   ├── _layouts/
│   ├── _pages/
│   ├── assets/css/
│   └── _config.yml
│
├── render/
│   └── submit_rating.py                         # Render-hosted API for ratings
│
├── scripts/
│   ├── app.py                                   # End-to-end pipeline runner
│   ├── serper_search.py                         # News search via Serper API
│   ├── summarize_module.py                      # LLM summarisation
│   ├── consultation_module.py                   # Strategic business analysis
│   ├── attribution_module.py                    # Source attribution + claim flagging
│   └── llm_utils.py                             # Gemini API wrapper
│
└── .github/workflows/
    ├── run-sustainability-summary.yml           # Weekly pipeline trigger
    └── sync_ratings.yml                         # Daily ratings sync trigger
```

---

## GitHub Actions Workflows

**`run-sustainability-summary.yml`** — triggers weekly, runs the full pipeline from news fetch through to JSON and SQLite output, and copies current data to `/docs/_data/` for the live frontend.

**`sync_ratings.yml`** — triggers daily, checks the Render API for any new user ratings submitted since the last sync and writes them back into the repository.

---

## Tech Stack

| Layer | Technology |
|---|---|
| LLM | Google Gemini 2.5 |
| News search | Serper API |
| Ratings API | Python, hosted on Render |
| Storage | SQLite + dated JSON files |
| Frontend | Static site via GitHub Pages |
| Automation | GitHub Actions |
| Core language | Python |

---

## Notes

- Example company used throughout: Maersk
- Attribution is LLM-assisted and flags claims that cannot be grounded in the retrieved sources
- All outputs are saved in both JSON and SQLite for flexible downstream use
- This is an MVP — architecture and outputs may evolve
