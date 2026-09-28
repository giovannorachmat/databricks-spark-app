import os
import json
import urllib.request
from datetime import datetime
from zoneinfo import ZoneInfo
from pyspark.sql import SparkSession, Row

spark = SparkSession.builder.getOrCreate()

API_KEY = os.environ["API_KEY"]
BASE_URL_API = "https://api.weatherstack.com/current"
CITY = "Jakarta"
TODAY = datetime.now(ZoneInfo("Asia/Jakarta")).isoformat(timespec="seconds")

url = f"{BASE_URL_API}?access_key={API_KEY}&query={CITY}&units=m"
with urllib.request.urlopen(url) as r:
    weather_data = json.dumps(json.loads(r.read()), indent=4)

df = spark.createDataFrame([Row(date=TODAY, weatherstack_output=weather_data)])
df.show(truncate=False)
