from fastapi import APIRouter, HTTPException, status, Header
import bcrypt
from datetime import datetime
from bson import ObjectId
from app.models.schemas import (
    StudentRegister, 
    StudentLogin, 
    StudentUpdate,
    StudentResponse,
    TokenResponse
)
from app.utils.jwt_handler import create_access_token, verify_token, get_token_from_header
from app.utils.database import students_collection

router = APIRouter(prefix="/students", tags=["Students"])

# ========== AUTHENTICATION ==========

@router.post("/register", status_code=status.HTTP_201_CREATED)
def register_student(student: StudentRegister):
    """Register a new student"""
    # Check if email already exists
    if students_collection.find_one({"email": student.email}):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Validate password length
    password = student.password.strip()
    if len(password.encode("utf-8")) > 72:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password too long - must be less than 72 characters"
        )
    
    # Hash password using bcrypt directly
    password_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password_bytes, salt).decode('utf-8')
    
    student_doc = {
        "name": student.name,
        "email": student.email,
        "password": hashed_password,
        "created_at": datetime.utcnow().isoformat(),
        "updated_at": datetime.utcnow().isoformat()
    }
    
    result = students_collection.insert_one(student_doc)
    
    return {
        "message": "Student registered successfully",
        "student_id": str(result.inserted_id)
    }

@router.post("/login", response_model=TokenResponse)
def login_student(credentials: StudentLogin):
    """Student login"""
    # Find student
    student = students_collection.find_one({"email": credentials.email})
    if not student:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    
    # Verify password using bcrypt directly
    password_bytes = credentials.password.encode('utf-8')
    stored_password = student["password"].encode('utf-8')
    
    if not bcrypt.checkpw(password_bytes, stored_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    
    # Create token
    token_data = {
        "id": str(student["_id"]),
        "email": student["email"],
        "name": student["name"],
        "role": "student"
    }
    token = create_access_token(token_data)
    
    # Prepare user data (without password)
    user_data = {
        "id": str(student["_id"]),
        "_id": str(student["_id"]),
        "name": student["name"],
        "email": student["email"]
    }
    
    return TokenResponse(
        access_token=token,
        token_type="bearer",
        role="student",
        user=user_data
    )

# ========== PROFILE MANAGEMENT ==========

@router.get("/me")
def get_student_profile(authorization: str = Header(...)):
    """Get current student profile"""
    token = get_token_from_header(authorization)
    decoded = verify_token(token)
    
    student = students_collection.find_one(
        {"_id": ObjectId(decoded["id"])},
        {"password": 0}
    )
    
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
        )
    
    student["_id"] = str(student["_id"])
    student["id"] = str(student["_id"])
    return student

@router.put("/me")
def update_student_profile(
    update_data: StudentUpdate,
    authorization: str = Header(...)
):
    """Update current student profile"""
    token = get_token_from_header(authorization)
    decoded = verify_token(token)
    
    # Prepare update fields
    update_fields = {}
    if update_data.name:
        update_fields["name"] = update_data.name
    if update_data.email:
        # Check if new email is already taken
        existing = students_collection.find_one({
            "email": update_data.email,
            "_id": {"$ne": ObjectId(decoded["id"])}
        })
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already in use"
            )
        update_fields["email"] = update_data.email
    
    if not update_fields:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No fields to update"
        )
    
    update_fields["updated_at"] = datetime.utcnow().isoformat()
    
    # Update student
    result = students_collection.update_one(
        {"_id": ObjectId(decoded["id"])},
        {"$set": update_fields}
    )
    
    if result.matched_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
        )
    
    return {"message": "Profile updated successfully"}

# ========== INTERNAL SERVICE ENDPOINTS ==========

@router.get("/{student_id}", response_model=StudentResponse)
def get_student_by_id(student_id: str):
    """Get student by ID (for internal service communication)"""
    if not ObjectId.is_valid(student_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid student ID format"
        )
    
    student = students_collection.find_one(
        {"_id": ObjectId(student_id)},
        {"password": 0}
    )
    
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
        )
    
    return StudentResponse(
        id=str(student["_id"]),
        name=student["name"],
        email=student["email"],
        created_at=student.get("created_at")
    )

@router.delete("/{student_id}")
def delete_student(
    student_id: str,
    authorization: str = Header(...)
):
    """Delete a student (admin only)"""
    token = get_token_from_header(authorization)
    decoded = verify_token(token)
    
    # Check if user is admin
    if decoded.get("role") != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    
    if not ObjectId.is_valid(student_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid student ID format"
        )
    
    result = students_collection.delete_one({"_id": ObjectId(student_id)})
    
    if result.deleted_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
        )
    
    return {"message": "Student deleted successfully"}
