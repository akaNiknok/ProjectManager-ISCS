# Building the docker image and pushing to Docker Hub

To build the docker image run:

```bash
docker build -t <username>/projectmanager:<version> .
```

To test if the docker image is working:

```bash
docker run -p 4000:8000 <username>/projectmanager:<version>
```

Open a web browser and go to `localhost:4000` to verify that the app is working.

To push the image to Docker Hub run:

```bash
docker push <username>/projectmanager:<version>
```
# Creating a Kubernetes Cluster

Follow these steps to create a Kubernetes cluster in the Google Cloud Console:

1. Navigate to Kubernetes Engine > Clusters in the Google Cloud Console.
2. Click Create and select SWITCH TO STANDARD CLUSTER.
3. Enter my-cluster as the cluster name.
4. For Location type, select Regional.
5. Choose us-central1-f as the region.
6. In the left pane, click Node Pools and select default-pool.
7. Set the Number of nodes to 3.
8. In the left pane, click Networking under Cluster.
9. Ensure Enable authorized networks is not selected.
10. Check the box for Override control plane’s default private endpoint subnet.
11. Set the Private endpoint subnet to default.
12. Click Create to finalize the cluster setup.

Reviewing Cluster Details

To review the details of your cluster, use the following command in the Cloud Shell:
gcloud container clusters describe my-cluster --region us-central1-f

# Kubernetes Manifests for Deployment

This repository contains Kubernetes manifest files for deploying the `my-app` application.

## Directory Structure

```
kubernetes-manifests/
├── deployment.yaml
├── service.yaml
├── ingress.yaml
├── autoscale.yaml
├── pvc.yaml
```

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

```bash
kubectl apply -f deployment.yaml
kubectl get pods
```

## Creating and Deploying the `service.yaml` File

```yaml
apiVersion: v1
kind: Service
metadata:
  name: my-app-service
spec:
  type: LoadBalancer
  selector:
    app: my-app
  ports:
    - protocol: TCP
      port: 80
      targetPort: 8000
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
              number: 80
```
To deploy the application using the ingress.yaml file:

```bash
kubectl apply -f ingress.yaml
```

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

```bash
kubectl apply -f autoscale.yaml
```

## Accessing the application

Once all the YAML files have been applied, to recap:

```bash
kubectl apply -f deployment.yaml

kubectl apply -f service.yaml

kubectl apply -f ingress.yaml

kubectl apply -f autoscale.yaml
```

Verify the deployment:

```bash
kubectl get pods

kubectl get services

kubectl get ingress
kubectl get hpa
```

```
Check the service to access the external IP:
```bash
kubectl get svc
```

Type the external IP into your browser