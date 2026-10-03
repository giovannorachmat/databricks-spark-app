import json
import logging
import os
import urllib.request
from datetime import datetime
from zoneinfo import ZoneInfo

from databricks.sdk import WorkspaceClient
from pyspark.sql import Row, SparkSession

logger = logging.getLogger()

# databricks config
w = WorkspaceClient(
    host=os.environ.get("DATABRICKS_HOST"),
    account_id=os.environ.get("DATABRICKS_ACCOUNT_ID"),
    token=os.environ.get("DATABRICKS_TOKEN"),
)

CATALOG = "giografi-dev"
SCHEMA = "default"
TABLE = "weatherstack_spark"
WAREHOUSE_ID = os.environ.get("DATABRICKS_WAREHOUSE_ID")

# initiate spark session
spark = SparkSession.builder.getOrCreate()

# weatherstack config
API_KEY = os.environ["API_KEY"]
BASE_URL_API = "https://api.weatherstack.com/current"
CITY = "Jakarta"

# set ingestion datetime
TODAY = datetime.now(ZoneInfo("Asia/Jakarta")).isoformat(timespec="seconds")

# build API url
url = f"{BASE_URL_API}?access_key={API_KEY}&query={CITY}&units=m"
# hit API url
logger.info("hitting Weatherstack API...")
with urllib.request.urlopen(url) as r:
    print(f"Return code: {r.status}")
    weather_data = json.dumps(json.loads(r.read()), indent=4)

# create df
df = spark.createDataFrame([Row(ingestion_date=TODAY, json_output=weather_data)])
# save df output to databricks table
tbl = df.write.mode("error").saveAsTable(f"{CATALOG}.{SCHEMA}.{TABLE}")
