# Twitter Data Engineering Pipeline

An end-to-end data engineering project that takes a raw Twitter dataset, cleans it, checks its quality, and produces a reliable final file, with every step automated and tested. It is built with **Python**, **Pandas**, and **Apache Airflow**.

 **[View Live Dashboard](https://twitter-data-pipeline-dashboard.vercel.app/)**

---

##  What This Project Does

Raw data is often messy: it has missing values, duplicate rows, and inconsistent column names. This project shows how a data engineer turns that raw data into clean, trustworthy data using an **ETL pipeline** (Extract → Transform → Load).

The original reference project used the Twitter API. This version uses a **public Twitter dataset (CSV)** instead, so anyone can run it without API keys or paid access.

##  How the Pipeline Works

```text
Public Dataset → Extract → Transform → Validate → Load → Refined CSV
```

1. **Extract:** Reads the raw tweets from `Data/tweets.csv` into a Pandas DataFrame.
2. **Transform:** Cleans and standardizes the data:
   - Removes the `latitude` and `longitude` columns because they were almost entirely empty
   - Renames columns to clearer names (see table below)
   - Converts the date field into a proper datetime format
   - Removes rows missing important fields (user, text, or created time)
   - Removes duplicate tweets so each tweet ID appears only once
3. **Validate:** Runs data quality checks before saving. If any check fails, the pipeline stops with an error instead of quietly producing bad data.
4. **Load:** Saves the final clean dataset to `output/refined_tweets.csv`.

### Column Renaming

| Original Column | New Column |
|---|---|
| author | user |
| content | text |
| number_of_likes | like_count |
| number_of_shares | share_count |
| date_time | created_at |

##  Data Quality Checks

Before the final file is written, the pipeline confirms that:

- All required columns exist
- The dataset is not empty
- Every tweet ID is unique
- `created_at` contains valid dates
- Important fields are filled in
- Required fields contain valid values

##  Results

| Metric | Result |
|---|---|
| Source records | 52,542 |
| Final clean records | 16,947 |
| Duplicate tweet IDs handled | 8,901 |
| Final columns | 8 |
| Unit tests | 4 passed |

##  Workflow Automation with Apache Airflow

Apache Airflow runs the pipeline as a DAG (a chain of tasks that run in order):

```text
extract_tweets → transform_tweets → validate_and_load
```

The DAG is in `dags/twitter_etl_dag.py`. It was tested locally on Windows using **WSL2 (Ubuntu)**, because Airflow works best in Unix-like environments. Airflow runs locally for development and demonstration and is not hosted on a cloud server.

## Testing

Automated unit tests cover the transformation and validation logic:

- Duplicate tweet ID removal
- Column renaming
- Successful data validation
- Detection of duplicate IDs during validation

Run them with:

```bash
python -m unittest discover tests
```
##  Dashboard

A lightweight static dashboard (HTML and CSS) is deployed on **Vercel**. It shows the record counts, pipeline status, architecture, data quality checks, and technologies used. It only presents the results of a verified pipeline run. It does not run the ETL or connect to Airflow.

##  Project Structure

```text
twitter-data-engineering-project/
├── dags/
│   └── twitter_etl_dag.py       # Airflow DAG
├── scripts/
│   └── twitter_etl.py           # ETL logic
├── tests/
│   └── test_twitter_etl.py      # Unit tests
├── dashboard/
│   ├── index.html
│   └── style.css
├── Data/
│   └── tweets.csv               # Source dataset (not on GitHub)
├── output/
│   ├── raw_tweets.csv           # Generated intermediate file (not on GitHub)
│   ├── transformed_tweets.csv   # Generated intermediate file (not on GitHub)
│   └── refined_tweets.csv       # Final output (not on GitHub)
├── .gitignore
├── requirements.txt
└── README.md
```

##  Technologies Used

| Tool | Purpose |
|---|---|
| Python | ETL implementation |
| Pandas | Data processing and cleaning |
| Apache Airflow | Workflow orchestration |
| WSL2 / Ubuntu | Local Airflow environment |
| Git & GitHub | Version control |
| HTML / CSS | Dashboard |
| Vercel | Dashboard deployment |

## How to Run

### 1. Clone the repository

```bash
git clone https://github.com/Jinatsultana/twitter-data-pipeline.git
cd twitter-data-pipeline
```

### 2. Create and activate a virtual environment (Windows PowerShell)

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Install Python dependencies

```bash
pip install pandas
```

### 4. Add the dataset

Place the dataset at `Data/tweets.csv`.

### 5. Run the pipeline

```bash
python scripts/twitter_etl.py
```

The refined dataset will be created at `output/refined_tweets.csv`.

##  Security and Reproducibility

- No Twitter API credentials are used
- Secrets, environment variables, and local config files are excluded from version control
- The dataset and generated CSV files are excluded via `.gitignore` to keep the repository lightweight

##  What I Learned

- Building an end-to-end ETL pipeline
- Cleaning and transforming data with Pandas
- Detecting and removing duplicates
- Adding data quality validation
- Writing reusable functions and unit tests
- Orchestrating workflows with Apache Airflow
- Working with WSL2 on Windows
- Using Git and GitHub
- Building and deploying a static dashboard with Vercel

##  Future Improvements

If extended into a production-grade system, this project could add:

- Cloud storage such as Amazon S3
- A relational or analytical database
- Incremental data loading
- More extensive data quality checks
- Monitoring and alerting
- A production Airflow environment
- CI/CD with GitHub Actions
- Distributed processing for larger datasets

These are listed as future work and are not part of the current implementation.
