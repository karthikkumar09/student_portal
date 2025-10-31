# Build all Docker images for Student Portal
# Run this from the student-portal root directory

Write-Host "Building Student Portal Docker Images..." -ForegroundColor Green

# Set registry prefix (change this if pushing to a registry)
$REGISTRY = "student-portal"

Write-Host ""
Write-Host "Building Student Service..." -ForegroundColor Cyan
docker build -t ${REGISTRY}/student-service:latest ./backend/student-service

Write-Host ""
Write-Host "Building Course Service..." -ForegroundColor Cyan
docker build -t ${REGISTRY}/course-service:latest ./backend/course-service

Write-Host ""
Write-Host "Building Enrollment Service..." -ForegroundColor Cyan
docker build -t ${REGISTRY}/enrollment-service:latest ./backend/enrollment-service

Write-Host ""
Write-Host "Building Frontend..." -ForegroundColor Cyan
docker build -t ${REGISTRY}/frontend:latest --build-arg VITE_STUDENT_SERVICE_URL=http://localhost:8001 --build-arg VITE_COURSE_SERVICE_URL=http://localhost:8000 --build-arg VITE_ENROLLMENT_SERVICE_URL=http://localhost:8002 ./frontend

Write-Host ""
Write-Host "All images built successfully!" -ForegroundColor Green
Write-Host ""
Write-Host "Verifying images..." -ForegroundColor Yellow
docker images | Select-String "student-portal"

Write-Host ""
Write-Host "Images are ready for Kubernetes deployment!" -ForegroundColor Green