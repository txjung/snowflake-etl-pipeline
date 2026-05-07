# Snowflake ETL Pipeline
Self-serve ETL pipeline to load and merge weekly CSV data into Snowflake — built to unblock a work-stoppage data gap

## Problem
Our data engineering team had a significant backlog of requests, and a critical data gap was becoming a work-stoppage issue for the analytics team. Rather than wait indefinitely for EDW capacity, I designed and built a self-serve weekly ETL pipeline to bridge the gap and unblock analysis.

## What It Does
An end-to-end Python pipeline that prepares and loads weekly CSV data for Snowflake ingestion:

- Detects the latest raw CSV file in a designated input folder
- Validates and reconciles row counts before and after processing
- Cleans and standardizes headers to match the Snowflake destination schema
- Adds an insert timestamp column for load tracking
- Implements retry logic for resilience
- Saves the cleaned file to a separate output folder
- Archives the original raw file
- Logs each run with status and row counts to a txt file

## Stack
- Python (pandas, os, logging)
- Snowflake (staging table design + SQL merge logic)
- SQL (see `merge_staging.sql` for full transformation logic)

## Setup
1. Clone this repo
2. Copy `.env.example` to `.env` and fill in your credentials
3. Install dependencies: `pip install -r requirements.txt`
4. Update the folder path variables in the script to match your local directory
5. Run: `python etl_pipeline.py`

## What I'd Do Next
The current implementation handles all CSV preparation locally. The logical next step is integrating `snowflake-connector-python` to execute the staging load and merge logic directly within the script — completing the pipeline in a single automated run. A separate `merge_staging.sql` is included to show the full transformation logic.