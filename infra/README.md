# Data Park Infrastructure

This directory contains the Kubernetes YAML files for deploying the Data Park infrastructure.

## Components

- **Spark**: Apache Spark cluster with master, workers, and history server
- **Kafka**: Kafka messaging system with Zookeeper
- **PostgreSQL**: PostgreSQL database for data storage and Airflow metadata
- **Airflow**: Apache Airflow for workflow orchestration
- **Jupyter**: Jupyter Notebook for interactive development

## Directory Structure

```
infra/
├── common/           # Common resources like namespace, ingress, storage classes
├── spark/            # Spark master, workers, and history server
├── kafka/            # Kafka and Zookeeper
├── postgres/         # PostgreSQL database
├── airflow/          # Airflow web server, scheduler, and workers
└── jupyter/          # Jupyter notebook server
```

## Deployment Order

For proper deployment, apply the YAML files in the following order:

1. Common resources
   ```
   kubectl apply -f infra/common/
   ```

2. PostgreSQL (since other services depend on it)
   ```
   kubectl apply -f infra/postgres/
   ```

3. Kafka and Zookeeper
   ```
   kubectl apply -f infra/kafka/
   ```

4. Spark
   ```
   kubectl apply -f infra/spark/
   ```

5. Airflow
   ```
   kubectl apply -f infra/airflow/
   ```

6. Jupyter
   ```
   kubectl apply -f infra/jupyter/
   ```

## Accessing the Services

After deployment, you can access the services at the following URLs:

- Spark Master UI: http://data-park.local/spark
- Spark History Server: http://data-park.local/history
- Airflow UI: http://data-park.local/airflow
- Jupyter Notebook: http://data-park.local/jupyter

## Integration Details

- Spark is configured to connect to PostgreSQL using JDBC
- Airflow has preconfigured connections to Spark, PostgreSQL, and Kafka
- Jupyter includes sample notebooks for Spark, Kafka, and PostgreSQL integration
- Kafka is initialized with topics for customer events, product events, order events, and clickstream data

## Local Development

For local development, ensure you have:

1. Added `data-park.local` to your hosts file pointing to your local IP
2. Installed Kubernetes with ingress controller enabled
3. Configured local storage provisioner for persistent volumes

## Resource Requirements

The entire infrastructure requires at minimum:
- 8GB RAM
- 4 CPU cores
- 20GB free disk space
