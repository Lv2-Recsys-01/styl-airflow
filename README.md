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
conda env remove -n air # remove env

sh airflow_setup.sh

# airflow.cfg를 입맛에 맞게 수정
# 반영 확인. 문제 있다면 $AIRFLOW_HOME 확인 요망
airflow info # check airflow configuration

airflow db init
airflow db upgrade # create the database schema that Airflow can use
airflow db check # db reachable?
airflow db reset


airflow users create --username admin --firstname admin --lastname admin --role Admin --email darrenkwondev46@gmail.com
airflow users list


airflow webserver --port 8080
```
