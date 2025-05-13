# Data Park

A comprehensive local training environment for data engineering with Apache Spark, Kafka, PostgreSQL, and Airflow.

## Overview

This repository provides infrastructure and code examples for advanced data engineering training, focusing on:

- Batch processing with Apache Spark
- Stream processing with Kafka and Spark Streaming
- ETL and ELT workflows
- Data pipeline orchestration with Airflow
- Data generation for realistic scenarios

## Accessing Services

Services are directly accessible via NodePort:
- **Spark Master UI**: http://localhost:30080
- **Spark History Server**: http://localhost:30081
- **Airflow UI**: http://localhost:30082
  - Username: `admin`
  - Password: `admin`
- **Jupyter Notebook**: http://localhost:30083

## Repository Structure

```
data_park/
├── infra/                            # Kubernetes manifests
│   ├── spark/                        # Spark deployments
│   ├── kafka/                        # Kafka and Zookeeper
│   ├── postgres/                     # PostgreSQL database
│   ├── airflow/                      # Airflow deployment
│   ├── jupyter/                      # Jupyter notebook server
│   └── common/                       # Common resources (namespace, storage)
│
├── python/                           # Python code examples
│   ├── batch/                        # Batch processing examples
│   ├── streaming/                    # Streaming examples
│   ├── etl/                          # ETL examples
│   ├── elt/                          # ELT examples
│   ├── airflow/                      # Airflow DAGs
│   └── generators/                   # Data generators
│
├── scala/                            # Scala code examples
│   ├── batch/                        # Batch processing examples
│   ├── streaming/                    # Streaming examples
│   ├── etl/                          # ETL examples
│   └── elt/                          # ELT examples
│
├── data/                             # Sample datasets
│   ├── raw/                          # Raw data samples
│   └── processed/                    # Processed data examples
│
├── docs/                             # Documentation
│   ├── setup/                        # Setup guides
│   ├── tutorials/                    # Step-by-step tutorials
│   └── architecture/                 # Architecture diagrams
│
└── scripts/                          # Utility scripts
    ├── setup.sh                      # Environment setup
    ├── status.sh                     # Check service status
    └── cleanup.sh                    # Environment cleanup
```

## Getting Started

1. Run the setup script to deploy the infrastructure:
   ```bash
   cd scripts
   ./setup.sh
   ```

2. Access the services at the URLs listed above.

3. Check the [documentation](docs/) for more details on how to use the platform.

## Core Technologies

- **Apache Spark**: Unified analytics engine for large-scale data processing
- **Apache Kafka**: Distributed event streaming platform
- **PostgreSQL**: Advanced open-source relational database
- **Apache Airflow**: Platform to programmatically author, schedule, and monitor workflows
- **Jupyter Notebook**: Web-based interactive development environment

## License

MIT
