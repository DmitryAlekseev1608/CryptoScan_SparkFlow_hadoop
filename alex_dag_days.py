import sys

sys.path.append("/opt/hadoop/airflow/dags/alex_crypto/")
import datetime as dt

from airflow import DAG
from airflow.operators.python_operator import PythonOperator

import compute.current
import compute.days

default_args = {"owner": "alex", "start_date": dt.datetime(2023, 12, 14)}

with DAG(
    "alex_crypt_days_result",
    default_args=default_args,
    dagrun_timeout=dt.timedelta(minutes=60),
    schedule_interval="@hourly",
) as dag:
    air_days = PythonOperator(task_id="all_price_in_prometheus", python_callable=compute.days.main)
