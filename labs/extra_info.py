# from airflow import DAG
# from airflow.decorators import dag ,task
# from airflow.operators.python import PythonOperator,BranchPythonOperator
# from airflow.operators.email import EmailOperator
# from cosmos import ProfileConfig
# from dotenv import load_dotenv

# load_dotenv()

# @task(task_id = 'getting data from API',tag= ['start'])
# def get_data():
#     import requests
#     import os


#     link = os.getenv('API_URL')
#     respon = requests.get(link)
#     result = respon.json()
#     try:
#         result = result.get('Time Series FX (Daily)')
#         return result
#     except:
#         print('something error, need be re-configured')


# @task
# def reformated(some_data:dict):
#     import polars as pl

#     data = [ {
#             'Date': w,
#             'Open': q['1. open'],
#             'Close': q['4. close'],
#             'Low': q['3. low'],
#             'High': q['2. high'],
#             'Volume': q['5. volume']
#         } for w,q in some_data.items() ]
#     result = pl.LazyFrame(data)
    
#     if  result.width == 0:
#        raise IndexError(" There aren't Dataframe created during the processes")
#     else :
#         return result
    
# import polars as pl
# @task.branch
# def check_get_data(data:pl.LazyFrame):

#     checkk :pl.DataFrame = data.collect(streaming=True)

#     if checkk.height == 0 | checkk.width == 0:
#         return 'fail_email'
#     else :
#         return 'extend_transform' 

# @task
# def extend_tranform(data:pl.LazyFrame):
#     read = data.clone().collect(streaming=True)
#     return read.with_columns([
#         pl.col('date').str.to_date(),
#         pl.col('volume').cast(pl.Int64)
#     ])

# '''
# Connection URLs for Airflow within Docker
# For Airflow components in the same Docker network, use:

# Airflow Metadata Database

# metadata con :
# postgresql://airflow:airflow@postgres-airflow:5432/airflow
# Application Data Database

# data con :
# postgresql://myapp:myapp@postgres-data:5432/myapp_data
# '''

# @task
# def load_to_db(data:pl.LazyFrame):
#     import psycopg2
#     from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
#     postgres = 'postgresql://myapp:myapp@postgres-data:5432/myapp_data'
#     data2 = data.clone()
#     create_table_sql = """
#     CREATE TABLE IF NOT EXISTS stock_data (
#         Date DATE PRIMARY KEY,
#         Open FLOAT NOT NULL,
#         Close FLOAT NOT NULL,
#         Low FLOAT NOT NULL,
#         High FLOAT NOT NULL,
#         Volume BIGINT NOT NULL
#     );
#     """

#     try:
#         # Create table if doesn't exist
#         conn = psycopg2.connect(postgres)
#         conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT) # to kinda set some env where the created table is also commited at db.
#         with conn.cursor() as cur:
#             cur.execute(create_table_sql)
#         conn.close()

#         # Write data
#         df = data.collect()
#         df.write_database(
#             table_name='stock_data',
#             connection=postgres,
#             if_table_exists='append'
#         )
#     except Exception as e:
#         print(f"Database operation failed: {str(e)}")
#         raise


# @task.bash
# def finished_up():
#     return 'echo "congrats u have finishing dag proceses"'


# from datetime import datetime

# default_args = {
#     'owner':'airflow_development',
#     'retries' : 1,
#     'start_time' : datetime(2024 , 5 , 1)
# }

# '''
# <h1>Main Heading</h1>  <!-- h1 to h6 for headings -->
# <p>Paragraph text</p>
# <strong>Bold text</strong>
# <em>Italic text</em>
# <br>  <!-- Line break -->
# <hr>  <!-- Horizontal line -->
# '''

# '''
# # Common Airflow template variables:
# {{ ds }}                    # The execution date as YYYY-MM-DD
# {{ ds_nodash }}            # The execution date as YYYYMMDD
# {{ ts }}                   # The execution date with timestamp
# {{ task_instance.task_id }} # The current task's ID
# {{ task_instance.dag_id }}  # The DAG's ID
# {{ task.owner }}           # The task's owner
# {{ task.email }}           # The task owner's email
# {{ task_instance.try_number }} # The current retry attempt number
# {{ task_instance.state }}   # The task's current state
# {{ dag }}                  # The entire DAG object
# {{ conf }}                 # The Airflow configuration object
# {{ macros }}              # Access to various utility macros
# {{ var.value.some_variable }} # Access Airflow variables
# '''

# html = '''<h1> ALERT SOME DAGS HAS FALLEN!!! </h1>
# <p> today {{ds}} has ben executing regular dag 
# at :
# task {{task_instance.task_id}} 
# from :
# dag {{task_instance.dag_id}} has failed to be execute </p>
# <br>
# <p><strong>Please investigate the failure and take necessary action.</strong></p>
# <strong> Sorry for bothering ur weekend :D </strong>'''

# with DAG('updating stock data',
#     default_args = default_args,
#     catchup=False,
#     schedule_interval='0 0 30 * *',
#     tags=['testing']
# )as dag:

#     emails = EmailOperator(
#         task_id = 'fail_email',
#         to=['alifnurhadi90@gmail.com','clara.data08@gmail.com','farrosg@gmail.com','intanmuktif@gmail.com','joobeboy12@gmail.com'],
#         subject='Stock Data Pipeline Failure Alert',
#         html_content=html
#     )

#     data = get_data()
#     reform = reformated(data)
#     checking = check_get_data(reform)
#     another_ref = extend_tranform(reform)
#     load = load_to_db(reform)

#     data >> reform >> checking >> [load , emails]

from cryptography.fernet import Fernet
print(Fernet.generate_key().decode())
