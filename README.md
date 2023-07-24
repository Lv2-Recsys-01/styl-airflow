# styl-airflow

single node airflow for batching data ingestion and processing

airflow는 일단 로컬에서 설치형으로 작업하되, 외부 필요한 서비스들은 docker로 작동

## docs

[extra pkg](https://airflow.apache.org/docs/apache-airflow/stable/extra-packages-ref.html)  
[pg13 docs korean](https://www.postgresql.kr/docs/13/)

## init

```bash
conda create -n air python=3.10
conda activate air
conda env remove -n air # remove env if needed
```

```bash
sh airflow_setup.sh
sh set_env.sh

# airflow.cfg를 입맛에 맞게 수정 한 후 확인
airflow info # check airflow configuration

airflow db init
airflow db upgrade # create the database schema that Airflow can use
airflow db check # db reachable?
airflow db reset # reset db


airflow users create --username admin \
    --firstname admin --lastname admin \
    --role Admin \
    --email darrenkwondev46@gmail.com

airflow users list


airflow webserver --port 8080
airflow scheduler
```

```bash
# task 추가시. 의존 task를 다 실행하지 않고 Test a task instance.
airflow tasks test $dag_id $tasks_id $execution_date(YYYY-MM-DD)
```

## troubleshooting

### Task exited with return code Negsignal.SIGTRAP

```bash
export OBJC_DISABLE_INITIALIZE_FORK_SAFETY=YES
```
