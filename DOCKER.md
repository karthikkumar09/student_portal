# Docker Deployment Guide

Complete guide for running Student Portal with Docker and Docker Compose.

## Prerequisites

- **Docker** installed and running
- **Docker Compose** (included with Docker Desktop)

### Install Docker

#### Windows
1. Download [Docker Desktop for Windows](https://www.docker.com/products/docker-desktop/)
2. Install and start Docker Desktop
3. Verify: `docker --version` and `docker-compose --version`

#### macOS
```bash
brew install --cask docker
# Or download from docker.com
```

#### Linux
```bash
# Ubuntu/Debian
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER  # Add user to docker group
newgrp docker  # Activate changes

# Verify
docker --version
docker-compose --version
```

## Quick Start (Easiest Method)

### Option 1: Docker Compose (Recommended)

Run everything with one command:

```bash
# Build and start all services
docker-compose up --build

# Or run in detached mode (background)
docker-compose up -d --build
```

**Access the application:**
- Frontend: http://localhost:80 or http://localhost
- Student Service API: http://localhost:8001/docs
- Course Service API: http://localhost:8000/docs
- Enrollment Service API: http://localhost:8002/docs

**Default credentials:**
- Email: admin@example.com
- Password: admin123

### Option 2: Build and Run Manually

```bash
# Build all images
./build-images.sh

# Start with docker-compose
docker-compose up
```

## Docker Compose Commands

### Start Services
```bash
# Start all services
docker-compose up

# Start in background
docker-compose up -d

# Rebuild and start
docker-compose up --build

# Start specific service
docker-compose up frontend
```

### Stop Services
```bash
# Stop all services
docker-compose down

# Stop and remove volumes (deletes data!)
docker-compose down -v

# Stop specific service
docker-compose stop frontend
```

### View Logs
```bash
# All services
docker-compose logs

# Follow logs (real-time)
docker-compose logs -f

# Specific service
docker-compose logs student-service

# Last 100 lines
docker-compose logs --tail=100 -f
```

### Check Status
```bash
# List running containers
docker-compose ps

# Check specific service
docker-compose ps frontend
```

### Restart Services
```bash
# Restart all
docker-compose restart

# Restart specific service
docker-compose restart course-service
```

### Execute Commands in Container
```bash
# Open shell in container
docker-compose exec student-service bash

# Run one-off command
docker-compose exec student-service python setup_admin.py

# Check MongoDB
docker-compose exec mongodb mongosh
```

## Building Individual Images

### Build All at Once
```bash
./build-images.sh
```

### Build Individually
```bash
# Student Service
docker build -t student-portal/student-service:latest ./backend/student-service

# Course Service
docker build -t student-portal/course-service:latest ./backend/course-service

# Enrollment Service
docker build -t student-portal/enrollment-service:latest ./backend/enrollment-service

# Frontend
docker build -t student-portal/frontend:latest ./frontend
```

### Build with Version Tag
```bash
./build-images.sh v1.0.0
```

## Running Without Docker Compose

If you prefer to run containers manually:

### 1. Create Network
```bash
docker network create student-portal-network
```

### 2. Start MongoDB
```bash
docker run -d \
  --name mongodb \
  --network student-portal-network \
  -p 27017:27017 \
  -v mongodb_data:/data/db \
  mongo:7
```

### 3. Start Backend Services
```bash
# Student Service
docker run -d \
  --name student-service \
  --network student-portal-network \
  -p 8001:8001 \
  -e MONGO_URI=mongodb://mongodb:27017 \
  -e JWT_SECRET_KEY=your-secret-key \
  student-portal/student-service:latest

# Course Service
docker run -d \
  --name course-service \
  --network student-portal-network \
  -p 8000:8000 \
  -e MONGO_URI=mongodb://mongodb:27017 \
  -e JWT_SECRET_KEY=your-secret-key \
  student-portal/course-service:latest

# Enrollment Service
docker run -d \
  --name enrollment-service \
  --network student-portal-network \
  -p 8002:8002 \
  -e MONGO_URI=mongodb://mongodb:27017 \
  -e JWT_SECRET_KEY=your-secret-key \
  student-portal/enrollment-service:latest
```

### 4. Start Frontend
```bash
docker run -d \
  --name frontend \
  --network student-portal-network \
  -p 80:80 \
  student-portal/frontend:latest
```

### 5. Initialize Admin
```bash
docker run --rm \
  --network student-portal-network \
  -e MONGO_URI=mongodb://mongodb:27017 \
  student-portal/student-service:latest \
  python setup_admin.py
```

## Troubleshooting

### Port Already in Use
```bash
# Check what's using the port
# Windows
netstat -ano | findstr :80

# Linux/Mac
lsof -i :80
sudo lsof -i :80

# Stop conflicting service or change port in docker-compose.yml
```

### Cannot Connect to MongoDB
```bash
# Check MongoDB is running
docker ps | grep mongodb

# Check MongoDB logs
docker logs mongodb

# Restart MongoDB
docker-compose restart mongodb
```

### Container Keeps Restarting
```bash
# Check logs
docker logs <container-name>

# Check last logs before crash
docker logs --tail 50 <container-name>

# Common issues:
# - MongoDB not ready → Wait longer
# - Missing environment variables → Check docker-compose.yml
# - Port conflicts → Check ports not in use
```

### Image Build Fails
```bash
# Clear Docker cache
docker builder prune

# Rebuild without cache
docker-compose build --no-cache

# Check Dockerfile syntax
docker build --no-cache -t test ./backend/student-service
```

### Services Can't Communicate
```bash
# Check network
docker network ls
docker network inspect student-portal_student-portal-network

# Ensure all containers on same network
docker-compose ps
```

### Frontend Can't Connect to Backend
```bash
# Check backend services are accessible
curl http://localhost:8001/health
curl http://localhost:8000/health
curl http://localhost:8002/health

# Check from inside frontend container
docker-compose exec frontend wget -O- http://student-service:8001/health
```

## Production Deployment

### 1. Use Environment Variables
```bash
# Create .env file
cat > .env << EOL
MONGO_URI=mongodb://mongodb:27017
JWT_SECRET_KEY=$(openssl rand -hex 32)
ALLOWED_ORIGINS=https://yourdomain.com
EOL

# Update docker-compose.yml to use .env
```

### 2. Use Docker Secrets
```yaml
secrets:
  jwt_secret:
    file: ./secrets/jwt_secret.txt

services:
  student-service:
    secrets:
      - jwt_secret
```

### 3. Enable HTTPS
```yaml
frontend:
  environment:
    - VIRTUAL_HOST=yourdomain.com
    - LETSENCRYPT_HOST=yourdomain.com
    - LETSENCRYPT_EMAIL=admin@yourdomain.com
```

### 4. Use Production Images
```yaml
services:
  student-service:
    image: your-registry.com/student-service:v1.0.0
```

### 5. Configure Logging
```yaml
services:
  student-service:
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
```

### 6. Add Health Checks
Already included in docker-compose.yml:
```yaml
healthcheck:
  test: ["CMD", "curl", "-f", "http://localhost:8001/health"]
  interval: 30s
  timeout: 10s
  retries: 3
```

### 7. Configure Resource Limits
```yaml
services:
  student-service:
    deploy:
      resources:
        limits:
          cpus: '0.5'
          memory: 512M
        reservations:
          cpus: '0.25'
          memory: 256M
```

## Pushing to Registry

### Docker Hub
```bash
# Login
docker login

# Tag images
docker tag student-portal/student-service:latest yourusername/student-service:v1.0.0

# Push
docker push yourusername/student-service:v1.0.0
```

### Private Registry
```bash
# Tag with registry URL
docker tag student-portal/student-service:latest registry.company.com/student-service:v1.0.0

# Push
docker push registry.company.com/student-service:v1.0.0
```

### Update docker-compose.yml
```yaml
services:
  student-service:
    image: registry.company.com/student-service:v1.0.0
    # Remove build section
```

## Monitoring

### View Resource Usage
```bash
# All containers
docker stats

# Specific container
docker stats student-service
```

### Check Health
```bash
# Health status
docker inspect --format='{{.State.Health.Status}}' student-service

# Health logs
docker inspect --format='{{json .State.Health}}' student-service | jq
```

### Export Logs
```bash
# Export to file
docker-compose logs > application.log

# Export with timestamps
docker-compose logs -t > application-timestamped.log
```

## Backup and Restore

### Backup MongoDB
```bash
# Create backup
docker-compose exec mongodb mongodump --out /data/backup

# Copy to host
docker cp mongodb:/data/backup ./mongodb-backup

# Or use volume
docker run --rm \
  -v student-portal_mongodb_data:/data/db \
  -v $(pwd):/backup \
  mongo:7 \
  mongodump --out /backup/mongodb-backup
```

### Restore MongoDB
```bash
# Copy backup to container
docker cp ./mongodb-backup mongodb:/data/restore

# Restore
docker-compose exec mongodb mongorestore /data/restore
```

### Backup Volumes
```bash
# List volumes
docker volume ls

# Backup volume
docker run --rm \
  -v student-portal_mongodb_data:/data \
  -v $(pwd):/backup \
  alpine \
  tar czf /backup/mongodb-data-backup.tar.gz /data
```

## Cleanup

### Remove Everything
```bash
# Stop and remove containers, networks
docker-compose down

# Also remove volumes (deletes data!)
docker-compose down -v

# Remove images
docker rmi $(docker images 'student-portal/*' -q)
```

### Remove Unused Resources
```bash
# Remove stopped containers
docker container prune

# Remove unused images
docker image prune

# Remove unused volumes
docker volume prune

# Remove everything unused
docker system prune -a
```

## Tips and Best Practices

1. **Use .dockerignore** - Already included in project
2. **Multi-stage builds** - Frontend already uses this
3. **Layer caching** - Copy requirements.txt first
4. **Non-root user** - All containers run as non-root
5. **Health checks** - Already configured
6. **Resource limits** - Set in production
7. **Logging** - Configure log driver
8. **Secrets** - Never commit in images
9. **Version tags** - Always tag with versions
10. **CI/CD** - Automate builds and deployments

## Next Steps

1. Setup CI/CD pipeline (GitHub Actions, GitLab CI)
2. Deploy to cloud (AWS ECS, Google Cloud Run, Azure)
3. Setup monitoring (Prometheus, Grafana)
4. Configure backup automation
5. Implement rolling updates
6. Setup load balancing

---

**Docker makes deployment simple - one command to run everything!** 🚀
