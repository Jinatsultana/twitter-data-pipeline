# Twitter Data Engineering Pipeline

An end-to-end **Data Engineering project** that extracts a raw Twitter dataset, transforms and cleans the data with **Python and Pandas**, validates data quality, and produces a refined dataset.

The ETL workflow is orchestrated locally using **Apache Airflow**, with automated unit tests covering the transformation and validation logic.

**[View Live Dashboard](https://twitter-data-pipeline-dashboard.vercel.app/)**

---

## Project Overview

Raw datasets often contain missing values, duplicate records, inconsistent column names, and invalid timestamps.

This project demonstrates how an ETL pipeline can transform raw data into a cleaner and more reliable dataset.

```text
Raw Twitter Dataset
        ↓
     Extract
        ↓
    Transform
        ↓
     Validate
        ↓
       Load
        ↓
 Refined CSV Dataset
        ↓
 Interactive Dashboard
```

The original reference implementation used the Twitter API. This implementation uses a public Twitter dataset in CSV format so the project can be reproduced without Twitter API credentials or paid API access.

---

## What the Pipeline Does

### 1. Extract

The pipeline reads the raw dataset from:

```text
Data/tweets.csv
```

The dataset is loaded into a Pandas DataFrame for processing.

### 2. Transform

The transformation stage cleans and standardizes the dataset.

The pipeline:

- Removes the latitude and longitude columns
- Renames columns to clearer names
- Converts the timestamp field into a proper datetime format
- Removes records missing critical fields
- Removes duplicate tweet IDs

#### Column Renaming

| Original Column | Refined Column |
|---|---|
| author | user |
| content | text |
| number_of_likes | like_count |
| number_of_shares | share_count |
| date_time | created_at |

### 3. Validate

Before the refined dataset is written, the pipeline performs data-quality checks.

It verifies that:

- All required columns exist
- The dataset is not empty
- Tweet IDs are unique
- `created_at` contains valid datetime values
- Required fields are present

If a validation check fails, the pipeline raises an error instead of silently producing invalid output.

### 4. Load

After successful validation, the refined dataset is written to:

```text
output/refined_tweets.csv
```

---

## Results

The current pipeline produces the following results:

| Metric | Result |
|---|---|
| Source records | 52,542 |
| Final clean records | 16,947 |
| Duplicate tweet IDs handled | 8,901 |
| Final columns | 8 |
| Unit tests | 4 passed |

These results represent the current dataset and pipeline run used for the project dashboard.

---

## Apache Airflow Workflow

Apache Airflow is used to orchestrate the ETL workflow as a DAG.

The workflow follows:

```text
extract_tweets
      ↓
transform_tweets
      ↓
validate_and_load
```

The DAG is located at:

```text
dags/twitter_etl_dag.py
```

Airflow was tested locally using WSL2 with Ubuntu on Windows because Airflow is better suited to a Unix-like development environment.

The Airflow environment is used for local development and demonstration. It is not deployed to a cloud server.

---

## Testing

The project includes automated unit tests for the ETL transformation and validation logic.

The tests cover:

- Duplicate tweet ID removal
- Column renaming
- Successful data validation
- Detection of duplicate IDs during validation

Run the tests with:

```bash
python -m unittest discover tests
```

Expected result:

```text
Ran 4 tests
OK
```

---

## Interactive Dashboard

A lightweight interactive dashboard is deployed on Vercel.

**[View Live Dashboard](https://twitter-data-pipeline-dashboard.vercel.app/)**

The dashboard provides:

- Source record count
- Final clean record count
- Duplicate ID count
- Pipeline status
- Interactive user filtering
- Tweet count for the selected user
- Like count for the selected user
- Share count for the selected user
- ETL pipeline architecture
- Data-quality checks
- Technology stack
- Project overview

The dashboard reads the refined dataset and presents the results of a verified pipeline run.

It does not execute the ETL pipeline or connect directly to Apache Airflow.

---

## Project Structure

```text
twitter-data-pipeline/
│
├── dags/
│   └── twitter_etl_dag.py
│
├── scripts/
│   └── twitter_etl.py
│
├── tests/
│   └── test_twitter_etl.py
│
├── dashboard/
│   ├── index.html
│   ├── script.js
│   ├── style.css
│   └── data/
│       └── refined_tweets.csv
│
├── .gitignore
├── requirements.txt
└── README.md
```

---

## Technologies Used

| Technology | Purpose |
|---|---|
| Python | ETL implementation |
| Pandas | Data processing and transformation |
| Apache Airflow | Workflow orchestration |
| WSL2 / Ubuntu | Local Airflow environment |
| HTML / CSS / JavaScript | Interactive dashboard |
| Git | Version control |
| GitHub | Source code hosting |
| Vercel | Dashboard deployment |

---

## How to Run

### 1. Clone the Repository

```bash
git clone https://github.com/Jinatsultana/twitter-data-pipeline.git
cd twitter-data-pipeline
```

### 2. Create a Virtual Environment

For Windows PowerShell:

```powershell
python -m venv .venv
```

Activate the environment:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 3. Install Dependencies

Install the project's Python dependencies:

```bash
pip install -r requirements.txt
```

### 4. Add the Dataset

Place the raw dataset at:

```text
Data/tweets.csv
```

### 5. Run the ETL Pipeline

Run the standalone ETL script:

```bash
python scripts/twitter_etl.py
```

The refined dataset will be generated at:

```text
output/refined_tweets.csv
```

---

## Running the Dashboard Locally

The dashboard is a static frontend and does not require a backend server.

From the project root, run:

```bash
python -m http.server 8000 -d dashboard
```

Then open:

```text
http://localhost:8000
```

The dashboard loads the refined dataset from:

```text
dashboard/data/refined_tweets.csv
```

The production version is deployed on Vercel.

---

## Reproducibility and Security

This project is designed to remain lightweight and reproducible without paid external services.

- No Twitter API credentials are required
- No paid Twitter API access is used
- No continuously running cloud server is required
- The ETL pipeline can run locally
- Apache Airflow is used locally for workflow orchestration
- The dashboard is deployed separately as a static frontend
- Local configuration files and sensitive information are excluded through `.gitignore`
- The project does not require a cloud database

---

## Key Data Engineering Concepts Demonstrated

This project demonstrates practical experience with:

- ETL pipeline development
- Data extraction from CSV
- Data cleaning and transformation
- Schema standardization
- Duplicate detection and removal
- Data-quality validation
- Exception handling
- Unit testing
- Workflow orchestration with Apache Airflow
- Local development with WSL2
- Git and GitHub
- Static frontend deployment
- Interactive data visualization and filtering

---

## What I Learned

Through this project, I gained hands-on experience with:

- Building an end-to-end ETL workflow
- Processing datasets using Pandas
- Designing reusable ETL functions
- Handling missing and duplicate data
- Implementing data-quality validation
- Writing unit tests
- Orchestrating workflows using Apache Airflow
- Working with WSL2 and Ubuntu on Windows
- Managing code with Git and GitHub
- Building an interactive dashboard for processed data
- Deploying a static dashboard using Vercel

---

## Future Improvements

The current project is intentionally designed as a local, zero-cost implementation.

Possible future extensions include:

- Cloud object storage such as Amazon S3
- A relational or analytical database
- Incremental data loading
- More extensive data-quality rules
- Pipeline monitoring and alerting
- Production Airflow deployment
- CI/CD with GitHub Actions
- Distributed processing for larger datasets

These are future improvements only and are not part of the current implementation.
