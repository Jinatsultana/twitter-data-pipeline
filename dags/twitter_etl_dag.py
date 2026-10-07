from datetime import datetime
from pathlib import Path
import sys

import pandas as pd

from airflow.sdk import dag
from airflow.providers.standard.operators.python import PythonOperator


# --------------------------------------------------
# PROJECT PATH
# --------------------------------------------------

PROJECT_ROOT = Path("/mnt/d/projects/twitter-data-engineering-project")

SCRIPTS_PATH = PROJECT_ROOT / "scripts"

sys.path.insert(0, str(SCRIPTS_PATH))

from twitter_etl import (
    extract_data,
    transform_data,
    validate_data,
    load_data,
)


# --------------------------------------------------
# AIRFLOW TASK FUNCTIONS
# --------------------------------------------------

def extract_task():
    df = extract_data()

    output_file = PROJECT_ROOT / "output" / "raw_tweets.csv"

    df.to_csv(output_file, index=False)

    print(f"Extracted data saved to: {output_file}")


def transform_task():
    input_file = PROJECT_ROOT / "output" / "raw_tweets.csv"
    output_file = PROJECT_ROOT / "output" / "transformed_tweets.csv"

    df = pd.read_csv(input_file)

    df = transform_data(df)

    df.to_csv(output_file, index=False)

    print(f"Transformed data saved to: {output_file}")


def validate_and_load_task():
    input_file = PROJECT_ROOT / "output" / "transformed_tweets.csv"

    df = pd.read_csv(input_file)

    validate_data(df)

    load_data(df)


# --------------------------------------------------
# AIRFLOW DAG
# --------------------------------------------------

@dag(
    dag_id="twitter_etl_pipeline",
    start_date=datetime(2026, 10, 7),
    schedule=None,
    catchup=False,
)
def twitter_etl_pipeline():

    extract = PythonOperator(
        task_id="extract_tweets",
        python_callable=extract_task,
    )

    transform = PythonOperator(
        task_id="transform_tweets",
        python_callable=transform_task,
    )

    validate_and_load = PythonOperator(
        task_id="validate_and_load",
        python_callable=validate_and_load_task,
    )

    extract >> transform >> validate_and_load


twitter_etl_pipeline()