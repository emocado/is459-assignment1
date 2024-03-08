'''

Name: 
Email: 

'''

from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime
from twitter_collector import run_etl
from twitter_mongo_loader import run_mongo_loader
from dotenv import load_dotenv
import os

load_dotenv()
OWNER = os.getenv('owner')

default_args = {
    'owner': OWNER,
    'depends_on_past': False,
    'start_date': datetime.today(),
    'retries': 0
}

dag = DAG(
    dag_id='is459_assignment1_twitter',
    default_args=default_args,
    catchup=False,
    schedule_interval='@once'
)


# CREATE TASK 1
task_1 = PythonOperator(
    task_id='run_etl',
    python_callable=run_etl,
    dag=dag
)


# CREATE TASK 2
task_2 = PythonOperator(
    task_id='run_mongo_loader',
    python_callable=run_mongo_loader,
    dag=dag
)


# CREATE EXECUTION SEQUENCE
task_1 >> task_2