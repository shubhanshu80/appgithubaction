"""
ML Pipeline DAG - Main workflow orchestration
Demonstrates a complete ML pipeline with data processing, training, and deployment
"""

from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from airflow.utils.dates import days_ago

# Default DAG arguments
default_args = {
    'owner': 'ml-team',
    'start_date': days_ago(1),
    'retries': 2,
    'retry_delay': timedelta(minutes=5),
    'email_on_failure': True,
    'email_on_retry': False,
    'email': ['ml-alerts@example.com'],
}

# Define DAG
dag = DAG(
    'ml_pipeline_dag',
    default_args=default_args,
    description='ML CI/CD Pipeline with Data Processing and Model Training',
    schedule_interval='0 2 * * *',  # Run daily at 2 AM
    catchup=False,
    tags=['ml', 'pipeline', 'production'],
)


# Task 1: Data Fetch
def fetch_data(**context):
    """Fetch data from source"""
    print("🔄 Fetching data from source...")
    # Simulate data fetching
    data = {
        'records': 1000,
        'status': 'success',
        'timestamp': datetime.now().isoformat()
    }
    context['task_instance'].xcom_push(key='data_fetched', value=data)
    print(f"✅ Data fetched: {data['records']} records")
    return data


# Task 2: Data Validation
def validate_data(**context):
    """Validate fetched data"""
    print("🔍 Validating data...")
    data = context['task_instance'].xcom_pull(key='data_fetched', task_ids='fetch_data')
    
    if data['records'] > 0:
        print(f"✅ Data validation passed: {data['records']} records validated")
        context['task_instance'].xcom_push(key='data_valid', value=True)
        return True
    else:
        raise ValueError("No data records found!")


# Task 3: Data Preprocessing
def preprocess_data(**context):
    """Clean and preprocess data"""
    print("🧹 Preprocessing data...")
    data_valid = context['task_instance'].xcom_pull(key='data_valid', task_ids='validate_data')
    
    if data_valid:
        preprocessing_result = {
            'cleaned_records': 950,  # Assume 50 records were removed as outliers
            'features_created': 15,
            'status': 'preprocessing_complete'
        }
        context['task_instance'].xcom_push(key='preprocessed_data', value=preprocessing_result)
        print(f"✅ Preprocessing complete: {preprocessing_result['cleaned_records']} records, {preprocessing_result['features_created']} features")
        return preprocessing_result


# Task 4: Model Training
def train_model(**context):
    """Train ML model"""
    print("🤖 Training model...")
    preprocess_result = context['task_instance'].xcom_pull(key='preprocessed_data', task_ids='preprocess_data')
    
    training_result = {
        'model_name': 'model_v1.0',
        'accuracy': 0.92,
        'precision': 0.89,
        'recall': 0.91,
        'training_time_seconds': 245,
        'status': 'training_complete'
    }
    context['task_instance'].xcom_push(key='trained_model', value=training_result)
    print(f"✅ Model training complete - Accuracy: {training_result['accuracy']}")
    return training_result


# Task 5: Model Evaluation
def evaluate_model(**context):
    """Evaluate trained model"""
    print("📊 Evaluating model...")
    model_result = context['task_instance'].xcom_pull(key='trained_model', task_ids='train_model')
    
    evaluation_result = {
        'model_name': model_result['model_name'],
        'accuracy': model_result['accuracy'],
        'auc_score': 0.95,
        'f1_score': 0.90,
        'passed_threshold': model_result['accuracy'] > 0.85,
        'status': 'evaluation_complete'
    }
    context['task_instance'].xcom_push(key='evaluation_result', value=evaluation_result)
    
    if not evaluation_result['passed_threshold']:
        raise ValueError("Model did not pass evaluation threshold!")
    
    print(f"✅ Model evaluation complete - AUC: {evaluation_result['auc_score']}")
    return evaluation_result


# Task 6: Run Unit Tests
def run_tests(**context):
    """Run unit tests on the pipeline"""
    print("🧪 Running unit tests...")
    import subprocess
    result = subprocess.run(
        ['pytest', 'tests/', '-v', '--tb=short'],
        cwd='/Users/ssingh14/Downloads/XYZ_DEMO_CHECK/appgithubaction',
        capture_output=True,
        text=True
    )
    
    if result.returncode == 0:
        print("✅ All unit tests passed")
        context['task_instance'].xcom_push(key='tests_passed', value=True)
        return True
    else:
        print(f"❌ Tests failed:\n{result.stdout}\n{result.stderr}")
        raise ValueError("Unit tests failed!")


# Task 7: Deploy Model
def deploy_model(**context):
    """Deploy model to production"""
    print("🚀 Deploying model...")
    evaluation_result = context['task_instance'].xcom_pull(key='evaluation_result', task_ids='evaluate_model')
    tests_passed = context['task_instance'].xcom_pull(key='tests_passed', task_ids='run_tests')
    
    if evaluation_result['passed_threshold'] and tests_passed:
        deployment_result = {
            'model_name': evaluation_result['model_name'],
            'deployment_status': 'deployed',
            'endpoint': 'https://ml-api.example.com/v1/predict',
            'timestamp': datetime.now().isoformat()
        }
        context['task_instance'].xcom_push(key='deployment_result', value=deployment_result)
        print(f"✅ Model deployed successfully at {deployment_result['endpoint']}")
        return deployment_result
    else:
        raise ValueError("Model deployment blocked: evaluation or tests failed")


# Task 8: Monitoring and Logging
def log_results(**context):
    """Log final results"""
    print("📝 Logging final results...")
    deployment_result = context['task_instance'].xcom_pull(key='deployment_result', task_ids='deploy_model')
    
    print("\n" + "="*60)
    print("ML PIPELINE EXECUTION SUMMARY")
    print("="*60)
    print(f"Pipeline Status: ✅ SUCCESS")
    print(f"Model Name: {deployment_result['model_name']}")
    print(f"Deployment Status: {deployment_result['deployment_status']}")
    print(f"Endpoint: {deployment_result['endpoint']}")
    print(f"Timestamp: {deployment_result['timestamp']}")
    print("="*60 + "\n")


# Define Tasks
t1 = PythonOperator(
    task_id='fetch_data',
    python_callable=fetch_data,
    dag=dag,
)

t2 = PythonOperator(
    task_id='validate_data',
    python_callable=validate_data,
    dag=dag,
)

t3 = PythonOperator(
    task_id='preprocess_data',
    python_callable=preprocess_data,
    dag=dag,
)

t4 = PythonOperator(
    task_id='train_model',
    python_callable=train_model,
    dag=dag,
)

t5 = PythonOperator(
    task_id='evaluate_model',
    python_callable=evaluate_model,
    dag=dag,
)

t6 = PythonOperator(
    task_id='run_tests',
    python_callable=run_tests,
    dag=dag,
)

t7 = PythonOperator(
    task_id='deploy_model',
    python_callable=deploy_model,
    dag=dag,
)

t8 = PythonOperator(
    task_id='log_results',
    python_callable=log_results,
    dag=dag,
)

# Define Task Dependencies (DAG Structure)
t1 >> t2 >> t3 >> t4 >> t5
t5 >> t6 >> t7 >> t8
