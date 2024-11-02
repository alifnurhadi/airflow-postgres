import os
from airflow import DAG
from airflow.decorators import task
from airflow.operators.email import EmailOperator
from airflow.operators.bash import BashOperator
from dotenv import load_dotenv
from datetime import datetime, timedelta
import polars as pl
import requests
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

# Load environment variables
# load_dotenv()
@task
def get_data():
    """Fetches stock data from an API and returns the JSON response as a dictionary."""

    link = os.getenv('ALPHA_VANTAGE_API_KEY')
    web = f'https://www.alphavantage.co/query?function=FX_DAILY&from_symbol=AUD&to_symbol=USD&outputsize=full&apikey={link}'

    print(f'this line {web}')
    try:
        response = requests.get(web, timeout=30)
        result = response.json()
        time_series_data:dict = result.get('Time Series FX (Daily)')
        print(f"Parsed Time Series Data: {time_series_data}")
        print(f"Returned data type: {type(time_series_data)}")
        if response.status_code != 200:
            raise Exception(f"API returned error: {response.status_code}") 
        if not result:
            raise ValueError("No data received from API")
        return time_series_data
    except Exception as e:
        print(f'Error: {e}')
        return {}

@task
def reformating_datas(some_data: dict):
    """Converts raw API data into a Polars LazyFrame."""
    try:
        time_series_data = some_data
        data = [{
            'Date': w,
            'Open': q['1. open'],
            'Close': q['4. close'],
            'Low': q['3. low'],
            'High': q['2. high']
        } for w, q in time_series_data.items()]

        if not data:
            raise ValueError("No valid data found in the API response.")
        
        month_ago = datetime.now() - timedelta(days=30)
        result = pl.LazyFrame(data).filter(pl.col('Date') >= str(month_ago))

        if result.collect().shape[0] == 0:
            raise IndexError("No data was formatted into a DataFrame")
        else:
            result2 = [ row for row in data if row['Date'] >= str(month_ago)]
            return result2
        
    except Exception as e:
        print(f"Error in data reformatting: {str(e)}")
        raise

@task.branch
def check_processes(data: list):
    """Checks if the data is empty. If empty, branches to 'fail_email', else continues to 'final_transformation'."""
    processed_data = pl.LazyFrame(data)
    checked_data: pl.DataFrame = processed_data.collect()
    try:
        if checked_data.shape[0] == 0:
            return 'error_nor_failure'
        else:
            return 'final_transformation'
    except Exception as e:
        print(f"Error in process checking: {str(e)}")
        return 'error_nor_failure'

# Alert email template for failures
html_failure = '''<h1>ALERT: DAG Execution Failure</h1>
<p>The DAG '{{ task_instance.dag_id }}' encountered an error during execution on {{ ds }} at task '{{ task_instance.task_id }}'.</p>
<p><strong>Immediate investigation is recommended.</strong></p>'''

# Failure email task
fail_email = EmailOperator(
    task_id='error_nor_failure',
    to=['alifnurhadi90@gmail.com', 'clara.data08@gmail.com', 'farrosg@gmail.com', 'intanmuktif@gmail.com', 'joobeboy12@gmail.com'],
    subject='Stock Data Pipeline Failure Alert',
    html_content=html_failure
)

@task
def error_nor_failure():
    """Handles the case when the data is empty."""
    print("Error: No data to process. Triggering failure email.")

@task
def final_transformation(data: list):
    """Adds new columns and type casts existing columns in the data."""
    dataframe = pl.LazyFrame(data)
    df = dataframe.collect()
    df =  df.with_columns([
        pl.col(['Open', 'Close', 'Low', 'High']).cast(pl.Float64)
    ]).select(pl.all())
    return df.to_dicts()

@task
def load_to_db(data: list):
    """Loads data into a PostgreSQL database."""
    postgres_url = 'postgresql://myapp:myapp@postgres:5432/myapp'
    print(f'postgres url{postgres_url}')
    if not postgres_url:
        raise ValueError("Database URL not found in environment variables")

    create_table_sql = """
    CREATE TABLE IF NOT EXISTS stock_data (
        date DATE PRIMARY KEY,
        open FLOAT NOT NULL,
        close FLOAT NOT NULL,
        low FLOAT NOT NULL,
        high FLOAT NOT NULL
    );
    """

    try:
        # Establish connection and create table
        conn = psycopg2.connect(postgres_url)
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        with conn.cursor() as cur:
            cur.execute(create_table_sql)
        conn.close()

        # Insert data into database
        final = pl.LazyFrame(data).collect()
        final = final.rename({col : col.lower() for col in final.columns})
        final.write_database(
            table_name='stock_data',
            connection=postgres_url,
            if_table_exists='append'
        )
    except Exception as e:
        print(f"Database operation failed: {str(e)}")
        raise

# Success email template after DAG completion
html_success = '''<h1>DAG Execution Success</h1>
<p>The DAG '{{ task_instance.dag_id }}' completed successfully on {{ ds }}.</p>
'''
# Success email task
success_email_task = EmailOperator(
    task_id='success_email',
    to=['alifnurhadi90@gmail.com', 'clara.data08@gmail.com', 'farrosg@gmail.com', 'intanmuktif@gmail.com', 'joobeboy12@gmail.com'],
    subject='Stock Data Pipeline Success Notification',
    html_content=html_success
)

default_args = {
    'owner': 'airflow_development',
    'retries': 1,
    'start_date': datetime(2024, 5, 1),
    'email_on_failure': True,
    'email_on_retry': True
}

# Define DAG
with DAG(
    'updating_stock_data',
    default_args=default_args,
    catchup=False,
    schedule_interval='0 0 30 * *',
    tags=['stock_data']
) as dag:

    # Tasks
    data = get_data()
    reform = reformating_datas(data)
    checking = check_processes(reform)
    transform = final_transformation(reform)
    error_handling = error_nor_failure()
    load = load_to_db(transform)

    confirm_completion = BashOperator(
        task_id='success_logging',
        bash_command='echo "DAG process has successfully completed , CONGRATS"',
    )

    # Task Dependencies
    data >> reform >> checking >> [transform, error_handling]
    transform >> load >> confirm_completion >> success_email_task


'''
from dataclasses import dataclass
from datetime import datetime

@dataclass
class metadata_file:
    location: str
    rows: int
    columns: List[str]
    created_at: datetime
    metadata: Dict = None # anything that help the logging processes.
    
    def validate(self) -> bool:
        """Validate if data exists and is accessible"""
        if not os.path.exists(self.location):
            raise FileNotFoundError(f"Data not found at {self.location}")
        return True
    

@task
def reference_extract() -> DataReference:

    start_time = time.time()
    
    # Transformation logic + end-up with export file
    data.write_parquet(file_path)
    
    processing_time = time.time() - start_time
    
    return DataReference(
        location=file_path,
        rows=len(data),
        columns=data.columns,
        created_at=datetime.now(),
        metadata={
            'processing_time': processing_time,
            'source': 'any_source',
            'memory_usage': data.estimated_size("mb"),
            'null_counts': len(data.filter(pl.any(pl.col("*").is_null())))
        }
    )

@task
def reference_transform(data_ref: DataReference) -> DataReference:
    
    data_ref.validate()
    
    # Transformation logic + end-up with export file
    data = pl.read_parquet(data_ref.location)
    data.write_parquet(new_path)
    
    return DataReference(
        location=new_path,
        rows=len(data),
        columns=data.columns,
        created_at=datetime.now(),
        metadata={
            'processing_time': time.time() - start_time,
            'source_reference': data_ref.location,
            'transformation_type': 'standard',
            'memory_usage': data.estimated_size("mb")
        }
    )

'''