from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")

# Create MongoDB client
client = MongoClient(MONGO_URI)

# Database
db = client["student_portal"]

# Collections
enrollments_collection = db["enrollments"]

# Create indexes for better performance
try:
    enrollments_collection.create_index([("student_id", 1), ("course_id", 1)], unique=True)
    enrollments_collection.create_index("student_id")
    enrollments_collection.create_index("course_id")
    enrollments_collection.create_index("status")
    enrollments_collection.create_index("enrollment_date")
except:
    pass  # Indexes might already exist
