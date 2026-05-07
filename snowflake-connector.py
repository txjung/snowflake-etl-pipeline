# Skeleton script showing planned Snowflake connector integration
# Would be incorporated into etl_pipeline.py to complete the pipeline
# See README for context

import snowflake.connector
import os\
\
conn = snowflake.connector.connect(\
    account=os.environ.get("SNOWFLAKE_ACCOUNT"),\
    user=os.environ.get("SNOWFLAKE_USER"),\
    password=os.environ.get("SNOWFLAKE_PASSWORD"),\
    database=os.environ.get("SNOWFLAKE_DATABASE"),\
    schema=os.environ.get("SNOWFLAKE_SCHEMA"),\
    warehouse=os.environ.get("SNOWFLAKE_WAREHOUSE")\
)\
\
cursor = conn.cursor()\
cursor.execute("merge_staging.sql")\
conn.close()}