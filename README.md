# styl-airflow

for batching data ingestion and processing

## set uid for host, container RBAC authorization

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
