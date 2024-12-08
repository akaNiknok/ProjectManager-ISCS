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

```
To deploy the application using the deployment.yaml file:


kubectl apply -f deployment.yaml
kubectl get pods

## Creating and Deploying the `service.yaml` File

```yaml
apiVersion: v1
kind: Service
metadata:
  name: my-app-service
spec:
  selector:
    app: my-app
  ports:
    - protocol: TCP
      port: 8000
      targetPort: 8000
  type: ClusterIP
```
To deploy the application using the service.yaml file:

kubectl apply -f service.yaml


## Creating and Deploying the `ingress.yaml` File

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: my-app-ingress
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
spec:
  rules:
  - host: localhost
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: my-app-service
            port:
              number: 8000
```
To deploy the application using the ingress.yaml file:

kubectl apply -f ingress.yaml

## Creating and Deploying the `autoscale.yaml` File

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: my-app-autoscaler
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: my-app
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 50
```

To deploy the application using the autoscale.yaml file:

kubectl apply -f autoscale.yaml
