#!/usr/bin/env python3
"""
Setup script to create default admin user in MongoDB
Run this script once before starting the student service
"""

import bcrypt
from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")

# Default admin credentials
ADMIN_EMAIL = "admin@example.com"
ADMIN_PASSWORD = "admin123"
ADMIN_NAME = "System Administrator"

def create_admin_user():
    """Create default admin user in MongoDB"""
    
    # Connect to MongoDB
    client = MongoClient(MONGO_URI)
    db = client["student_portal"]
    admins_collection = db["admins"]
    
    # Check if admin already exists
    existing_admin = admins_collection.find_one({"email": ADMIN_EMAIL})
    
    if existing_admin:
        print(f"✅ Admin user already exists: {ADMIN_EMAIL}")
        print(f"   You can login with these credentials")
        return
    
    # Hash the password
    password_bytes = ADMIN_PASSWORD.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password_bytes, salt).decode('utf-8')
    
    # Create admin document
    admin_doc = {
        "name": ADMIN_NAME,
        "email": ADMIN_EMAIL,
        "password": hashed_password,
        "role": "admin"
    }
    
    # Insert admin user
    result = admins_collection.insert_one(admin_doc)
    
    print("=" * 60)
    print("✅ Admin user created successfully!")
    print("=" * 60)
    print(f"Email: {ADMIN_EMAIL}")
    print(f"Password: {ADMIN_PASSWORD}")
    print("=" * 60)
    print("⚠️  IMPORTANT: Change this password after first login!")
    print("=" * 60)

if __name__ == "__main__":
    try:
        print("Setting up admin user...")
        create_admin_user()
    except Exception as e:
        print(f"❌ Error: {e}")
        print("Make sure MongoDB is running on localhost:27017")
