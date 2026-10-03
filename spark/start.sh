source "$(dirname "$0")/.env"
exec docker compose exec spark-master /opt/spark/bin/spark-submit \
  --master "spark://spark-master:${SPARK_MASTER_PORT}" \
  --driver-memory "${SPARK_SUBMIT_MEMORY}" \
  --executor-memory "${SPARK_SUBMIT_MEMORY}" \
  "/app/$1"
