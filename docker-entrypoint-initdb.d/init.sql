-- https://airflow.apache.org/docs/apache-airflow/stable/howto/set-up-database.html#setting-up-a-postgresql-database

SELECT rolname FROM pg_roles;
SELECT * FROM pg_user;


-- CREATE DATABASE airflow_db;
-- CREATE DATABASE airflow;
-- CREATE USER airflow WITH PASSWORD 'airflow';
-- GRANT ALL PRIVILEGES ON DATABASE airflow_db TO airflow;

-- -- PostgreSQL 15 requires additional privileges:
-- USE airflow_db;
-- GRANT ALL ON SCHEMA public TO airflow_user;