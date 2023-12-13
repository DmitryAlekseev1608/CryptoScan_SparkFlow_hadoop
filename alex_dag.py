import sys

sys.path.append("/opt/hadoop/airflow/dags/alex_crypto/")


import datetime as dt

from airflow import DAG
from airflow.operators.python_operator import PythonOperator

import command

import compute.current
import compute.days

default_args = {"owner": "alex", "start_date": dt.datetime(2023, 12, 12)}

with DAG("alex_cryptoscan", default_args=default_args, dagrun_timeout=dt.timedelta(minutes=60)) as dag:
    air_command = PythonOperator(task_id="delivery_hadoop", python_callable=command.main)

    air_current = PythonOperator(task_id="current_best_in_telegram", python_callable=compute.current.main)

    air_days = PythonOperator(task_id="all_price_in_prometheus", python_callable=compute.days.main)

air_command >> [air_current, air_days]
