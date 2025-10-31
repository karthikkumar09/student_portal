# Deploy Student Portal to Kubernetes
# Run this from the student-portal root directory

Write-Host "Deploying Student Portal to Kubernetes..." -ForegroundColor Green

# Check if kubectl is available
try {
    kubectl version --client --short 2>$null
} catch {
    Write-Host "Error: kubectl is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Please enable Kubernetes in Docker Desktop Settings" -ForegroundColor Yellow
    exit 1
}

# Check if k8s directory exists
if (-Not (Test-Path "./k8s")) {
    Write-Host "Error: k8s directory not found!" -ForegroundColor Red
    Write-Host "Make sure you're in the student-portal root directory" -ForegroundColor Yellow
    exit 1
}

Write-Host ""
Write-Host "Step 1: Creating namespace..." -ForegroundColor Cyan
kubectl apply -f k8s/00-namespace.yaml

Write-Host ""
Write-Host "Step 2: Creating ConfigMap..." -ForegroundColor Cyan
kubectl apply -f k8s/01-configmap.yaml

Write-Host ""
Write-Host "Step 3: Creating Secrets..." -ForegroundColor Cyan
kubectl apply -f k8s/02-secret.yaml

Write-Host ""
Write-Host "Step 4: Deploying MongoDB..." -ForegroundColor Cyan
kubectl apply -f k8s/03-mongodb.yaml

Write-Host ""
Write-Host "Waiting for MongoDB to be ready (this may take 1-2 minutes)..." -ForegroundColor Yellow
kubectl wait --for=condition=ready pod -l app=mongodb -n student-portal --timeout=300s

Write-Host ""
Write-Host "Step 5: Deploying Student Service..." -ForegroundColor Cyan
kubectl apply -f k8s/04-student-service.yaml

Write-Host ""
Write-Host "Step 6: Deploying Course Service..." -ForegroundColor Cyan
kubectl apply -f k8s/05-course-service.yaml

Write-Host ""
Write-Host "Step 7: Deploying Enrollment Service..." -ForegroundColor Cyan
kubectl apply -f k8s/06-enrollment-service.yaml

Write-Host ""
Write-Host "Step 8: Deploying Frontend..." -ForegroundColor Cyan
kubectl apply -f k8s/07-frontend.yaml

Write-Host ""
Write-Host "Step 9: Creating Admin User..." -ForegroundColor Cyan
kubectl apply -f k8s/09-init-admin-job.yaml

Write-Host ""
Write-Host "Deployment complete!" -ForegroundColor Green

Write-Host ""
Write-Host "Waiting for all pods to be ready..." -ForegroundColor Yellow
Start-Sleep -Seconds 10

Write-Host ""
Write-Host "Checking deployment status..." -ForegroundColor Cyan
kubectl get pods -n student-portal

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "    Student Portal Deployed!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green

Write-Host ""
Write-Host "To access the application, run:" -ForegroundColor Yellow
Write-Host "  kubectl port-forward -n student-portal svc/frontend 8080:80" -ForegroundColor White
Write-Host ""
Write-Host "Then open: http://localhost:8080" -ForegroundColor Cyan

Write-Host ""
Write-Host "Default Admin Credentials:" -ForegroundColor Yellow
Write-Host "  Email: admin@example.com" -ForegroundColor White
Write-Host "  Password: admin123" -ForegroundColor White

Write-Host ""
Write-Host "Useful commands:" -ForegroundColor Yellow
Write-Host "  View pods:        kubectl get pods -n student-portal" -ForegroundColor White
Write-Host "  View services:    kubectl get svc -n student-portal" -ForegroundColor White
Write-Host "  View logs:        kubectl logs -n student-portal <pod-name>" -ForegroundColor White
Write-Host "  Check admin job:  kubectl logs -n student-portal job/init-admin" -ForegroundColor White