# Student Portal - Complete System

A comprehensive student portal microservices application with separate backend services and a modern React frontend.

## 🏗️ Architecture

This project consists of:
- **Student Service** (Port 8001): Handles student and admin authentication
- **Course Service** (Port 8000): Manages courses
- **Enrollment Service** (Port 8002): Handles course enrollments and progress tracking
- **Frontend** (Port 5173): React + Vite application

## 📋 Prerequisites

- **Python 3.8+**
- **Node.js 16+** and npm
- **MongoDB** running on `localhost:27017`

## 🚀 Quick Start

### 1. Install MongoDB

If you don't have MongoDB installed:

**Ubuntu/Debian:**
```bash
sudo apt-get install mongodb
sudo systemctl start mongodb
sudo systemctl enable mongodb
```

**macOS (using Homebrew):**
```bash
brew tap mongodb/brew
brew install mongodb-community
brew services start mongodb-community
```

**Windows:**
Download and install from [MongoDB Download Center](https://www.mongodb.com/try/download/community)

### 2. Clone or Extract the Project

```bash
cd student-portal
```

### 3. Setup Backend Services

#### Terminal 1 - Student Service
```bash
cd backend/student-service
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python setup_admin.py  # Create default admin user
uvicorn main:app --port 8001 --reload
```

#### Terminal 2 - Course Service
```bash
cd backend/course-service
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --port 8000 --reload
```

#### Terminal 3 - Enrollment Service
```bash
cd backend/enrollment-service
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --port 8002 --reload
```

### 4. Setup Frontend

#### Terminal 4 - Frontend
```bash
cd frontend
npm install
npm run dev
```

## 🌐 Access the Application

- **Frontend**: http://localhost:5173
- **Student Service API**: http://localhost:8001/docs
- **Course Service API**: http://localhost:8000/docs
- **Enrollment Service API**: http://localhost:8002/docs

## 🐳 Docker Deployment (Alternative)

Want to skip manual setup? Use Docker!

```bash
# Start everything with one command
docker-compose up --build

# Access at http://localhost
```

See **[DOCKER.md](DOCKER.md)** for complete Docker documentation.

## ☸️ Kubernetes Deployment

Deploy to Kubernetes for production:

```bash
# Build images
./build-images.sh

# Deploy to Kubernetes
./deploy-k8s.sh
```

See **[KUBERNETES.md](KUBERNETES.md)** for complete Kubernetes documentation.

## 👤 Default Admin Credentials

After running `setup_admin.py`:
- **Email**: admin@example.com
- **Password**: admin123

## 📱 Using the Application

### As a Student:
1. Go to http://localhost:5173
2. Click "Register Now" to create a new account
3. Login with your credentials
4. Access the student dashboard to:
   - View your enrollment statistics
   - Browse available courses
   - Enroll in courses
   - Track your progress
   - Drop courses

### As an Admin:
1. Go to http://localhost:5173
2. Click "Admin Login"
3. Login with default credentials above
4. Access the admin dashboard to:
   - View system statistics
   - Create/edit/delete courses
   - View all students
   - Monitor enrollments

## 🔧 Configuration

All services use environment variables defined in their `.env` files:

```bash
MONGO_URI=mongodb://localhost:27017
JWT_SECRET_KEY=super-secret-key-change-in-production-12345
```

**IMPORTANT**: Change the JWT secret key in production!

## 📁 Project Structure

```
student-portal/
├── backend/
│   ├── student-service/
│   │   ├── app/
│   │   │   ├── models/
│   │   │   ├── routes/
│   │   │   └── utils/
│   │   ├── main.py
│   │   ├── requirements.txt
│   │   └── setup_admin.py
│   ├── course-service/
│   │   ├── app/
│   │   │   ├── models/
│   │   │   ├── routes/
│   │   │   └── utils/
│   │   ├── main.py
│   │   └── requirements.txt
│   └── enrollment-service/
│       ├── app/
│       │   ├── models/
│       │   ├── routes/
│       │   └── utils/
│       ├── main.py
│       └── requirements.txt
└── frontend/
    ├── src/
    │   ├── components/
    │   ├── contexts/
    │   ├── pages/
    │   ├── services/
    │   ├── App.jsx
    │   └── main.jsx
    ├── package.json
    └── index.html
```

## 🎯 Features

### Student Features:
- ✅ Register and login
- ✅ View personalized dashboard with statistics
- ✅ Browse all available courses
- ✅ Enroll in courses
- ✅ Track course progress
- ✅ Drop courses with reason
- ✅ View enrollment history

### Admin Features:
- ✅ Secure admin login
- ✅ View system-wide statistics
- ✅ Create, edit, and delete courses
- ✅ View all students
- ✅ View student enrollment details
- ✅ Monitor course enrollments

### Technical Features:
- ✅ JWT-based authentication
- ✅ Role-based access control (Student/Admin)
- ✅ Microservices architecture
- ✅ RESTful APIs
- ✅ Modern React UI with Tailwind CSS
- ✅ MongoDB database
- ✅ Password hashing with bcrypt

## 🐛 Troubleshooting

### CORS Errors
If you see CORS errors in the browser console, see **[CORS-FIX.md](CORS-FIX.md)** for solutions.

Quick fix: **Restart all backend services** (they now have CORS enabled for all origins in development).

### MongoDB Connection Issues
```bash
# Check if MongoDB is running
sudo systemctl status mongodb  # Linux
brew services list              # macOS

# If not running, start it
sudo systemctl start mongodb    # Linux
brew services start mongodb-community  # macOS
```

### Port Already in Use
If a port is already in use, you can:
1. Kill the process using that port
2. Or change the port in the service startup command

### Module Not Found Errors
Make sure you've activated the virtual environment and installed dependencies:
```bash
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

### Frontend Not Loading
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
npm run dev
```

## 🔐 Security Notes

1. Change the `JWT_SECRET_KEY` in production
2. Use HTTPS in production
3. Implement rate limiting for API endpoints
4. Add email verification for student registration
5. Use environment-specific configuration files

## 📝 API Documentation

Each service provides interactive API documentation via Swagger UI:
- Student Service: http://localhost:8001/docs
- Course Service: http://localhost:8000/docs
- Enrollment Service: http://localhost:8002/docs

## 🤝 Contributing

This is a complete working application. Feel free to extend it with:
- Email notifications
- Password reset functionality
- Course categories and search
- Student assignments and grades
- Course materials upload
- Real-time notifications

## 📄 License

This project is provided as-is for educational purposes.

## 🎓 Learning Outcomes

This project demonstrates:
- Microservices architecture
- RESTful API design
- JWT authentication
- Role-based access control
- React frontend development
- MongoDB database operations
- Service-to-service communication

---

**Happy Learning! 🚀**