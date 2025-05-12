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
GREY="\033[90m"

# Banner function
print_banner() {
    echo -e "${BOLD}${BLUE}"
    echo "📊 =============================================== 📊"
    echo "       🔍 DATA PARK - Infrastructure Status 🔍      "
    echo "📊 =============================================== 📊"
    echo -e "${RESET}"
}

# Function for section headers
section_header() {
    echo -e "\n${BOLD}${CYAN}$1${RESET}"
    echo -e "${CYAN}${2:-===========================================}${RESET}"
}

# Function for component status
component_status() {
    local component=$1
    local emoji=$2
    local namespace="data-park"
    
    echo -e "${BOLD}${BLUE}${emoji} ${component}:${RESET}"
    
    # Check pods
    echo -e "${YELLOW}Pods:${RESET}"
    pod_status=$(kubectl get pods -n $namespace -l app=$component -o wide 2>/dev/null)
    if [ $? -eq 0 ] && [ -n "$pod_status" ]; then
        echo "$pod_status" | while read line; do
            if echo "$line" | grep -q "Running"; then
                echo -e "${GREEN}  $line${RESET}"
            elif echo "$line" | grep -q "ContainerCreating\|PodInitializing"; then
                echo -e "${YELLOW}  $line${RESET}"
            elif echo "$line" | grep -q "NAME"; then
                echo -e "${BOLD}  $line${RESET}"
            else
                echo -e "${RED}  $line${RESET}"
            fi
        done
    else
        echo -e "${GREY}  No pods found for $component${RESET}"
    fi
    
    # Check services
    echo -e "${YELLOW}Services:${RESET}"
    service_status=$(kubectl get services -n $namespace -l app=$component 2>/dev/null)
    if [ $? -eq 0 ] && [ -n "$service_status" ]; then
        echo "$service_status" | while read line; do
            if echo "$line" | grep -q "NAME"; then
                echo -e "${BOLD}  $line${RESET}"
            else
                echo -e "${CYAN}  $line${RESET}"
            fi
        done
    else
        echo -e "${GREY}  No services found for $component${RESET}"
    fi
    
    echo ""
}

# Function to check if kubectl exists
check_kubectl() {
    if ! command -v kubectl &> /dev/null; then
        echo -e "${RED}❌ kubectl not found. Please install kubectl.${RESET}"
        exit 1
    fi
    
    if ! kubectl cluster-info &>/dev/null; then
        echo -e "${RED}❌ Cannot connect to Kubernetes cluster. Is it running?${RESET}"
        exit 1
    fi
}

# Main execution
print_banner
check_kubectl

# Check namespace
section_header "🌍 Namespace Status"
namespace_status=$(kubectl get namespace data-park 2>/dev/null)
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ data-park namespace exists${RESET}"
    echo "$namespace_status" | while read line; do
        if echo "$line" | grep -q "NAME"; then
            echo -e "${BOLD}$line${RESET}"
        else
            echo -e "${CYAN}$line${RESET}"
        fi
    done
else
    echo -e "${RED}❌ data-park namespace does not exist${RESET}"
    exit 1
fi

# Component statuses
section_header "🧩 Components Status"

# PostgreSQL
component_status "postgres" "🐘"

# Zookeeper
component_status "zookeeper" "🔱"

# Kafka
component_status "kafka" "📨"

# Spark Master
component_status "spark-master" "⚡"

# Spark Worker
component_status "spark-worker" "🔥"

# Spark History Server
component_status "spark-history-server" "📜"

# Redis
component_status "redis" "🔄"

# Airflow Webserver
component_status "airflow-webserver" "🖥️"

# Airflow Scheduler
component_status "airflow-scheduler" "⏰"

# Airflow Worker
component_status "airflow-worker" "👷"

# Jupyter Notebook
component_status "jupyter-notebook" "📓"

# PersistentVolumeClaims
section_header "💾 Persistent Volume Claims"
pvc_status=$(kubectl get pvc -n data-park 2>/dev/null)
if [ $? -eq 0 ] && [ -n "$pvc_status" ]; then
    echo "$pvc_status" | while read line; do
        if echo "$line" | grep -q "NAME"; then
            echo -e "${BOLD}$line${RESET}"
        elif echo "$line" | grep -q "Bound"; then
            echo -e "${GREEN}$line${RESET}"
        elif echo "$line" | grep -q "Pending"; then
            echo -e "${YELLOW}$line${RESET}"
        else
            echo -e "${RED}$line${RESET}"
        fi
    done
else
    echo -e "${GREY}No PVCs found${RESET}"
fi

# ConfigMaps
section_header "⚙️ ConfigMaps"
kubectl get configmaps -n data-park 2>/dev/null | head -10

# Secrets
section_header "🔒 Secrets"
kubectl get secrets -n data-park 2>/dev/null | head -10

# Network Policies
section_header "🔌 Network Policies"
kubectl get networkpolicies -n data-park 2>/dev/null

# Ingress
section_header "🚪 Ingress"
ingress_status=$(kubectl get ingress -n data-park 2>/dev/null)
if [ $? -eq 0 ] && [ -n "$ingress_status" ]; then
    echo "$ingress_status" | while read line; do
        if echo "$line" | grep -q "NAME"; then
            echo -e "${BOLD}$line${RESET}"
        else
            echo -e "${CYAN}$line${RESET}"
        fi
    done
else
    echo -e "${GREY}No Ingress resources found${RESET}"
fi

# Node resources
section_header "🖥️ Node Resources"
node_status=$(kubectl top nodes 2>/dev/null)
if [ $? -eq 0 ] && [ -n "$node_status" ]; then
    echo "$node_status" | while read line; do
        if echo "$line" | grep -q "NAME"; then
            echo -e "${BOLD}$line${RESET}"
        else
            echo -e "${MAGENTA}$line${RESET}"
        fi
    done
else
    echo -e "${GREY}Resource metrics not available${RESET}"
fi

# Access Information
section_header "🔗 Access Information" "-----------------------------------"
echo -e "${BOLD}${YELLOW}📌 Service Access URLs:${RESET}"
echo -e "${CYAN}🔸 Spark UI:${RESET} http://data-park.local/spark"
echo -e "${CYAN}🔸 Spark History:${RESET} http://data-park.local/history"
echo -e "${CYAN}🔸 Airflow:${RESET} http://data-park.local/airflow"
echo -e "${CYAN}🔸 Jupyter:${RESET} http://data-park.local/jupyter"

# Port forwarding information
section_header "📡 Port Forwarding Commands" "-----------------------------------"
echo -e "${YELLOW}To access services directly (if ingress is not set up):${RESET}"
echo -e "${CYAN}kubectl port-forward -n data-park svc/spark-master 8080:8080${RESET}"
echo -e "${CYAN}kubectl port-forward -n data-park svc/spark-history-server 18080:18080${RESET}"
echo -e "${CYAN}kubectl port-forward -n data-park svc/airflow-webserver 8081:8080${RESET}"
echo -e "${CYAN}kubectl port-forward -n data-park svc/jupyter-notebook 8888:8888${RESET}"

echo -e "\n${BOLD}${GREEN}🎉 Status check complete! 🎉${RESET}\n"
