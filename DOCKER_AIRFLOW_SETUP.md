# Running Apache Airflow with Docker

## Prerequisites
- Docker Desktop (https://www.docker.com/products/docker-desktop)
- Docker Compose

## Quick Start

### 1. Install Docker (if not already installed)
```bash
# On macOS, you can use Homebrew:
brew install --cask docker
```

### 2. Start Airflow
```bash
cd /Users/ssingh14/Downloads/XYZ_DEMO_CHECK/appgithubaction

# Start all services (webserver, scheduler, postgres, redis)
docker-compose up -d

# Wait for services to be ready (about 30 seconds)
sleep 30

# Check status
docker-compose ps
```

### 3. Access Airflow Web UI
Open your browser and go to:
```
http://localhost:8080
```

**Login Credentials:**
- **Username:** `admin`
- **Password:** `admin`

### 4. View Your DAGs
Once logged in, you'll see:
- **ml_pipeline_dag** - Your ML pipeline DAG
- DAG graph visualization
- Task logs
- Run history
- Trigger DAG runs

## Docker Commands

### View logs
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f airflow-webserver
docker-compose logs -f airflow-scheduler
```

### Stop Airflow
```bash
docker-compose down
```

### Stop and remove all data
```bash
docker-compose down -v
```

### Restart services
```bash
docker-compose restart
```

### Monitor running containers
```bash
docker-compose ps
```

## Troubleshooting

### Services not starting
```bash
# Check logs
docker-compose logs

# Rebuild images
docker-compose build --no-cache
docker-compose up -d
```

### DAG not appearing
- Make sure `dags/ml_pipeline_dag.py` exists
- Refresh the browser
- Check scheduler logs: `docker-compose logs airflow-scheduler`

### Port already in use
If port 8080 is already in use:
```bash
# Edit docker-compose.yml and change:
# ports:
#   - "8081:8080"  # Use 8081 instead

docker-compose up -d
```

## Architecture

```
┌─────────────────────────────────────────────┐
│         Docker Compose Services             │
├─────────────────────────────────────────────┤
│                                             │
│  ┌──────────────────────────────────────┐  │
│  │   Airflow Web Server (Port 8080)    │  │
│  │   - View DAGs                       │  │
│  │   - Trigger runs                    │  │
│  │   - View logs                       │  │
│  └──────────────────────────────────────┘  │
│                    │                        │
│                    ▼                        │
│  ┌──────────────────────────────────────┐  │
│  │   Airflow Scheduler                  │  │
│  │   - Monitors DAGs                   │  │
│  │   - Schedules tasks                 │  │
│  │   - Executes tasks                  │  │
│  └──────────────────────────────────────┘  │
│                    │                        │
│                    ▼                        │
│  ┌──────────────────────────────────────┐  │
│  │   PostgreSQL Database                │  │
│  │   - Stores DAG metadata             │  │
│  │   - Task history                    │  │
│  │   - Execution logs                  │  │
│  └──────────────────────────────────────┘  │
│                                             │
│  ┌──────────────────────────────────────┐  │
│  │   Redis (Optional)                   │  │
│  │   - Task queue (future)              │  │
│  └──────────────────────────────────────┘  │
│                                             │
└─────────────────────────────────────────────┘
```

## Your ML Pipeline DAG

Once Airflow is running, you can:

1. **View the DAG Graph** - See the visual representation of all tasks and dependencies
2. **Trigger a DAG Run** - Click "Trigger DAG" to start a pipeline execution
3. **Monitor Execution** - View task status in real-time
4. **Check Logs** - Click on tasks to see detailed execution logs
5. **View Metrics** - See task duration, success/failure rates, etc.

## Next Steps

- Modify `dags/ml_pipeline_dag.py` to add more tasks
- Connect to real data sources
- Set up email notifications
- Configure backfill for historical data
- Deploy to production Kubernetes cluster

## Resources

- [Apache Airflow Documentation](https://airflow.apache.org/docs/)
- [Airflow Docker Images](https://github.com/apache/airflow/tree/main/docker)
- [Airflow Best Practices](https://airflow.apache.org/docs/apache-airflow/stable/best_practices.html)
