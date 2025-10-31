# Kubernetes Deployment Guide

This guide explains how to deploy the Student Portal application to Kubernetes.

## Prerequisites

### Required Tools
- **Docker** (for building images)
- **kubectl** (Kubernetes CLI)
- **Kubernetes cluster** (one of):
  - Minikube (local development)
  - Docker Desktop with Kubernetes
  - Cloud provider (GKE, EKS, AKS)
  - kind (Kubernetes in Docker)

### Install kubectl
```bash
# macOS
brew install kubectl

# Windows (using Chocolatey)
choco install kubernetes-cli

# Linux
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
chmod +x kubectl
sudo mv kubectl /usr/local/bin/
```

### Setup Local Kubernetes (Choose One)

#### Option 1: Minikube
```bash
# Install Minikube
# macOS
brew install minikube

# Windows
choco install minikube

# Linux
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
sudo install minikube-linux-amd64 /usr/local/bin/minikube

# Start Minikube
minikube start --driver=docker --memory=4096 --cpus=2

# Enable ingress addon (optional)
minikube addons enable ingress
```

#### Option 2: Docker Desktop
1. Open Docker Desktop
2. Go to Settings → Kubernetes
3. Check "Enable Kubernetes"
4. Click "Apply & Restart"

#### Option 3: kind
```bash
# Install kind
brew install kind  # macOS
# or
curl -Lo ./kind https://kind.sigs.k8s.io/dl/v0.20.0/kind-linux-amd64
chmod +x ./kind
sudo mv ./kind /usr/local/bin/kind

# Create cluster
kind create cluster --name student-portal
```

## Deployment Steps

### Step 1: Build Docker Images

```bash
# Set your registry (optional)
export DOCKER_REGISTRY=student-portal

# Build all images
./build-images.sh

# Verify images are built
docker images | grep student-portal
```

### Step 2: Load Images to Kubernetes (Local Only)

If using Minikube:
```bash
minikube image load student-portal/student-service:latest
minikube image load student-portal/course-service:latest
minikube image load student-portal/enrollment-service:latest
minikube image load student-portal/frontend:latest
```

If using kind:
```bash
kind load docker-image student-portal/student-service:latest --name student-portal
kind load docker-image student-portal/course-service:latest --name student-portal
kind load docker-image student-portal/enrollment-service:latest --name student-portal
kind load docker-image student-portal/frontend:latest --name student-portal
```

If using Docker Desktop, images are already available.

### Step 3: Deploy to Kubernetes

```bash
# Deploy everything
./deploy-k8s.sh

# Or deploy manually step by step:
kubectl apply -f k8s/00-namespace.yaml
kubectl apply -f k8s/01-configmap.yaml
kubectl apply -f k8s/02-secret.yaml
kubectl apply -f k8s/03-mongodb.yaml
kubectl wait --for=condition=ready pod -l app=mongodb -n student-portal --timeout=300s
kubectl apply -f k8s/04-student-service.yaml
kubectl apply -f k8s/05-course-service.yaml
kubectl apply -f k8s/06-enrollment-service.yaml
kubectl apply -f k8s/07-frontend.yaml
kubectl apply -f k8s/09-init-admin-job.yaml
```

### Step 4: Verify Deployment

```bash
# Check all pods are running
kubectl get pods -n student-portal

# Expected output:
# NAME                                  READY   STATUS    RESTARTS   AGE
# course-service-xxx                    1/1     Running   0          2m
# enrollment-service-xxx                1/1     Running   0          2m
# frontend-xxx                          1/1     Running   0          2m
# mongodb-0                             1/1     Running   0          3m
# student-service-xxx                   1/1     Running   0          2m

# Check services
kubectl get svc -n student-portal

# Check logs if something fails
kubectl logs -n student-portal -l app=student-service
kubectl logs -n student-portal job/init-admin
```

## Accessing the Application

### Method 1: LoadBalancer (Cloud Providers)

```bash
# Get external IP
kubectl get svc frontend -n student-portal

# Wait for EXTERNAL-IP to show (might take a few minutes)
# Access: http://<EXTERNAL-IP>
```

### Method 2: Port Forward (Local Development)

```bash
# Forward frontend port
kubectl port-forward -n student-portal svc/frontend 8080:80

# Access: http://localhost:8080
```

### Method 3: Minikube Service

```bash
minikube service frontend -n student-portal
```

### Method 4: Ingress (Recommended for Production)

```bash
# Deploy ingress
kubectl apply -f k8s/08-ingress.yaml

# For Minikube, get IP
minikube ip

# Add to /etc/hosts (Linux/Mac) or C:\Windows\System32\drivers\etc\hosts (Windows)
<MINIKUBE-IP> student-portal.local

# Access: http://student-portal.local
```

## Default Credentials

**Admin Login:**
- Email: admin@example.com
- Password: admin123

Check the init-admin job logs:
```bash
kubectl logs -n student-portal job/init-admin
```

## Scaling

```bash
# Scale services
kubectl scale deployment student-service -n student-portal --replicas=3
kubectl scale deployment course-service -n student-portal --replicas=3
kubectl scale deployment enrollment-service -n student-portal --replicas=3
kubectl scale deployment frontend -n student-portal --replicas=3

# Check status
kubectl get pods -n student-portal
```

## Updating the Application

```bash
# Build new images with version
./build-images.sh v2.0.0

# Update image in deployment
kubectl set image deployment/student-service student-service=student-portal/student-service:v2.0.0 -n student-portal

# Or edit deployment
kubectl edit deployment student-service -n student-portal

# Rollout status
kubectl rollout status deployment/student-service -n student-portal

# Rollback if needed
kubectl rollout undo deployment/student-service -n student-portal
```

## Troubleshooting

### Pods not starting
```bash
# Describe pod to see events
kubectl describe pod <pod-name> -n student-portal

# Check logs
kubectl logs <pod-name> -n student-portal

# Check previous logs if pod restarted
kubectl logs <pod-name> -n student-portal --previous
```

### MongoDB connection issues
```bash
# Check MongoDB is running
kubectl get pods -n student-portal -l app=mongodb

# Test connection from another pod
kubectl run -it --rm debug --image=mongo:7 --restart=Never -n student-portal -- mongosh mongodb://mongodb:27017
```

### Service not accessible
```bash
# Check service endpoints
kubectl get endpoints -n student-portal

# Test service from within cluster
kubectl run -it --rm debug --image=curlimages/curl --restart=Never -n student-portal -- curl http://student-service:8001/health
```

### Image pull errors
```bash
# For local images, ensure imagePullPolicy is set correctly
# Edit deployments:
kubectl edit deployment student-service -n student-portal
# Set: imagePullPolicy: IfNotPresent
```

## Monitoring

### View all resources
```bash
kubectl get all -n student-portal
```

### Watch pod status
```bash
kubectl get pods -n student-portal -w
```

### View events
```bash
kubectl get events -n student-portal --sort-by='.lastTimestamp'
```

### Check resource usage
```bash
kubectl top pods -n student-portal
kubectl top nodes
```

## Cleanup

### Delete everything
```bash
kubectl delete namespace student-portal
```

### Delete specific resources
```bash
kubectl delete -f k8s/
```

### Stop local cluster
```bash
# Minikube
minikube stop
minikube delete

# kind
kind delete cluster --name student-portal
```

## Production Considerations

### 1. Use a Container Registry
```bash
# Tag and push images
docker tag student-portal/student-service:latest your-registry.com/student-service:v1.0.0
docker push your-registry.com/student-service:v1.0.0

# Update k8s deployments with registry URL
# image: your-registry.com/student-service:v1.0.0
```

### 2. Configure Resource Limits
Already included in manifests. Adjust based on your needs:
```yaml
resources:
  requests:
    memory: "128Mi"
    cpu: "100m"
  limits:
    memory: "256Mi"
    cpu: "200m"
```

### 3. Enable HTTPS
```bash
# Install cert-manager
kubectl apply -f https://github.com/cert-manager/cert-manager/releases/download/v1.13.0/cert-manager.yaml

# Update ingress with TLS
# See k8s/08-ingress.yaml and add tls section
```

### 4. Use Persistent Storage
MongoDB already uses PersistentVolumeClaim. Configure StorageClass for your cloud provider.

### 5. Setup Monitoring
```bash
# Install Prometheus & Grafana
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm install prometheus prometheus-community/kube-prometheus-stack -n monitoring --create-namespace
```

### 6. Implement Secrets Management
Use external secrets manager (AWS Secrets Manager, HashiCorp Vault, etc.)

### 7. Configure Network Policies
Add network policies to restrict pod-to-pod communication.

## Architecture

```
                    Internet
                        |
                   LoadBalancer
                        |
                    Frontend (2 replicas)
                        |
            +-----------+-----------+
            |           |           |
      Student      Course    Enrollment
      Service      Service     Service
    (2 replicas) (2 replicas) (2 replicas)
            |           |           |
            +--------MongoDB---------+
                   (StatefulSet)
```

## Next Steps

1. Configure CI/CD pipeline
2. Setup monitoring and alerting
3. Implement backup strategy for MongoDB
4. Configure auto-scaling (HPA)
5. Setup multiple environments (dev, staging, prod)

---

**Need Help?** Check the main README.md or open an issue!
