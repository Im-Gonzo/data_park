# Data Park

A comprehensive local training environment for data engineering with Apache Spark, Kafka, PostgreSQL, and Airflow.

## Overview

This repository provides infrastructure and code examples for advanced data engineering training, focusing on:

- Batch processing with Apache Spark
- Stream processing with Kafka and Spark Streaming
- ETL and ELT workflows
- Data pipeline orchestration with Airflow
- Data generation for realistic scenarios

## Repository Structure

```
data_park/
├── k8s/                              # Kubernetes manifests
│   ├── spark/                        # Spark operator and deployments
│   ├── kafka/                        # Kafka and Zookeeper
│   ├── postgres/                     # PostgreSQL database
│   ├── airflow/                      # Airflow deployment
│   └── jupyter/                      # Jupyter notebook server
│
├── configs/                          # Configuration files
│   ├── spark/                        # Spark configurations
│   ├── kafka/                        # Kafka configurations
│   ├── airflow/                      # Airflow DAGs and configs
│   └── postgres/                     # PostgreSQL init scripts and configs
│
├── python/                           # Python code examples
│   ├── batch/                        # Batch processing examples
│   ├── streaming/                    # Streaming examples
│   ├── etl/                          # ETL examples
│   ├── elt/                          # ELT examples
│   ├── airflow/                      # Airflow DAGs
│   └── generators/                   # Data generators
│       ├── kafka/                    # Kafka data generators
│       └── postgres/                 # PostgreSQL data generators
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
    ├── deploy.sh                     # Deployment to K8s
    └── cleanup.sh                    # Environment cleanup
```

## Getting Started

1. See the [setup guide](docs/setup/README.md) for instructions on deploying the infrastructure.
2. Check the [architecture documentation](docs/architecture/README.md) for an overview of the system components.
3. Follow the [tutorials](docs/tutorials/README.md) to learn about the various data engineering patterns.

## Core Technologies

- **Apache Spark**: Unified analytics engine for large-scale data processing
- **Apache Kafka**: Distributed event streaming platform
- **PostgreSQL**: Advanced open-source relational database
- **Apache Airflow**: Platform to programmatically author, schedule, and monitor workflows
- **Jupyter Notebook**: Web-based interactive development environment

## License

MIT
