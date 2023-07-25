from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.providers.amazon.aws.transfers.local_to_s3 import LocalFilesystemToS3Operator
from airflow.providers.amazon.aws.hooks.s3 import S3Hook
import pandas as pd
import psycopg2
import os
from dotenv import load_dotenv
import subprocess

load_dotenv()

pem_key_path = './style-web-app.pem'
ec2_public_ip = os.environ.get('AIRFLOW_EC2_IP')
ec2_username = 'ubuntu'
remote_folder_path = '/home/ubuntu/styl-backend/logging'
local_destination_path = './logging'

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 7, 23),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'example_etl_dag',
    default_args=default_args,
    description='A simple ETL DAG',
    schedule_interval=timedelta(days=1),
)

def get_remote_files(remote_folder_path):
    command = f"ssh -i {pem_key_path} {ec2_username}@ec2-{ec2_public_ip}.ap-northeast-2.compute.amazonaws.com 'find {remote_folder_path} -type f'"
    remote_files = subprocess.check_output(command, shell=True)
    remote_files = remote_files.decode('utf-8').strip().split('\n')
    return remote_files

def save_ec2_logs_to_local():
    try:
        # 원격 폴더 내의 모든 파일과 서브 폴더 목록을 가져옴
        remote_files = get_remote_files(remote_folder_path)

        for remote_file in remote_files:
            # 로컬에 해당 파일이 있는지 확인
            local_file = os.path.join(local_destination_path, os.path.relpath(remote_file, start=remote_folder_path))
            if os.path.exists(local_file):
                # 로컬 파일이 있으면 수정 시간을 비교하여 변경 여부 확인
                remote_mtime = subprocess.check_output(f"ssh -i {pem_key_path} {ec2_username}@ec2-{ec2_public_ip}.ap-northeast-2.compute.amazonaws.com 'stat -c %Y {remote_file}'", shell=True)
                remote_mtime = int(remote_mtime.decode('utf-8').strip())

                local_mtime = os.path.getmtime(local_file)

                print('remote:',remote_mtime, "local:",local_mtime)
                if remote_mtime > local_mtime:
                    # 원격 파일이 로컬 파일보다 최신일 경우에만 파일을 가져옴
                    print("new!")
                    print(os.path.dirname(local_file), remote_file)
                    command = f"scp -i {pem_key_path} {ec2_username}@ec2-{ec2_public_ip}.ap-northeast-2.compute.amazonaws.com:{remote_file} {os.path.dirname(local_file)}"
                    subprocess.run(command, shell=True, check=True)
            else:
                # 로컬에 해당 파일이 없으면 파일을 가져옴
                os.makedirs(os.path.dirname(local_file), exist_ok=True)
                command = f"scp -i {pem_key_path} {ec2_username}@ec2-{ec2_public_ip}.ap-northeast-2.compute.amazonaws.com:{remote_file} {os.path.dirname(local_file)}"
                subprocess.run(command, shell=True, check=True)

    except subprocess.CalledProcessError as e:
        print(f"Error while executing the command: {str(e)}")


# def extract_from_postgresql():
#     connection = psycopg2.connect(
#         host=os.environ.get('AIRFLOW_PSQL_HOST'),
#         port=os.environ.get('AIRFLOW_PSQL_PORT'),
#         database='postgres',
#         user=os.environ.get('AIRFLOW_PSQL_USER'),
#         password=os.environ.get('AIRFLOW_PSQL_PWD')
#     )
#     query = "SELECT * FROM your_table"
#     df = pd.read_sql(query, connection)
#     connection.close()
#     return df

# def preprocess_data():
#     # Preprocess the data in the Pandas DataFrame
#     pass

# def save_to_s3():
#     # Save the preprocessed data to Amazon S3
#     pass

# Define tasks using PythonOperator
save_ec2_logs_to_local_task = PythonOperator(
    task_id='save_ec2_logs_to_local_task',
    python_callable=save_ec2_logs_to_local,
    dag=dag,
)

# extract_from_postgresql_task = PythonOperator(
#     task_id='extract_from_postgresql_task',
#     python_callable=extract_from_postgresql,
#     dag=dag,
# )

# preprocess_data_task = PythonOperator(
#     task_id='preprocess_data_task',
#     python_callable=preprocess_data,
#     dag=dag,
# )

# save_to_s3_task = PythonOperator(
#     task_id='save_to_s3_task',
#     python_callable=save_to_s3,
#     dag=dag,
# )

# Set task dependencies
# extract_and_preprocess_task >> extract_from_postgresql_task
# extract_from_postgresql_task >> preprocess_data_task
# preprocess_data_task >> save_to_s3_task
