# Data Park Setup Guide

This guide provides instructions for setting up the Data Park environment on your local machine.

## Prerequisites

Before you begin, ensure you have the following installed:

- **Docker** (version 20.10 or later)
- **Kubernetes cluster** - One of the following:
  - Minikube (version 1.25 or later)
  - k3s (version 1.21 or later)
  - Docker Desktop with Kubernetes enabled
  - Kind (Kubernetes IN Docker)
  - Microk8s
- **kubectl** (compatible with your Kubernetes version)
- **Git** (version 2.30 or later)
- At least 8GB RAM and 4 CPU cores available
- At least 20GB free disk space

## Setup Steps

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/data_park.git
cd data_park
```

### 2. Deploy the Infrastructure

We provide a deployment script that will set up all components in the correct order:

```bash
# Make the script executable
chmod +x scripts/setup.sh

# Run the setup script
./scripts/setup.sh
```

Alternatively, you can deploy components manually in the following order:

```bash
# 1. Deploy common resources (namespace, storage class, etc.)
kubectl apply -f infra/common/

# 2. Deploy PostgreSQL
kubectl apply -f infra/postgres/

# 3. Deploy Kafka and Zookeeper
kubectl apply -f infra/kafka/

# 4. Deploy Spark
kubectl apply -f infra/spark/

# 5. Deploy Airflow
kubectl apply -f infra/airflow/

# 6. Deploy Jupyter
kubectl apply -f infra/jupyter/
```

### 3. Verify the Deployment

Check that all pods are running:

```bash
kubectl get pods -n data-park
```

All pods should eventually reach the `Running` state. The initial deployment may take a few minutes as container images are downloaded and initialized.

### 4. Access the Services

After successful deployment, you can access the services directly via NodePort:

- **Spark Master UI**: http://localhost:30080
- **Spark History Server**: http://localhost:30081
- **Airflow UI**: http://localhost:30082
  - Username: `admin`
  - Password: `admin`
- **Jupyter Notebook**: http://localhost:30083

### 5. Default Credentials

- **PostgreSQL**:
  - Main user: `postgres`
  - Password: `postgrespass`
  - Host: `postgres.data-park.svc.cluster.local` (from inside Kubernetes)
  - Host: `localhost` (with port forwarding)
  - Port: `5432`

### 6. Troubleshooting

#### Pods Not Starting

If pods are stuck in `Pending` or `ContainerCreating` state:

```bash
# Check events
kubectl get events -n data-park

# Check pod details
kubectl describe pod [pod-name] -n data-park
```

Common issues:
- Insufficient resources (memory, CPU)
- PersistentVolumeClaim not bound
- Image pull failures

#### Connectivity Issues

If services cannot communicate with each other:

```bash
# Check service endpoints
kubectl get endpoints -n data-park

# Test connectivity from a pod
kubectl exec -it [pod-name] -n data-park -- curl [service-name]:[port]
```

### 7. Cleanup

To remove the entire Data Park infrastructure:

```bash
# Make the script executable
chmod +x scripts/cleanup.sh

# Run the cleanup script
./scripts/cleanup.sh
```

## Next Steps

After successful setup, you can:

1. Explore the sample notebooks in Jupyter
2. Check out the example Airflow DAGs
3. Execute some batch and streaming examples

See the [Architecture Documentation](../architecture/README.md) for more details on how the components interact with each other.
