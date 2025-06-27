from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
import os
import sys

# 🛠️ Permet à Airflow de trouver le script belib_ingestion.py même en container
sys.path.append(os.path.dirname(__file__))

from belib_ingestion import run_belib_pipeline

# ⚙️ Paramètres par défaut du DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,  # True si tu veux des alertes email
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# 🗓️ Définition du DAG
with DAG(
    dag_id='belib_to_mongodb',
    default_args=default_args,
    description='ETL vers MongoDB : récupération des données Vélib toutes les 30 minutes',
    schedule_interval='*/30 * * * *',  # toutes les 30 minutes
    start_date=datetime(2024, 1, 1),
    catchup=False,
    max_active_runs=1,
    tags=['etl', 'velib', 'mongodb'],
) as dag:

    # 📦 Tâche principale d’exécution du pipeline
    task_run_pipeline = PythonOperator(
        task_id='fetch_and_store_velib_data',
        python_callable=run_belib_pipeline,
        dag=dag,
        doc_md="""
        ### Pipeline ETL Vélib ➝ MongoDB
        Cette tâche appelle le script Python `run_belib_pipeline` toutes les 30 minutes pour :
        - Extraire les données depuis l’API open data Vélib
        - Ajouter un timestamp d’insertion
        - Insérer les documents dans la base MongoDB Compass locale
        """
    )

    task_run_pipeline  # liaison explicite dans le DAG
