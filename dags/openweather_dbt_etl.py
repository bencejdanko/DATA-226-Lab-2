from airflow import DAG
from airflow.operators.bash import BashOperator
\
from airflow.models import Variable

import datetime

DBT_PROJECT_DIR = "/opt/airflow/DATA-226-LAB-2"

account = Variable.get("SNOWFLAKE_ACCOUNT")
password = Variable.get("SNOWFLAKE_PASSWORD")
user = Variable.get("SNOWFLAKE_USER")


with DAG(
    "openweather_dbt_etl",
    start_date=datetime.datetime(2024, 11, 3),
    catchup=False,
    schedule_interval="@daily",

    default_args={
        "env": {
            "SNOWFLAKE_USER": user,
            "SNOWFLAKE_PASSWORD": password,
            "SNOWFLAKE_ACCOUNT": account,
            "SNOWFLAKE_DATABASE": "OPENWEATHER",
            "SNOWFLAKE_ROLE": "ACCOUNTADMIN",
            "SNOWFLAKE_WAREHOUSE": "compute_wh",
        }
    },

) as dag:
    dbt_run = BashOperator(
        task_id="dbt_run",
        bash_command=f"/home/airflow/.local/bin/dbt run --profiles-dir {DBT_PROJECT_DIR} --project-dir {DBT_PROJECT_DIR}",
    )

    dbt_test = BashOperator(
        task_id="dbt_test",
        bash_command=f"/home/airflow/.local/bin/dbt test --profiles-dir {DBT_PROJECT_DIR} --project-dir {DBT_PROJECT_DIR}",
    )

    dbt_snapshot = BashOperator(
        task_id="dbt_snapshot",
        bash_command=f"/home/airflow/.local/bin/dbt snapshot --profiles-dir {DBT_PROJECT_DIR} --project-dir {DBT_PROJECT_DIR}",
    )

    dbt_run >> dbt_test >> dbt_snapshot

