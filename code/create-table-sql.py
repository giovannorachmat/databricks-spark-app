import os
import time

from databricks.sdk import WorkspaceClient
from databricks.sdk.service.sql import StatementState

w = WorkspaceClient(
    host=os.environ.get("DATABRICKS_HOST"),
    account_id=os.environ.get("DATABRICKS_ACCOUNT_ID"),
    token=os.environ.get("DATABRICKS_TOKEN"),
)

CATALOG = "giografi-dev"
SCHEMA = "default"
TABLE = "weatherstack"
WAREHOUSE_ID = os.environ.get("DATABRICKS_WAREHOUSE_ID")


def run_sql(statement: str, warehouse_id: str = None) -> None:
    resp = w.statement_execution.execute_statement(
        warehouse_id=warehouse_id,
        statement=statement,
        wait_timeout="0s",
    )
    statement_id = resp.statement_id

    while True:
        resp = w.statement_execution.get_statement(statement_id)
        state = resp.status.state
        if state == StatementState.SUCCEEDED:
            return resp
        if state in (
            StatementState.FAILED,
            StatementState.CANCELED,
            StatementState.CLOSED,
        ):
            raise RuntimeError(f"Statement failed: {resp.status.error}")
        time.sleep(2)


# 1. ensure schema exists
run_sql(f"CREATE SCHEMA IF NOT EXISTS `{CATALOG}`.`{SCHEMA}`")

# 2. create table
run_sql(
    f"""
    CREATE TABLE IF NOT EXISTS `{CATALOG}`.`{SCHEMA}`.`{TABLE}` (
        id BIGINT,
        name STRING,
        created_at TIMESTAMP
    )
""",
    warehouse_id=WAREHOUSE_ID,
)

print(f"Table ready: `{CATALOG}`.`{SCHEMA}`.`{TABLE}`")
