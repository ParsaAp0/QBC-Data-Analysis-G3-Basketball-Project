# Quera Data Analysis Bootcamp – Project 1 - Group 3 | NBA Data Analytics

This repository contains the code, documentation, and analyses for the first project of the Quera Data Analysis Bootcamp. The main objectives are to scrape basketball data from `basketball-reference.com`, store it in a relational database, and perform statistical analyses to answer specific questions and test given hypotheses.

The project is divided into three main phases:
1.  **Web Scraping** (Data Extraction)
2.  **Database Design & Storage**
3.  **Statistical Analysis** (Descriptive stats & Hypothesis Testing)

---

## 📁 Folder & File Structure
(just a guess)
```text
QBC-Data-Analysis-G3-Basketball-Project/
│
├── README.md                         # This file – project overview and guide
├── .gitignore                        # List of files/folders ignored by Git
├── requirements.txt                  # Required Python libraries
├── environment.yml                   # (Optional) Conda environment file
│
├── docs/                             # Project documentation
│   ├── database_design.md            # Database design, ER diagram, tables, and relationships
│   ├── statistical_plan.md           # Hypotheses, custom metrics, and chosen statistical tests
│   └── presentation/                 # Final presentation files (slides, posters, data story)
│
├── src/                              # Main source code (all Python code)
│   ├── __init__.py
│   │
│   ├── scraping/                     # Phase 1: Web scraping
│   │   ├── __init__.py
│   │   ├── config.py                 # Scraping settings (base URLs, headers, timeouts)
│   │   ├── scraper.py                # Core HTML fetching logic (requests, response handling)
│   │   ├── parsers.py                # HTML parsers (extract players, teams, games data)
│   │   └── data_cleaner.py           # Initial cleaning (data type conversion, handling missing values)
│   │
│   ├── database/                     # Phase 2: Database design, connection, and storage
│   │   ├── __init__.py
│   │   ├── models.py                 # SQLAlchemy ORM models (Player, Team, League, Game)
│   │   ├── db_connection.py          # Create engine and session management
│   │   ├── init_db.py                # Script to create all tables (CREATE TABLES)
│   │   ├── insert_data.py            # Load scraped data into the database
│   │   └── queries.py                # Predefined SQL queries for analysis (e.g., top 50 players per season)
│   │
│   ├── analysis/                     # Phase 3: Statistical analysis & visualization
│   │   ├── __init__.py
│   │   ├── descriptive_stats.py      # Compute descriptive stats (distributions, means, medians, boxplots)
│   │   ├── hypothesis_tests.py       # Implement hypothesis tests (t-tests, ANOVA, etc.) for the two hypotheses
│   │   ├── metrics.py                # Custom metric definitions (e.g., agility = height/weight, innate ability = experience/age)
│   │   ├── visualizations.py         # Plotting functions (histograms, boxplots, scatter plots)
│   │   └── report_generator.py       # Generate final summary tables and save figures
│   │
│   └── utils/                        # Shared utility tools
│       ├── __init__.py
│       ├── logger.py                 # Logging configuration (save errors and events)
│       └── helpers.py                # General helper functions (file I/O, date formatting, etc.)
│
├── data/                             # Raw and processed data (this folder is gitignored)
│   ├── raw/                          # Raw scraped data (JSON/CSV) before DB insertion
│   └── processed/                    # Final output data for analysis (exported CSVs)
│
├── tests/                            # Automated tests (optional but recommended)
│   ├── test_scraper.py               # Tests for scraping functions
│   ├── test_models.py                # Tests for database models and relationships
│   └── test_analysis.py              # Tests for statistical calculations and metrics
│
├── scripts/                          # One-off or helper scripts
│   ├── reset_database.py             # Reset the database (drop and recreate all tables)
│   └── export_for_analysis.py        # Export data from DB to CSV for notebook analysis
│
└── notebooks/                        # Jupyter notebooks for exploration and presentation
    ├── 01_exploratory_analysis.ipynb # Initial data exploration
    ├── 02_descriptive_stats.ipynb    # Descriptive statistics and required plots
    └── 03_hypothesis_testing.ipynb   # Hypothesis testing and result interpretation
```

---

## 🧩 Detailed Description of Each File and Folder

### **Root Files**

| File | Description |
| :--- | :--- |
| **`README.md`** | This file. Contains the overall description, structure, and setup guide for the project. |
| **`.gitignore`** | Files that should not be committed (e.g., `__pycache__/`, `.env`, `data/`, `*.db`). **Must be created before the first commit.** |
| **`requirements.txt`** | Lists all Python libraries with exact versions. Install them all at once using `pip install -r requirements.txt`. |
| **`environment.yml`** | (Optional) If you are using Conda, this file replaces `requirements.txt`. |

---

### **`docs/` Folder (Documentation)**

All textual documentation and team decisions are stored here. This section is crucial for the final presentation.

| File/Folder | Description |
| :--- | :--- |
| **`database_design.md`** | Contains the ER diagram, normalized tables, explanations of relationships (primary/foreign keys), and the reasoning behind the chosen structure. |
| **`statistical_plan.md`** | Defines the custom metrics (agility, innate ability), formulates null and alternative hypotheses, and justifies the selected statistical tests for each hypothesis. |
| **`presentation/`** | Stores the final presentation files (PowerPoint, PDF, or data storytelling documents). |

---

### **`src/` Folder (Main Source Code)**

This folder contains all executable code, organized according to the project's three phases.

#### **`src/scraping/` (Phase 1 – Web Scraping)**
| File | Description |
| :--- | :--- |
| **`config.py`** | Defines constants like `BASE_URL`, `USER_AGENT`, and delays between requests to respect the website's terms of service. |
| **`scraper.py`** | Contains the core `fetch_page(url)` function to retrieve HTML content and handle network errors. |
| **`parsers.py`** | Includes parsing functions (e.g., `parse_player_row(row)`) that transform raw HTML into structured Python dictionaries. |
| **`data_cleaner.py`** | Provides functions for standardizing strings (e.g., converting height from "6-6" to centimeters) and handling missing or null values. |

#### **`src/database/` (Phase 2 – Database & Storage)**
| File | Description |
| :--- | :--- |
| **`models.py`** | Defines SQLAlchemy classes (e.g., `class Player(Base):`). All entities (Player, Team, League, Game) and their relationships are defined here. |
| **`db_connection.py`** | Creates the database engine (for SQLite, PostgreSQL, etc.) and manages session lifecycles. |
| **`init_db.py`** | Running this script creates all tables in the database based on the defined models (`Base.metadata.create_all(engine)`). |
| **`insert_data.py`** | Takes the scraped data, converts it into ORM objects, and saves them into the database using sessions. |
| **`queries.py`** | Contains reusable parameterized queries (e.g., `get_top_scorers(season, limit)`) to fetch data for the analysis phase. |

#### **`src/analysis/` (Phase 3 – Statistical Analysis)**
| File | Description |
| :--- | :--- |
| **`descriptive_stats.py`** | Computes descriptive statistics (distributions, means, medians, boxplots) for the requested features (height, experience). |
| **`hypothesis_tests.py`** | Implements the statistical tests (t-tests, Mann-Whitney U, etc.) for the two given hypotheses. |
| **`metrics.py`** | Centralizes the custom metric logic (e.g., agility = height/weight, innate ability = experience/age) to ensure consistency. |
| **`visualizations.py`** | Contains plotting functions (histograms, boxplots, scatter plots) using libraries like Matplotlib or Seaborn. |
| **`report_generator.py`** | Aggregates results, creates summary tables, and saves figures to the `data/processed/` folder or `docs/presentation/`. |

#### **`src/utils/` (Shared Utilities)**
| File | Description |
| :--- | :--- |
| **`logger.py`** | Configures logging to record errors, warnings, and key events during execution. |
| **`helpers.py`** | Contains generic helper functions, such as file saving/loading, date formatting, and path management. |

---

### **Other Folders**

| Folder | Description |
| :--- | :--- |
| **`data/`** | **Ignored by Git.** Used to store scraped raw data and processed output files. Keeps the repository lightweight. |
| **`tests/`** | (Optional) Contains unit tests to validate the logic of scraping, models, and analysis functions. Recommended for robust code. |
| **`scripts/`** | Contains utility scripts. For example, `reset_database.py` drops and recreates all tables, and `export_for_analysis.py` exports data to CSV for use in notebooks. |
| **`notebooks/`** | Jupyter notebooks for interactive exploration, prototyping, and creating the final data story. Keep them well-documented and sequential. |

---

## 🚀 Getting Started (Cloning the Repository)

### For Collaborators (with write access)

If you have been added as a collaborator to this repository, you can clone it using either SSH or HTTPS:

**Option 1: SSH (recommended if you've set up SSH keys)**
```bash
git clone git@github.com:owner-username/basketball-analytics-project.git
cd basketball-analytics-project
```

**Option 2: HTTPS (works without SSH setup)**
```bash
git clone https://github.com/owner-username/basketball-analytics-project.git
cd basketball-analytics-project
```

> **Note:** Replace `owner-username` with the actual GitHub username or organization name that owns the repository.

---

### For Read-Only Access (viewers, non-collaborators)

If you only need to view or download the code (without pushing changes), use:

```bash
git clone https://github.com/owner-username/basketball-analytics-project.git
cd basketball-analytics-project
```
