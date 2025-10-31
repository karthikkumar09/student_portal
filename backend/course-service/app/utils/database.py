from pymongo import MongoClient, ASCENDING
from pymongo.errors import OperationFailure
from dotenv import load_dotenv
import os

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")

# Create MongoDB client
client = MongoClient(MONGO_URI)

# Database
db = client["student_portal"]

# Collections
courses_collection = db["courses"]

# Fix indexes on startup
def initialize_indexes():
    """Initialize proper indexes and remove any legacy indexes"""
    try:
        # Drop the old problematic index if it exists
        try:
            courses_collection.drop_index("course_name_1_department_1")
            print("✓ Dropped legacy index: course_name_1_department_1")
        except OperationFailure:
            pass  # Index doesn't exist, which is fine
        
        # Create unique index on title
        try:
            courses_collection.create_index(
                [("title", ASCENDING)], 
                unique=True, 
                name="title_1_unique"
            )
            print("✓ Created unique index on 'title'")
        except OperationFailure:
            pass  # Index already exists
        
        # Create index on created_at for sorting
        try:
            courses_collection.create_index(
                [("created_at", ASCENDING)],
                name="created_at_1"
            )
            print("✓ Created index on 'created_at'")
        except OperationFailure:
            pass  # Index already exists
        
        # Clean up any old documents with legacy fields
        result = courses_collection.update_many(
            {
                "$or": [
                    {"course_name": {"$exists": True}},
                    {"department": {"$exists": True}}
                ]
            },
            {
                "$unset": {
                    "course_name": "",
                    "department": ""
                }
            }
        )
        if result.modified_count > 0:
            print(f"✓ Cleaned up {result.modified_count} documents with legacy fields")
            
    except Exception as e:
        print(f"Warning: Could not initialize indexes: {e}")

# Initialize indexes when module is loaded
initialize_indexes()