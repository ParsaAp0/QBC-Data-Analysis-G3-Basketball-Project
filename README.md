# Quera Data Analysis Bootcamp – Project 1 - Group 3 | NBA Data Analytics

Repository for the group project of the Quera Data Analysis Bootcamp. We scrape basketball-reference.com, store the data in a relational database (MySQL), and run the required statistical analyses.

---

## Team Members

- **Sajjad Moghayad**
- **Arash Tahamtan**
- **Morteza Eshghi**
- **Parsa Adlparvar**
- **Amirreza Abbasi**

---

## Directory Layout


```text
QBC-Data-Analysis-G3-Basketball-Project/
│
├── README.md                         # Project overview and guide
├── .gitignore                        # Files/folders ignored by Git
├── .gitattributes                    # Git attributes
├── Git_Help.txt                      # Useful Git commands
├── Project-Description.pdf           # Project description (PDF)
├── NBA_Statistical_Report.pdf        # Project Final Report (PDF)
├── python-requirements.txt           # Python dependencies
│
├── data/
│   ├── CSVs/                         # CSV format data
│   └── URLs/                         # URL lists for scraping
│
├── src/                              # Main source code
│   ├── Database_v2/                  # Current database implementation (Phase 2)
│   |   ├── create_database.sql       # Create the database schema
│   |   ├── create_tables.sql         # Create all tables
│   |   ├── indexes.sql               # Index definitions
│   |   └── Data_Load/                # ETL scripts to load CSV data into DB
│   |   |   ├── config.py             # Configuration (DB connection, paths)
│   |   |   ├── database.py           # Database connection utilities
│   |   |   ├── utils.py              # Helper functions for data cleaning
│   |   |   ├── main.py               # Main orchestration script
│   |   |   └── loaders/              # Individual loaders per entity
│   │
│   ├── scraping/                     # Phase 1: Web scraping (Jupyter notebooks)
│   │
│   ├── analysis/                     # Phase 3: Statistical analysis (SQL queries)
│   │   ├── Queries/                  # Almost all SQL queries
│   │   │   ├── Additional_Queries/   # Extra queries beyond the main tasks
│   │   │   │   ├── Questions/        # Ad‑hoc analytical questions (Q1‑Q4)
│   │   │   │   └── Tasks/            # Extra tasks (numbered extra*.sql)
│   │   │   ├── Hypotheses/           # Hypotheses queries
│   │   │   └── Tasks/                # Tasks
│   │   └── Python Codes/             # Python codes for analysis (and few queries)
│   │
│   ├── database_v1/                  # Legacy/earlier database implementation
│   |   ├── models.py                 # SQLAlchemy ORM models
│   |   ├── db_connection.py          # Database engine and session
│   |   ├── insert_data.py            # Load data into DB (old version)
│   |   ├── basketball_reference.db   # SQLite database file (v1)
│   |   └── Diagram.drawio            # ER diagram (Draw.io source)
```
---

## Components

### 1. Data (`data/`)

This folder contains all the data used in the project, split into two subfolders:

- **`CSVs/`** – Contains the final cleaned data in CSV format. These files are the output of the scraping notebooks and the input for the ETL pipeline:
  - `players_data.csv` – Player biographical information (name, height, weight, birthdate, etc.)
  - `teams_data.csv` – Team metadata (franchise, conference, division, etc.)
  - `awards.csv` – Award names and descriptions
  - `player_season_data.csv` – Per-season player statistics (points, rebounds, assists, etc.)
  - `team_season_data.csv` – Per-season team statistics
  - `award_season_data.csv` – Awards won by players per season

- **`URLs/`** – Contains text files with URL lists used during the scraping process. These act as a crawl index for the notebooks to systematically navigate the website.

---

### 2. Web Scraping (`src/scraping/`)

Six Jupyter notebooks handle the extraction process. They run in a specific order:

1. **`find_players_and_teams_url.ipynb`** – First step. Collects all player and team page URLs and saves them to `data/URLs/`.
2. **`find_players_info.ipynb`** – Uses the player URLs to scrape biographical data (height, weight, birth year, college, etc.).
3. **`find_team_info.ipynb`** – Uses team URLs to scrape franchise metadata.
4. **`find_player_season_info.ipynb`** – Scrapes season-by-season stats for every player.
5. **`find_team_season_info.ipynb`** – Scrapes season-by-season stats for every team.
6. **`find_awards_info.ipynb`** – Scrapes award/achievement data.

All scraping configurations (headers, delays, timeout settings) are stored in `config.json`.

---

### 3. Database (`src/Database_v2/`)

This is the current database implementation, using **MySQL** as the relational database management system. It consists of:

- **Schema definition files** (`.sql`):
  - `create_database.sql` – Creates the database (e.g., `CREATE DATABASE IF NOT EXISTS nba_data;`).
  - `create_tables.sql` – Defines all tables and their relationships (primary keys, foreign keys, data types).
  - `indexes.sql` – Creates indexes for performance optimization on frequently queried columns.

- **ETL Pipeline** (`Data_Load/`):
  - `main.py` – Orchestrates the entire loading process. Run this script to populate the database.
  - `config.py` – Stores MySQL connection parameters (host, user, password, database name) and file paths.
  - `database.py` – Utilities for connecting to MySQL and managing transactions using `mysql-connector-python` or `PyMySQL`.
  - `utils.py` – Helper functions for data cleaning, type conversion, and validation.
  - `loaders/` – One Python module per entity. Each loader reads its corresponding CSV file, processes the data, and inserts it into the database.
  - `lookups.py` – Helper functions that map names to IDs (e.g., finding a player's ID by name) to maintain referential integrity.

---

### 4. Analysis (`src/analysis/Queries/`)

This folder contains all SQL queries used for analysis. They are organized into three subfolders:

- **`Tasks/`** – The five project tasks (`task1.sql` – `task5.sql`).

- **`Additional_Queries/Questions/`** – Contains four ad-hoc analytical questions (Q1-Q4) that explore the data beyond the main requirements.

- **`Additional_Queries/Tasks/`** – Extra numbered tasks (`extra*.sql`). These are likely additional exercises or challenge questions that go beyond the core project.

- **`Hypotheses/`** – Reserved for queries specifically related to hypothesis testing. This would contain the SQL needed to extract data for statistical tests.

- **`Python Codes/`** – Conducting hypothesis tests and creating graphs and charts.

The queries can be run directly against the populated MySQL database using any SQL client or from the command line.

---

### 5. Legacy Code (`src/database_v1/`)

This is an older version of the database implementation kept for reference. It uses SQLAlchemy ORM instead of raw SQL and has a different loading approach. Key files:

- `models.py` – SQLAlchemy ORM classes defining the database schema.
- `db_connection.py` – Manages the SQLite engine and sessions.
- `insert_data.py` – The original data loading script (now replaced by the `Database_v2` ETL pipeline).
- `basketball_reference.db` – The SQLite database file generated by v1.
- `Diagram.drawio` – An Entity-Relationship diagram (editable with draw.io) showing the database structure.

**Note:** `database_v1` is not used in the current workflow. All new work should target `Database_v2/`.

---