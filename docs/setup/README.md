# Data Park Setup Guide

This guide provides detailed instructions for setting up the Data Park environment on your local machine.

## Prerequisites

Before you begin, ensure you have the following installed:

- **Docker** (version 20.10 or later)
- **Kubernetes cluster** - One of the following:
  - Minikube (version 1.25 or later)
  - k3s (version 1.21 or later)
  - Docker Desktop with Kubernetes enabled
  - Kind (Kubernetes IN Docker)
- **kubectl** (compatible with your Kubernetes version)
- **Git** (version 2.30 or later)
- **Bash** shell or compatible
- At least 8GB RAM and 4 CPU cores available
- At least 20GB free disk space

## Setup Steps

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/data_park.git
cd data_park
```

### 2. Configure Your Local Environment

#### Set Up Local Domain Resolution

Add the following entry to your hosts file (`/etc/hosts` on Linux/macOS, `C:\Windows\System32\drivers\etc\hosts` on Windows):

```
127.0.0.1 data-park.local
```

#### Configure Kubernetes Ingress Controller

If you're using Minikube, enable the ingress addon:

```bash
minikube addons enable ingress
```

For other Kubernetes distributions, install an ingress controller of your choice (nginx-ingress is recommended).

### 3. Deploy the Infrastructure

We provide a deployment script that will set up all components in the correct order:

```bash
# Make the script executable
chmod +x scripts/deploy.sh

# Run the deployment script
./scripts/deploy.sh
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

### 4. Verify the Deployment

Check that all pods are running:

```bash
kubectl get pods -n data-park
```

All pods should eventually reach the `Running` state. The initial deployment may take a few minutes as container images are downloaded and initialized.

#### Port Forwarding (if not using Ingress)

If you're not using the Ingress setup, you can access the services using port forwarding:

```bash
# Spark UI
kubectl port-forward -n data-park svc/spark-master 8080:8080 &

# Spark History Server
kubectl port-forward -n data-park svc/spark-history-server 18080:18080 &

# Airflow UI
kubectl port-forward -n data-park svc/airflow-webserver 8081:8080 &

# Jupyter Notebook
kubectl port-forward -n data-park svc/jupyter-notebook 8888:8888 &
```

### 5. Access the Services

After successful deployment, you can access the services at the following URLs:

- **Spark Master UI**: http://data-park.local/spark
- **Spark History Server**: http://data-park.local/history
- **Airflow UI**: http://data-park.local/airflow
- **Jupyter Notebook**: http://data-park.local/jupyter

If using port forwarding instead of Ingress:
- **Spark Master UI**: http://localhost:8080
- **Spark History Server**: http://localhost:18080
- **Airflow UI**: http://localhost:8081
- **Jupyter Notebook**: http://localhost:8888

#### Default Credentials

- **Airflow**:
  - Username: `admin`
  - Password: `admin`

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

#### Storage Issues

If persistent volumes are not being provisioned:

```bash
# Check PVC status
kubectl get pvc -n data-park

# Check persistent volumes
kubectl get pv
```

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

To manually cleanup components in reverse order:

```bash
kubectl delete -f infra/jupyter/
kubectl delete -f infra/airflow/
kubectl delete -f infra/spark/
kubectl delete -f infra/kafka/
kubectl delete -f infra/postgres/
kubectl delete -f infra/common/
```

## Next Steps

After successful setup, you can:

1. Explore the sample notebooks in Jupyter
2. Check out the example Airflow DAGs
3. Execute some batch and streaming examples
4. Develop your own data pipelines

See the [Architecture Documentation](../architecture/README.md) for more details on how the components interact with each other.
