# Next steps after this: connect to Snowflake via snowflake-connector
# and execute merge_staging.sql to complete the pipeline
# See merge_staging.sql for full transformation logic and README.md for context

import pandas as pd
import re
import os
import shutil
import time
from datetime import datetime

# Folders
RAW_FOLDER = "data/raw/"
CLEAN_FOLDER = "data/cleaned/"
ARCHIVE_FOLDER = "data/archive/"
LOG_FILE = "data/run_log.csv"

# Ensure folders exist
os.makedirs(CLEAN_FOLDER, exist_ok=True)
os.makedirs(ARCHIVE_FOLDER, exist_ok=True)

# Retry helper
def retry(operation, attempts=3, delay=3):
    for i in range(attempts):
        try:
            return operation()
        except Exception as e:
            if i == attempts - 1:
                raise
            print(f"Retrying after error: {e}")
            time.sleep(delay)

# Step 1: Find newest raw file (with retry)
def get_newest_file():
    raw_files = [f for f in os.listdir(RAW_FOLDER) if f.lower().endswith(".csv")]
    if not raw_files:
        raise FileNotFoundError("No CSV files found in the raw folder.")
    return max(
        [os.path.join(RAW_FOLDER, f) for f in raw_files],
        key=os.path.getmtime
    )

newest_file = retry(get_newest_file, attempts=5, delay=5)
print(f"Loading newest file: {newest_file}")

# Step 2: Count raw rows (excluding header)
raw_row_count = sum(1 for _ in open(newest_file, encoding="utf-8")) - 1

# Step 3: Load CSV with retry
df = retry(lambda: pd.read_csv(newest_file, dtype=str), attempts=3, delay=2)

# Cleaning function
def clean_col(col):
    col = col.upper()
    col = col.strip()
    col = re.sub(r'[^A-Z0-9]+', '_', col)
    col = re.sub(r'_+', '_', col)
    col = col.strip('_')
    return col

# Step 4: Clean headers
df.columns = [clean_col(c) for c in df.columns]

# Step 5: Add insert date column and force it to be last
df["INSERT_DATE"] = datetime.now().strftime("%Y-%m-%d")
cols = list(df.columns)
cols.remove("INSERT_DATE")
cols.append("INSERT_DATE")
df = df[cols]

# Step 6: Validate row counts
cleaned_row_count = len(df)

if raw_row_count != cleaned_row_count:
    print("ERROR: Row count mismatch detected!")
    print(f"Raw rows: {raw_row_count}, Cleaned rows: {cleaned_row_count}")
    print("Aborting pipeline. Raw file will NOT be archived or processed.")
    raise SystemExit("Pipeline stopped due to row count mismatch.")

# Step 7: Save cleaned file
timestamp = datetime.now().strftime("%Y-%m-%d_%H%M")
output_file = os.path.join(CLEAN_FOLDER, f"cleaned_{timestamp}.csv")

retry(lambda: df.to_csv(output_file, index=False), attempts=3, delay=2)
print(f"Cleaned file saved as: {output_file}")

# Step 8: Archive raw file
archive_name = f"raw_{timestamp}.csv"
archive_path = os.path.join(ARCHIVE_FOLDER, archive_name)

retry(lambda: shutil.move(newest_file, archive_path), attempts=3, delay=2)
print(f"Archived raw file to: {archive_path}")

# Step 9: Log the run
log_entry = {
    "run_timestamp": timestamp,
    "raw_file": os.path.basename(newest_file),
    "archived_file": archive_name,
    "cleaned_file": os.path.basename(output_file),
    "raw_row_count": raw_row_count,
    "cleaned_row_count": cleaned_row_count,
    "row_count_match": True
}

def append_log():
    if not os.path.exists(LOG_FILE):
        pd.DataFrame([log_entry]).to_csv(LOG_FILE, index=False)
    else:
        pd.DataFrame([log_entry]).to_csv(LOG_FILE, mode='a', header=False, index=False)

retry(append_log, attempts=3, delay=2)
print(f"Run logged to: {LOG_FILE}")


