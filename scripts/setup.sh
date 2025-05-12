#!/bin/bash

# Define color codes and styles
BOLD="\033[1m"
RESET="\033[0m"
GREEN="\033[32m"
YELLOW="\033[33m"
BLUE="\033[34m"
MAGENTA="\033[35m"
CYAN="\033[36m"
RED="\033[31m"

# Banner function
print_banner() {
    echo -e "${BOLD}${BLUE}"
    echo "🌟 =============================================== 🌟"
    echo "       🚀 DATA PARK - Setup Environment 🚀        "
    echo "🌟 =============================================== 🌟"
    echo -e "${RESET}"
}

# Success message function
success_message() {
    echo -e "${GREEN}✅ $1${RESET}"
}

# Error message function
error_message() {
    echo -e "${RED}❌ $1${RESET}"
}

# Info message function
info_message() {
    echo -e "${CYAN}ℹ️  $1${RESET}"
}

# Warning message function
warning_message() {
    echo -e "${YELLOW}⚠️  $1${RESET}"
}

# Progress message function
progress_message() {
    echo -e "${MAGENTA}🔄 $1${RESET}"
}

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to check dependencies
check_dependencies() {
    progress_message "Checking dependencies..."
    
    if ! command_exists kubectl; then
        error_message "kubectl not found. Please install kubectl."
        exit 1
    else
        success_message "kubectl found"
    fi
}

# Function to check if Kubernetes is running
check_kubernetes() {
    progress_message "Checking Kubernetes connection..."
    
    if ! kubectl cluster-info &>/dev/null; then
        error_message "Cannot connect to Kubernetes cluster. Is it running?"
        exit 1
    else
        success_message "Connected to Kubernetes cluster"
    fi
}

# Function to create namespace
create_namespace() {
    progress_message "Creating data-park namespace..."
    
    if kubectl get namespace data-park &>/dev/null; then
        info_message "Namespace data-park already exists"
    else
        kubectl apply -f ../infra/common/namespace.yaml
        if [ $? -eq 0 ]; then
            success_message "Namespace data-park created"
        else
            error_message "Failed to create namespace"
            exit 1
        fi
    fi
}

# Function to deploy infrastructure components
deploy_component() {
    local component=$1
    local emoji=$2
    
    progress_message "${emoji} Deploying ${component}..."
    
    kubectl apply -f ../infra/${component}/
    if [ $? -eq 0 ]; then
        success_message "${component} deployed successfully"
    else
        error_message "Failed to deploy ${component}"
        return 1
    fi
}

# Function to wait for pod readiness
wait_for_pods() {
    local component=$1
    local timeout=$2
    
    progress_message "Waiting for ${component} pods to be ready (timeout: ${timeout}s)..."
    
    kubectl wait --namespace data-park --for=condition=ready pod --selector=app=${component} --timeout=${timeout}s
    if [ $? -eq 0 ]; then
        success_message "${component} pods are ready"
    else
        warning_message "Timeout waiting for ${component} pods"
    fi
}

# Main execution
print_banner
check_dependencies
check_kubernetes

echo -e "\n${BOLD}${CYAN}🏁 Starting Deployment Process 🏁${RESET}\n"

# Create namespace and common resources
create_namespace
progress_message "🌐 Deploying common resources..."
kubectl apply -f ../infra/common/
if [ $? -eq 0 ]; then
    success_message "Common resources deployed successfully"
else
    error_message "Failed to deploy common resources"
    exit 1
fi

# Deploy PostgreSQL (other components depend on it)
deploy_component "postgres" "🐘" || exit 1
wait_for_pods "postgres" 120

# Deploy Kafka and Zookeeper
deploy_component "kafka" "📨" || exit 1
wait_for_pods "zookeeper" 120
wait_for_pods "kafka" 180

# Deploy Spark
deploy_component "spark" "⚡" || exit 1
wait_for_pods "spark-master" 120
wait_for_pods "spark-worker" 120
wait_for_pods "spark-history-server" 120

# Deploy Airflow
deploy_component "airflow" "🔄" || exit 1
wait_for_pods "redis" 120
wait_for_pods "airflow-webserver" 300
wait_for_pods "airflow-scheduler" 300
wait_for_pods "airflow-worker" 300

# Deploy Jupyter
deploy_component "jupyter" "📓" || exit 1
wait_for_pods "jupyter-notebook" 180

echo -e "\n${BOLD}${GREEN}🎉 Data Park Environment Setup Complete! 🎉${RESET}"
echo -e "\n${BOLD}${CYAN}📊 Access the services at:${RESET}"
echo -e "${YELLOW}📌 Spark UI:${RESET} http://data-park.local/spark"
echo -e "${YELLOW}📌 Spark History:${RESET} http://data-park.local/history"
echo -e "${YELLOW}📌 Airflow:${RESET} http://data-park.local/airflow"
echo -e "${YELLOW}📌 Jupyter:${RESET} http://data-park.local/jupyter"

echo -e "\n${CYAN}To add data-park.local to your hosts file:${RESET}"
echo -e "${YELLOW}sudo echo \"127.0.0.1 data-park.local\" >> /etc/hosts${RESET}"

echo -e "\n${BOLD}${CYAN}💡 Remember to forward ports if using minikube:${RESET}"
echo -e "${YELLOW}kubectl port-forward -n data-park svc/spark-master 8080:8080 &${RESET}"
echo -e "${YELLOW}kubectl port-forward -n data-park svc/airflow-webserver 8081:8080 &${RESET}"
echo -e "${YELLOW}kubectl port-forward -n data-park svc/jupyter-notebook 8888:8888 &${RESET}"

echo -e "\n${BOLD}${GREEN}Happy data engineering! 🚀${RESET}\n"
