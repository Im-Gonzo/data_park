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
    echo -e "${BOLD}${RED}"
    echo "🧹 =============================================== 🧹"
    echo "       🗑️  DATA PARK - Cleanup Infrastructure 🗑️    "
    echo "🧹 =============================================== 🧹"
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

# Function to ask for confirmation
confirm() {
    read -p "$(echo -e ${YELLOW}⚠️  $1 [y/N]: ${RESET})" response
    case "$response" in
        [yY][eE][sS]|[yY]) 
            return 0
            ;;
        *)
            return 1
            ;;
    esac
}

# Function to check if kubectl exists
check_kubectl() {
    if ! command -v kubectl &> /dev/null; then
        error_message "kubectl not found. Please install kubectl."
        exit 1
    fi
}

# Function to remove a component
remove_component() {
    local component=$1
    local emoji=$2
    
    progress_message "${emoji} Removing ${component}..."
    kubectl delete -f "../infra/${component}/" --ignore-not-found
    
    if [ $? -eq 0 ]; then
        success_message "${component} removed successfully!"
    else
        error_message "Failed to remove ${component}!"
    fi
}

# Main execution
print_banner
check_kubectl

echo -e "\n${BOLD}${RED}🚨 Starting Cleanup Process 🚨${RESET}\n"

if ! confirm "This will remove all Data Park infrastructure. Continue?"; then
    info_message "Cleanup cancelled."
    exit 0
fi

# Remove components in reverse order
remove_component "jupyter" "📓"
remove_component "airflow" "🔄"
remove_component "spark" "⚡"
remove_component "kafka" "📨"
remove_component "postgres" "🐘"

# Remove common resources
progress_message "🌐 Removing common resources..."
kubectl delete -f "../infra/common/" --ignore-not-found
if [ $? -eq 0 ]; then
    success_message "Common resources removed successfully!"
else
    error_message "Failed to remove common resources!"
fi

# Check if namespace still exists
if kubectl get namespace data-park &>/dev/null; then
    warning_message "Namespace data-park still exists."
    
    if confirm "Do you want to delete the namespace and all its resources?"; then
        kubectl delete namespace data-park
        if [ $? -eq 0 ]; then
            success_message "Namespace data-park deleted successfully!"
        else
            error_message "Failed to delete namespace data-park!"
        fi
    fi
else
    success_message "Namespace data-park no longer exists."
fi

echo -e "\n${BOLD}${GREEN}🎉 Cleanup completed! 🎉${RESET}\n"
