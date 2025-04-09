# Exam_MLOps_MFE

https://mathias1801.github.io/Exam_MLOps_MFE/ 

![Screenshot](images/flowchart.png)

# Application Setup

The application utilizes GitHub Actions to run a pipeline set up to fetch news related to the sustainability cause relevant to businesses. The main pipeline is driven via the `app.py` script, which utilizes the backend scripts and updates data for the frontend.

---

## Backend

The backend process starts with `serper_search.py`, which utilizes the web scraping tool **Serper**, a Google web scraping API. Specific sources are provided to influence the scraping (e.g., from the EEA), wwhile a query for unspecified sources is also utilized to find outside sources in general as well. For the purpose of this repository these query metrics are hardcoded, however in the future one could imagine it being dynamic query parameters decided by the user of the application. These found sources are stored in `.json` format in the `data/weekly_log/` folder, as well as in the `source_log` table in the `sustainability.db` database, where each individual source is stored as a separate row.

After the sources are found, the next part of the backend process utilizes an agentic LLM system to transform these sources into readable summaries by filtering out irrelevant information. The `summarize_agent` in `agent.py` and the task `summarize_task` in `tasks.py` include specific instructions regarding role, function, and treatment of the input data using an n-shot prompting approach. A single example is provided to help guide the LLM toward producing consistently structured and relevant summaries.

This part of the process is crucial, as it dictates the future usability and analytical potential of the summaries. The application performs best when the summaries remain consistent in structure, supporting data analysis over time.

The output of the agentic system is saved as a `.json` file in `data/weekly_summary/`, and also overwrites the `current_summary.json` file in `docs/_data/`, which dictates the content displayed on the frontend GitHub page. Additionally, the summary is stored in the `summary_reports` table in `sustainability.db`.

These backend components are executed via the `app.py` script, which is triggered by a GitHub Actions workflow defined in the YAML file `.github/workflows/run-sustainability-summary.yml`. This file grants permissions to add and overwrite data in the repository, enabling new data updates on a weekly basis.

The `app.py` script serves as the glue connecting the Serper-based scraping and the LLM summarization, while also ensuring proper storage of outputs.

The outputs of `app.py` are written to the folders `data/` and `docs/_data/`, and to the `sustainability.db` database.

### Database Structure

#### `summary_reports`:

| Column Name | Type    | Description                                  |
|-------------|---------|----------------------------------------------|
| `id`        | INTEGER | Auto-incrementing primary key                |
| `date`      | TEXT    | Date of the summary (e.g., `2025-04-09`)     |
| `content`   | TEXT    | The full summary text                        |

#### `source_log`:

| Column Name   | Type    | Description                                           |
|---------------|---------|-------------------------------------------------------|
| `id`          | INTEGER | Auto-incrementing primary key                         |
| `report_date` | TEXT    | Date of the associated summary                        |
| `title`       | TEXT    | Title of the article/source                           |
| `date`        | TEXT    | Publication date of the article (if available)        |
| `link`        | TEXT    | URL to the article or source                          |
| `snippet`     | TEXT    | Short summary or snippet from the article             |
| `text`        | TEXT    | Full scraped article text (if available)              |
| `source_type` | TEXT    | Either `"serper"` or `"eea"`                          |

---

## Frontend

For frontend purposes, HTML and CSS are used in combination with GitHub Pages, which provides a hosted webpage with multiple tabs. The HTML and CSS files are located in the `docs/` folder, which includes the following subfolders:

- `_data/`
- `_layouts/`
- `_pages/`
- `assets/css/`

In the `docs/_data/` folder, you will find the file `current_summary.json`, which holds the content for the **Weekly Summary** page. This file is automatically updated by the GitHub Actions workflow that triggers `app.py`, which overwrites the `current_summary.json` file with the latest LLM-generated summaries.

The other folders—`_layouts/`, `_pages/`, and `assets/css/`—contain the layout templates, static page content, and styling rules that define the appearance and structure of the GitHub Pages site.

