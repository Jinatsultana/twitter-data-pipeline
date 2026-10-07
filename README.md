# Twitter Data Engineering Pipeline

An end-to-end data engineering project that extracts, transforms, validates, and loads Twitter dataset records using Python, Pandas, and Apache Airflow.

## Project Overview

This project demonstrates a local ETL pipeline built around a publicly available Twitter dataset.

The original reference architecture used the Twitter API. This implementation uses a static dataset so that the pipeline is reproducible and does not depend on external API access.

The pipeline performs:

- Data extraction from CSV
- Data transformation and cleaning
- Duplicate tweet ID handling
- Data quality validation
- CSV output generation
- Workflow orchestration using Apache Airflow
- Automated unit testing

## Architecture

```text
tweets.csv
    |
    v
Extract
    |
    v
Transform
    |
    v
Data Quality Validation
    |
    v
Load
    |
    v
refined_tweets.csv