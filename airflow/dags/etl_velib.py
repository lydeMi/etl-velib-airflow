import os
import requests
from pymongo import MongoClient
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

def fetch_data():
    params = {
        "dataset": os.getenv("VELIB_DATASET"),
        "rows": os.getenv("VELIB_ROWS")
    }
    response = requests.get(os.getenv("VELIB_API_URL"), params=params)
    response.raise_for_status()
    return response.json()["records"]

def save_to_mongo(**context):
    records = context['ti'].xcom_pull(task_ids='fetch_data')
    client = MongoClient(os.getenv("MONGO_URI"))
    db = client[os.getenv("MONGO_DB")]
    collection = db[os.getenv("MONGO_COLLECTION")]
    collection.insert_many([record["fields"] for record in records])

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 1, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG("etl_velib", default_args=default_args, schedule_interval='@hourly', catchup=False) as dag:
    t1 = PythonOperator(task_id='fetch_data', python_callable=fetch_data)
    t2 = PythonOperator(task_id='save_to_mongo', python_callable=save_to_mongo, provide_context=True)

    t1 >> t2
