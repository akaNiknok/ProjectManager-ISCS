# Kubernetes Manifests for Deployment

This repository contains Kubernetes manifest files for deploying the `my-app` application.

## Directory Structure
kubernetes-manifests/ ├── deployment.yaml ├── service.yaml ├── ingress.yaml ├── autoscale.yaml ├── pvc.yaml


## Creating and Deploying the `deployment.yaml` File

The `deployment.yaml` file defines the Kubernetes deployment for the `my-app` application.

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-app
  labels:
    app: my-app
spec:
  replicas: 3
  selector:
    matchLabels:
      app: my-app
  template:
    metadata:
      labels:
        app: my-app
    spec:
      containers:
      - name: my-app
        image: nolene6988/projectmanager:1.3
        ports:
        - containerPort: 8000
        env:
        - name: ENV_VAR_NAME
          value: "value"  # Add any required environment variables
