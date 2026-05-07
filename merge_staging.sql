
-- Merge new weekly data from staging into production table
-- Matches on primary key, updates existing records, inserts new ones
-- Note: table names, schemas, and column names have been anonymized.
-- Logic reflects actual merge pattern used in production.


-- 1 Download new weekly file into /raw directory
-- 2 Run py script to clean
-- 3 Import cleaned .csv into staging_schema.staging_table 
-- 4 Run below sql to merge new data from STG to PROD table

MERGE INTO production_schema.target_table t
USING staging_schema.staging_table s
    ON t.primary_key_column = s.primary_key_column

WHEN MATCHED THEN UPDATE SET
    t.column_1 = s.column_1,
    t.column_2 = s.column_2,
    t.updated_at = s.insert_date

WHEN NOT MATCHED THEN INSERT (
    primary_key_column,
    column_1,
    column_2,
    updated_at
)
VALUES (
    s.primary_key_column,
    s.column_1,
    s.column_2,
    s.insert_date
);