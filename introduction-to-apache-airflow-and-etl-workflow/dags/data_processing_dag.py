from datetime import datetime
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from sklearn.model_selection import train_test_split
import pandas as pd
from sklearn.linear_model import LinearRegression
import requests
import json

# Task 1: Extract data from local JSON file
def extract_data_from_json():
    json_file_path = '/Users/jeff/Work/gs/intro-to-airflow-etl/data.json'
    with open(json_file_path, 'r') as file:
        data = json.load(file)
    return data

# Task 2: Transform the data with pandas and store as CSV
def transform_data_and_store(**context):
    data = context['ti'].xcom_pull(task_ids='extract_data_from_json')
    df = pd.DataFrame(data)
    df = df.rename(columns={'Price': 'price', 'SquareFootage': 'sqft'})
    df.to_csv('output.csv', index=False)

# Task 3: Train linear regression model with scikit-learn
def train_linear_regression_model():
    data = pd.read_csv('output.csv')
    X = data['sqft'].values.reshape(-1, 1) 
    y = data['price'].values

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = LinearRegression()
    model.fit(X_train, y_train)

# Define the DAG
default_args = {
    'owner': 'airflow',
    'start_date': datetime(2023, 5, 29),
}

dag = DAG('ml_training', default_args=default_args, schedule_interval=None)

# Define the tasks
task1 = PythonOperator(
    task_id='extract_data_from_json',
    python_callable=extract_data_from_json,
    dag=dag
)

task2 = PythonOperator(
    task_id='transform_data_and_store',
    python_callable=transform_data_and_store,
    provide_context=True,
    dag=dag
)

task3 = PythonOperator(
    task_id='train_linear_regression_model',
    python_callable=train_linear_regression_model,
    dag=dag
)

# Define the task dependencies
task1 >> task2 >> task3
