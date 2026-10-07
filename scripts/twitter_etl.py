from pathlib import Path
import logging

import pandas as pd


# --------------------------------------------------
# CONFIGURATION
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[1]

INPUT_FILE = PROJECT_ROOT / "Data" / "tweets.csv"
OUTPUT_FILE = PROJECT_ROOT / "output" / "refined_tweets.csv"


# --------------------------------------------------
# LOGGING
# --------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


# --------------------------------------------------
# EXTRACT
# --------------------------------------------------

def extract_data():
    logger.info("Starting data extraction...")

    if not INPUT_FILE.exists():
        raise FileNotFoundError(
            f"Input file not found: {INPUT_FILE}"
        )

    df = pd.read_csv(INPUT_FILE)

    logger.info(
        "Dataset loaded successfully. Rows: %s, Columns: %s",
        df.shape[0],
        df.shape[1]
    )

    return df


# --------------------------------------------------
# TRANSFORM
# --------------------------------------------------

def transform_data(df):
    logger.info("Starting data transformation...")

    # Remove columns that are almost completely empty
    df = df.drop(
        columns=["latitude", "longitude"],
        errors="ignore"
    )

    # Rename columns
    df = df.rename(
        columns={
            "author": "user",
            "content": "text",
            "number_of_likes": "like_count",
            "number_of_shares": "share_count",
            "date_time": "created_at"
        }
    )

    # Convert timestamp
    df["created_at"] = pd.to_datetime(
        df["created_at"],
        errors="coerce"
    )

    # Remove records missing important fields
    df = df.dropna(
        subset=["user", "text", "created_at"]
    )

    # Remove duplicate tweets using tweet ID
    df = df.drop_duplicates(
        subset=["id"]
    )

    logger.info(
        "Transformation completed. Rows: %s, Columns: %s",
        df.shape[0],
        df.shape[1]
    )

    return df

def validate_data(df):
    logger.info("Running data quality checks...")

    required_columns = [
        "user",
        "text",
        "country",
        "created_at",
        "id",
        "language",
        "like_count",
        "share_count"
    ]

    missing_columns = [
        column
        for column in required_columns
        if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {missing_columns}"
        )

    if df.empty:
        raise ValueError(
            "Data quality check failed: dataset is empty."
        )

    if df["id"].duplicated().any():
        raise ValueError(
            "Data quality check failed: duplicate tweet IDs found."
        )

    if df["created_at"].isna().any():
        raise ValueError(
            "Data quality check failed: invalid created_at values found."
        )

    logger.info("All data quality checks passed.")


# --------------------------------------------------
# LOAD
# --------------------------------------------------

def load_data(df):
    logger.info("Starting data loading...")

    OUTPUT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    df.to_csv(
        OUTPUT_FILE,
        index=False
    )

    logger.info(
        "Output successfully saved to: %s",
        OUTPUT_FILE
    )


# --------------------------------------------------
# MAIN ETL PIPELINE
# --------------------------------------------------

def main():

    logger.info("========== ETL PIPELINE STARTED ==========")

    df = extract_data()

    df = transform_data(df)

    validate_data(df)

    load_data(df)

    logger.info("========== ETL PIPELINE COMPLETED ==========")


if __name__ == "__main__":
    main()