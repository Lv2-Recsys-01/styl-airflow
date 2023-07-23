# styl-airflow

single node airflow for batching data ingestion and processing

## set uid for host, container auth connect

```bash
echo -e "AIRFLOW_UID=$(id -u)" > .env
```

## clean up env

```bash
docker rm $(docker ps -a -q)
docker-compose down --volumes --rmi all

docker compose up airflow-init

docker compose up
```

## celery

써보니, app을 정의하고 내부에 task를 정의 한 후 데몬화해서 쓰는 task queue임.
broker와 결과를 저장할 backend가 필요함. airflow에서는 redis를 broker, backend로 psql을 사용하는 것으로 보임.

```bash
celery -A airflow.executors.celery_executor.app inspect registered # 등록된(registered) 작업(task) 리스트가 출력
celery -A airflow.executors.celery_executor.app status
```

## redis

알자나. 여기저기에 쓰기 좋음. redis-cli로 접속해서 확인해보자.

styl-airflow-airflow-worker-1 | [2023-07-22 16:23:02 +0000] [95] [INFO] Booting worker with pid: 95
styl-airflow-airflow-worker-1 | [2023-07-22 16:23:02 +0000] [97] [INFO] Booting worker with pid: 97
