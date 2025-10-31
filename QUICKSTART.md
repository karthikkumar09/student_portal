# Quick Start Guide

Get the Student Portal running in 5 minutes!

## Prerequisites Check

```bash
# Check Python
python --version  # Should be 3.8+

# Check Node.js
node --version    # Should be 16+

# Check MongoDB
mongod --version  # Should be installed
```

## Step 1: Start MongoDB

```bash
# macOS
brew services start mongodb-community

# Ubuntu/Debian
sudo systemctl start mongodb

# Or if already running
sudo systemctl status mongodb
```

## Step 2: Setup Student Service & Create Admin

```bash
cd backend/student-service
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python setup_admin.py
```

**Note the admin credentials shown!** Default is:
- Email: admin@example.com
- Password: admin123

## Step 3: Start Student Service

```bash
# In the same terminal (student-service directory)
uvicorn main:app --port 8001 --reload
```

Keep this terminal open!

## Step 4: Start Course Service

Open a NEW terminal:
```bash
cd backend/course-service
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --port 8000 --reload
```

Keep this terminal open!

## Step 5: Start Enrollment Service

Open a NEW terminal:
```bash
cd backend/enrollment-service
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --port 8002 --reload
```

Keep this terminal open!

## Step 6: Start Frontend

Open a NEW terminal:
```bash
cd frontend
npm install
npm run dev
```

## Step 7: Access the Application

Open your browser and go to: **http://localhost:5173**

### Test as Student:
1. Click "Register Now"
2. Create a new account
3. Login and explore the dashboard
4. Browse and enroll in courses (after admin creates them)

### Test as Admin:
1. Click "Admin Login"
2. Login with:
   - Email: admin@example.com
   - Password: admin123
3. Create some courses
4. View students and enrollments

## Common Issues

### "Connection Refused" Error
- Make sure MongoDB is running: `sudo systemctl status mongodb`
- Check if all services are running on correct ports

### "Module Not Found" Error
- Make sure you activated the virtual environment
- Run `pip install -r requirements.txt` again

### Port Already in Use
- Kill the process using that port
- Or change the port in the command

### Frontend Not Loading
```bash
cd frontend
rm -rf node_modules
npm install
npm run dev
```

## Need Help?

Check the main README.md for detailed documentation!

---

**You're all set! Enjoy using the Student Portal! 🎉**
