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
students_collection = db["students"]
admins_collection = db["admins"]

# Create indexes for better performance
try:
    students_collection.create_index("email", unique=True)
    admins_collection.create_index("email", unique=True)
except:
    pass  # Indexes might already exist
