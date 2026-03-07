# Apache Airflow DAG Documentation

## Overview

This project includes an Apache Airflow-based ML pipeline with Directed Acyclic Graphs (DAGs) for workflow orchestration and scheduling.

## DAG Architecture

### ML Pipeline DAG: `ml_pipeline_dag.py`

**Purpose**: Orchestrate the complete machine learning pipeline from data ingestion to model deployment.

**Schedule**: Daily at 2 AM UTC (`0 2 * * *`)

**Task Flow Diagram**:
```
┌─────────────┐
│ Fetch Data  │
└──────┬──────┘
       │
       ▼
┌──────────────────┐
│ Validate Data    │
└──────┬───────────┘
       │
       ▼
┌──────────────────────┐
│ Preprocess Data      │
└──────┬───────────────┘
       │
       ▼
┌──────────────────┐
│ Train Model      │
└──────┬───────────┘
       │
       ├─────────────────────┐
       ▼                     ▼
┌──────────────────┐  ┌────────────┐
│ Evaluate Model   │  │ Run Tests  │
└──────┬───────────┘  └──────┬─────┘
       │                     │
       └────────┬────────────┘
                ▼
        ┌──────────────────┐
        │ Deploy Model     │
        └──────┬───────────┘
               │
               ▼
        ┌──────────────────┐
        │ Log Results      │
        └──────────────────┘
```

## Tasks Description

### 1. **Fetch Data** (`fetch_data`)
- Retrieves data from source systems
- Outputs data record count and metadata
- Pushes data to XCom for downstream tasks

### 2. **Validate Data** (`validate_data`)
- Validates data quality and completeness
- Checks for required fields and formats
- Fails pipeline if validation criteria not met

### 3. **Preprocess Data** (`preprocess_data`)
- Cleans and transforms raw data
- Creates features for model training
- Handles missing values and outliers

### 4. **Train Model** (`train_model`)
- Trains the ML model on processed data
- Logs training metrics (accuracy, precision, recall)
- Saves model artifacts

### 5. **Evaluate Model** (`evaluate_model`)
- Evaluates model performance on test set
- Calculates AUC, F1-score, and other metrics
- Ensures model meets production thresholds
- **Blocks deployment if metrics below threshold**

### 6. **Run Tests** (`run_tests`)
- Executes unit tests using pytest
- Validates code quality
- **Blocks deployment if tests fail**

### 7. **Deploy Model** (`deploy_model`)
- Deploys validated model to production
- Only runs if evaluation and tests passed
- Updates API endpoints

### 8. **Log Results** (`log_results`)
- Logs final pipeline execution summary
- Records deployment details
- Generates audit trail

## Getting Started

### Prerequisites
```bash
# Python 3.8+
# pip (Python package manager)
```

### Installation

1. **Install dependencies**:
```bash
cd /Users/ssingh14/Downloads/XYZ_DEMO_CHECK/appgithubaction
pip install -r requirements.txt
```

2. **Initialize Airflow**:
```bash
export AIRFLOW_HOME=/Users/ssingh14/Downloads/XYZ_DEMO_CHECK/appgithubaction/airflow_home
airflow db init
```

3. **Create Airflow admin user**:
```bash
airflow users create \
  --username admin \
  --firstname Admin \
  --lastname User \
  --role Admin \
  --email admin@example.com \
  --password admin123
```

### Running Airflow

#### Method 1: Start the Web UI (Recommended for Development)

```bash
# Terminal 1: Start the Airflow webserver
export AIRFLOW_HOME=/Users/ssingh14/Downloads/XYZ_DEMO_CHECK/appgithubaction/airflow_home
airflow webserver -p 8080

# Terminal 2: Start the Airflow scheduler
export AIRFLOW_HOME=/Users/ssingh14/Downloads/XYZ_DEMO_CHECK/appgithubaction/airflow_home
airflow scheduler
```

Then open: **http://localhost:8080**
- Username: `admin`
- Password: `admin123`

#### Method 2: Run DAG Manually

```bash
export AIRFLOW_HOME=/Users/ssingh14/Downloads/XYZ_DEMO_CHECK/appgithubaction/airflow_home

# Trigger DAG run
airflow dags trigger ml_pipeline_dag

# View DAG structure
airflow dags list
airflow dags show ml_pipeline_dag

# View task dependencies
airflow tasks list ml_pipeline_dag
```

#### Method 3: Run Specific Task

```bash
export AIRFLOW_HOME=/Users/ssingh14/Downloads/XYZ_DEMO_CHECK/appgithubaction/airflow_home

# Run a specific task
airflow tasks test ml_pipeline_dag fetch_data 2024-01-01
```

## Monitoring & Debugging

### View DAG Runs
```bash
# List all DAG runs
airflow dags list-runs -d ml_pipeline_dag

# Get specific run details
airflow dags list-runs -d ml_pipeline_dag --state success
```

### View Task Logs
```bash
# View logs for a specific task
airflow tasks logs ml_pipeline_dag fetch_data 2024-01-01T00:00:00
```

### Clear Task State
```bash
# Clear a task to re-run it
airflow tasks clear ml_pipeline_dag --task_ids fetch_data
```

## Key Concepts

### XCom (Cross Communication)
Tasks communicate via XCom to pass data:
```python
# Push data
context['task_instance'].xcom_push(key='my_key', value=data)

# Pull data
data = context['task_instance'].xcom_pull(key='my_key', task_ids='source_task')
```

### Task Dependencies
Defined using the `>>` operator:
```python
task1 >> task2 >> task3  # Linear dependency
task1 >> [task2, task3]  # Parallel execution
```

### Retries & Error Handling
- **retries**: Number of times to retry failed tasks (default: 2)
- **retry_delay**: Wait time between retries (default: 5 minutes)
- **email_on_failure**: Send email notifications on failure

## Configuration

### airflow.cfg Settings
- **executor**: SequentialExecutor (single-threaded, good for dev)
- **database**: SQLite for local development
- **webserver_port**: 8080
- **dag_dir**: dags/

### For Production
Consider these changes:
```ini
executor = CeleryExecutor  # Instead of SequentialExecutor
sql_alchemy_conn = postgresql://user:password@localhost/airflow
```

## Troubleshooting

### Error: "DAG Not Found"
- Ensure DAG file is in `dags/` directory
- Reload Airflow: `airflow dags reparse`

### Error: "Task Failed"
- Check task logs in Airflow UI
- Run with verbose mode: `airflow tasks test -l ml_pipeline_dag task_name 2024-01-01`

### Error: "Database Lock"
- SQLite has limitations. For production, use PostgreSQL
- Clear database: `rm ~/airflow/airflow.db && airflow db init`

## Project Structure

```
appgithubaction/
├── dags/
│   └── ml_pipeline_dag.py          # Main DAG definition
├── airflow_home/                   # Airflow home directory
│   ├── airflow.db                  # SQLite database
│   └── logs/                       # DAG execution logs
├── airflow.cfg                     # Airflow configuration
├── requirements.txt                # Python dependencies
└── README.md                       # Project documentation
```

## Next Steps

1. **Extend the DAG**: Add more tasks for your specific ML pipeline
2. **Connect to data sources**: Integrate with databases, S3, etc.
3. **Setup email notifications**: Configure SMTP for alerts
4. **Deploy to production**: Use CeleryExecutor and PostgreSQL
5. **Add monitoring**: Integrate with DataDog, Prometheus, etc.

## Resources

- [Apache Airflow Documentation](https://airflow.apache.org/)
- [Airflow Python API Reference](https://airflow.apache.org/docs/apache-airflow/stable/python_api.html)
- [DAG Best Practices](https://airflow.apache.org/docs/apache-airflow/stable/best_practices.html)
