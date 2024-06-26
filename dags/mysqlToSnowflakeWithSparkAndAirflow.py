from airflow import DAG
from airflow.contrib.operators.spark_submit_operator import SparkSubmitOperator
from datetime import datetime, timedelta

# Define default arguments for the DAG
default_args = {
    'owner': 'yosh0555',
    'start_date': datetime(2024, 3, 27),
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
}

# Define a DAG
mysqltosfdag = DAG('mysql_to_snowflake_poc',
        default_args=default_args,
        description='Extracting mysql dept table data, processing this data and storing it into snowflake',
        start_date=datetime(2024, 3, 27),
        schedule_interval='*/5 * * * *',
        catchup=True
)

# Define a task to run Spark job
spark_job = SparkSubmitOperator(
        task_id = 'spark_job_task',
        application = '/home/yosh0555/spark.py',
        conn_id = 'connect_spark',
        verbose = False,
        jars = '/home/yosh0555/mysql-connector-java-8.0.11.jar,/home/yosh0555/snowflake-jdbc-3.14.4.jar,/home/yosh0555/snowflake-ingest-sdk-2.0.2.jar,/home/yosh0555/spark-snowflake_2.12-2.11.3-spark_3.1.jar',
        dag = mysqltosfdag
)
