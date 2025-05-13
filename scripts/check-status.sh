#!/bin/bash

# Define color codes
GREEN="\033[0;32m"
RED="\033[0;31m"
YELLOW="\033[0;33m"
BLUE="\033[0;34m"
NC="\033[0m" # No Color

echo -e "${BLUE}===== Checking Pod Status =====${NC}"
kubectl get pods -n data-park

echo -e "\n${BLUE}===== Checking Services =====${NC}"
kubectl get svc -n data-park

echo -e "\n${BLUE}===== Checking Ingress =====${NC}"
kubectl get ingress -n data-park

echo -e "\n${BLUE}===== Checking Ingress Controller =====${NC}"
if kubectl get ns | grep -q "ingress"; then
  INGRESS_NS=$(kubectl get ns | grep ingress | awk '{print $1}')
  echo -e "${YELLOW}Ingress namespace: $INGRESS_NS${NC}"
  kubectl get pods -n $INGRESS_NS
  kubectl get svc -n $INGRESS_NS
else
  echo -e "${RED}No ingress namespace found${NC}"
fi
