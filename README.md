# StatGenie: A Learning Journey into Local NL2SQL ⚾

StatGenie is an experimental **Text-to-SQL (NL2SQL)** data agent built to explore the challenges of on-device AI and natural language interfaces for structured data.

This project started as a way to apply what I learned about local LLMs in class, using a familiar MLB batting dataset as a testing ground. It is less about being a "perfect tool" and more about the architectural decisions and roadblocks encountered while building it.

## 💡 Inspiration: The "Genie"
This project is inspired by **Databricks Genie**, an AI/BI feature that allows users to chat with their data. Genie works by:
- **Semantic Mapping:** Using metadata and a "Knowledge Store" to translate business terms into technical columns.
- **Trust & Verification:** Providing the underlying SQL so users can trust the answer.
- **Feedback Loops:** Allowing analysts to "teach" the agent through instructions and example queries.

StatGenie is my attempt to build a "miniature," local version of this — one that is agnostic enough to eventually work with any dataset (batting, fielding, or even non-sports data) just by swapping the schema and database.

## 🚀 Technical Setup
- **Model:** Liquid AI LFM2-8B (LFM2-8B-A1B-Q4_K_M)
- **Engine:** llama.cpp (`llama-server`) on Port 8080
- **Orchestration:** Minimal — plain Python with direct OpenAI-compatible API calls
- **Database:** SQLite
- **Frontend:** Streamlit

To run the app:
```bash
# 1. Start the local LLM server
llama-server --model <path-to-model> --port 8080

# 2. Launch the interface
streamlit run app.py
```

## 🏗️ Architecture: Multi-LLM Router

One of the core lessons from building this was that a single LLM chain doing everything — routing, SQL generation, and response formatting — produces poor results. The current architecture separates these concerns across three LLM calls:

```
User Message
    │
    ▼
[LLM 1 — Router]  ──── casual question? ──→  direct answer (like a support chatbot)
    │                   off-topic/invalid? ──→  polite redirect
    │ QUERY_NEEDED
    ▼
[LLM 2 — SQL Writer]   (focused prompt, full schema)
    │
    ▼
[SQLite — Query Executor]
    │
    ▼
[LLM 1 — Answer Formatter]  ──→  natural language answer + SQL shown to user
```

This means saying "Hi" gets a friendly response explaining what StatGenie can do, while "Who led the MLB in home runs in 2021?" triggers the SQL path — with the query displayed so users can verify the answer, just like Databricks Genie.

## 🚧 Roadblocks & Design Decisions

The goal of this project is to intentionally encounter and solve common NL2SQL problems:

- **The "Schema Gap":** How do I help an 8B model understand that `HR` means Home Runs? The solution was a hardcoded data dictionary in the SQL prompt — verbose but effective at preventing hallucinated column names.
- **Response Quality:** Early versions always ran SQL even for "Hi", producing robotic answers. The multi-LLM router fixed this by separating conversational intent from data retrieval.
- **Graceful Degradation:** What happens when a user asks about 1985 stats but the database only covers 2010–2024? The answer LLM is now primed with the data range and handles zero-result queries naturally.
- **Safety:** Direct SQL execution means a malicious prompt could theoretically run `DROP TABLE`. Added two guard layers: a jailbreak pattern check before any LLM call, and a SQL safety validator that rejects anything that isn't a `SELECT` against known tables.
- **Agnostic Architecture:** Designing the system so the logic stays the same even if the data changes. The schema is injected into the prompt — swapping databases is just a prompt edit.

## 📊 Data

Batting stats (2010–2024) are loaded from `batting.csv` into SQLite. Pitching and fielding data can be downloaded from the official MLB Stats API using the included scraper:

```bash
python3 scrape_data.py   # downloads pitching.csv and fielding.csv
python3 ingest_data.py   # loads all CSVs into the database
```

The scraper uses the official `statsapi.mlb.com` API — no third-party libraries, no fragile HTML scraping.

## 📁 File Reference

| File | Purpose |
|------|---------|
| `app.py` | Streamlit web interface. Renders the chat UI, passes messages to `agent.py`, and displays the natural language answer alongside the generated SQL in a collapsible expander. |
| `agent.py` | Core logic. Implements the multi-LLM router: classifies intent, generates SQL, executes it against SQLite, and formats the final answer. Also contains the jailbreak guard and SQL safety validator. |
| `scrape_data.py` | Downloads pitching and fielding stats from the official MLB Stats API (`statsapi.mlb.com`) for 2010–2024 and saves them as `pitching.csv` and `fielding.csv`. No third-party scraping libraries needed. |
| `ingest_data.py` | Loads `batting.csv`, `pitching.csv`, and `fielding.csv` into `mlb_batting_stats.db`. Re-run this whenever a CSV is added or updated. |
| `test_connection.py` | Quick sanity check to verify the local LLM server is running and reachable before launching the app. |
| `batting.csv` | Source batting data — one row per player-season, covering MLB 2010–2024. |
| `pitching.csv` | Source pitching data — generated by `scrape_data.py`. |
| `fielding.csv` | Source fielding data — generated by `scrape_data.py`. |
| `mlb_batting_stats.db` | SQLite database built from the CSV files by `ingest_data.py`. This is what the agent queries at runtime. |
| `requirements.txt` | Python package dependencies. Install with `pip install -r requirements.txt`. |

## 🗺️ Learning Roadmap
- [x] **NL2SQL pipeline** — convert natural language to SQL and execute it
- [x] **Streamlit interface** — chat UI with SQL shown in an expander
- [x] **Multi-LLM router** — separate routing, SQL generation, and answer formatting
- [x] **Full schema exposure** — all batting columns available (not just 4)
- [x] **Graceful degradation** — handles invalid years, unknown players, off-topic questions
- [x] **Safety layers** — jailbreak guard + SQL injection prevention
- [x] **Data scraper** — pitching and fielding data via MLB Stats API
- [ ] **Multi-table queries** — enable cross-table reasoning (batting + pitching + fielding)
- [ ] **Clarification loop** — flag ambiguous questions ("best player?") and ask the user to specify
- [ ] **Dynamic data dictionary** — let users teach the agent new terms without editing prompts
