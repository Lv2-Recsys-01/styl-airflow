from datetime import datetime

from airflow import DAG
from airflow.providers.postgres.operators.postgres import PostgresOperator

with DAG(
    "user_processing",
    default_args={},
    description="A simple tutorial DAG",
    start_date=datetime(2023, 1, 1),
    schedule_interval="@daily",
    catchup=False,
    tags=["lesson"],
) as dag:
    # https://airflow.apache.org/docs/apache-airflow-providers-postgres/stable/operators/postgres_operator_howto_guide.html
    create_table = PostgresOperator(
        task_id="create_table",
        # url="postgresql+psycopg2://airflow:airflow@127.0.0.1:30001/airflow_db",
        postgres_conn_id="postgresql_local",
        sql="""
            CREATE TABLE IF NOT EXISTS lesson_user (
                firstname TEXT NOT NULL,
                lastname TEXT NOT NULL,
                country TEXT NOT NULL,
                username TEXT NOT NULL,
                password TEXT NOT NULL,
                email TEXT NOT NULL
            )
        """,
    )
