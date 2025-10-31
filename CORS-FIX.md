# CORS Issues - Troubleshooting Guide

## Problem: CORS Errors in Browser Console

If you see errors like:
```
Access to XMLHttpRequest at 'http://localhost:8000/courses' from origin 'http://localhost:5173' 
has been blocked by CORS policy: No 'Access-Control-Allow-Origin' header is present on the requested resource.
```

## Quick Fix

### Solution 1: Restart Backend Services

The CORS middleware is configured in all backend services. Simply restart them:

**Stop all services** (Ctrl+C in each terminal)

**Then restart in order:**

#### Terminal 1 - Student Service
```bash
cd backend/student-service
venv\Scripts\activate  # Windows
# or: source venv/bin/activate  # Linux/Mac
uvicorn main:app --port 8001 --reload
```

#### Terminal 2 - Course Service
```bash
cd backend/course-service
venv\Scripts\activate  # Windows
# or: source venv/bin/activate  # Linux/Mac
uvicorn main:app --port 8000 --reload
```

#### Terminal 3 - Enrollment Service
```bash
cd backend/enrollment-service
venv\Scripts\activate  # Windows
# or: source venv/bin/activate  # Linux/Mac
uvicorn main:app --port 8002 --reload
```

#### Terminal 4 - Frontend
```bash
cd frontend
npm run dev
```

### Solution 2: Check Services Are Running

Verify all services are running:

1. **Student Service**: http://localhost:8001/docs
2. **Course Service**: http://localhost:8000/docs
3. **Enrollment Service**: http://localhost:8002/docs
4. **Frontend**: http://localhost:5173

If any service shows "Cannot connect" or timeout:
- That service is not running
- Start it following the commands above

### Solution 3: Clear Browser Cache

Sometimes browsers cache CORS responses:

1. Open DevTools (F12)
2. Right-click the refresh button
3. Select "Empty Cache and Hard Reload"
4. Or try incognito/private window

### Solution 4: Check MongoDB is Running

All backend services need MongoDB:

**Windows:**
```powershell
# Check if MongoDB is running
Get-Process mongod

# If not running, start it
# If installed as service:
net start MongoDB

# Or run manually:
mongod
```

**Linux/Mac:**
```bash
# Check status
sudo systemctl status mongod  # Linux
brew services list | grep mongodb  # Mac

# Start if not running
sudo systemctl start mongod  # Linux
brew services start mongodb-community  # Mac
```

## Why This Happens

CORS errors occur when:
1. **Backend services aren't running** - Start all 3 services
2. **Backend started before fix applied** - Restart services
3. **MongoDB not running** - Backend can't start without DB
4. **Wrong ports** - Check services run on correct ports

## Current CORS Configuration

All backend services now use:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins (development only)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

⚠️ **Note:** `allow_origins=["*"]` is for **development only**. 
For production, change to specific domains:
```python
allow_origins=["https://yourdomain.com"]
```

## Testing CORS is Fixed

Open browser console (F12) and run:
```javascript
fetch('http://localhost:8000/courses')
  .then(r => r.json())
  .then(d => console.log('CORS working!', d))
  .catch(e => console.error('CORS still failing:', e))
```

If you see "CORS working!" - it's fixed! ✅

## Still Having Issues?

### Check Network Tab
1. Open DevTools (F12)
2. Go to Network tab
3. Try the action again
4. Look for failed requests (red)
5. Click on failed request
6. Check "Headers" tab
7. Look at Response Headers - should include:
   - `access-control-allow-origin: *`
   - `access-control-allow-credentials: true`

### Verify Service Health
```bash
# Test each service
curl http://localhost:8001/health  # Student
curl http://localhost:8000/health  # Course
curl http://localhost:8002/health  # Enrollment
```

All should return: `{"status":"healthy"}`

### Check Service Logs
Look at the terminal where service is running for errors.

Common errors:
- `ModuleNotFoundError` → Install dependencies
- `Connection refused` → MongoDB not running
- `Port already in use` → Kill process using that port

## Using Docker Compose (Easier Alternative)

Instead of running services individually, use Docker Compose:

```bash
# Build and start all services
docker-compose up --build

# Access at:
# Frontend: http://localhost:80
# Services work automatically!
```

This avoids CORS issues since services communicate internally.

## Production CORS Configuration

For production, update all `main.py` files:

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI()

# Get allowed origins from environment
allowed_origins = os.getenv("ALLOWED_ORIGINS", "").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,  # ["https://yourdomain.com"]
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)
```

Then set environment variable:
```bash
export ALLOWED_ORIGINS="https://yourdomain.com,https://app.yourdomain.com"
```

---

**Need More Help?**

1. Check main README.md
2. Look at service logs in terminal
3. Verify all prerequisites are installed
4. Try Docker Compose instead

**The CORS fix is included in all backend services - just restart them!**
