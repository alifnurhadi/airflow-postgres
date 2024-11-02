from contextlib import contextmanager
import json
from re import L
import requests
import great_expectations as ge
import os
from datetime import datetime
from airflow import DAG
from airflow.decorators import task
from airflow.operators.email import EmailOperator as EmO
from airflow.operators.branch import BaseBranchOperator as BBO
from pyspark.sql import SparkSession
from pyspark.sql.types import StructField,StringType,FloatType,IntegerType,DateType,StructType,LongType


@contextmanager
def spark_session(workers=3):  # Specify the number of workers
    spark = SparkSession.builder \
        .master(f'local[{workers}]') \
        .appName('full-pipeline') \
        .config("spark.some.config.option", "some-value") \
        .config("spark.memory.fraction", "0.7") \
        .config("spark.cleaner.referenceTracking", "true") \
        .config("spark.sql.adaptive.enabled", "true") \
        .config("spark.sql.adaptive.coalescePartitions.enabled", "true") \
        .getOrCreate()

    try:
        yield spark
    finally:
        spark.stop()


api = os.getenv('Alpha_Vantage_API_KEY')
url = f'https://www.alphavantage.co/query?function=FX_DAILY&from_symbol=AUD&to_symbol=USD&outputsize=full&apikey={api}'


def get():
    ...

@task(task_id= 'fetch data')
def getdata():
    """Fetch data from the Alpha Vantage API."""
    data = requests.get(url)
    result = data.json()
    if data.status_code == 200:
        # Extract the "Time Series (Daily)" part of the response
        time_series = result.get("Time Series FX (Daily)", {})
        return time_series
    else:
        raise Exception(f"Error fetching data: {data.status_code}")

@task(task_id= 'check data')
def check_quality(data):
    ...


@task (task_id= 'reformated data')
def transform(data):
    """Transform the fetched data into a desired format."""


insert = [(w, q['1. open'] , q['4. close'] , q['3. low'] , q['2. high'] , q['5. volume']) for w , q in data.items()]
schema = StructType([
        StructField("date", DateType(), True),
        StructField("1. open", FloatType(), True),
        StructField("4. close", FloatType(), True),
        StructField("3. low", FloatType(), True),
        StructField("2. high", FloatType(), True),
        StructField("5. volume", LongType(), True)
    ])
    with spark_session() as spark:

        # Create Spark DataFrame directly
        df = spark.createDataFrame(insert, schema=schema)

        return df



@task(task_id='tweaks_data')
def tweaks():
    """Perform additional transformations or tweaks on the data."""
    with spark_session() as spark:
        df = spark.read.parquet('/data/data.parquet')
        # Perform your tweaks here
        return df


@task
def load_to_cloud():
    """Load transformed data to the cloud (e.g., AWS S3, GCS)."""
    # Implement loading logic here
    pass


def_args = {
    'owner': 'alif',
    'start_date': datetime(2024, 10, 1),
    'retries': 1,
    'email': ['jinmoori10@gmail.com'],
    'email_on_fail': True
}

with DAG('Project3',
         default_args=def_args,
         schedule_interval='0 0 1 1 *') as dag:

    send_notif = EmO(
        task_id='send_fail',
        to='alifnurhadi90@gmail.com',
        subject='Failed on process',
        html_content='The task has failed, needs to be repaired first',
        dag=dag
    )

    data = getdata()
    quality_check = check_quality(data)
    transformed_data = transform(data)
    tweaks_data = tweaks()
    load_to_cloud()

    # Set task dependencies
    data >> [send_notif, quality_check] >> transformed_data >> [send_notif, tweaks_data] >> load_to_cloud()
