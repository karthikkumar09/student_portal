from fastapi import APIRouter, HTTPException, status, Header
import bcrypt
from app.models.schemas import AdminLogin, AdminResponse, TokenResponse
from app.utils.jwt_handler import create_access_token, verify_token, get_token_from_header
from app.utils.database import admins_collection, students_collection

router = APIRouter(prefix="/admin", tags=["Admin"])

# ========== ADMIN AUTHENTICATION ==========

@router.post("/login", response_model=TokenResponse)
def admin_login(credentials: AdminLogin):
    """Admin login"""
    admin = admins_collection.find_one({"email": credentials.email})
    
    if not admin:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    
    # Verify password using bcrypt directly
    password_bytes = credentials.password.encode('utf-8')
    stored_password = admin["password"].encode('utf-8')
    
    if not bcrypt.checkpw(password_bytes, stored_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    
    # Create token
    token_data = {
        "id": str(admin["_id"]),
        "email": admin["email"],
        "name": admin["name"],
        "role": "admin"
    }
    token = create_access_token(token_data)
    
    # Prepare user data
    user_data = {
        "id": str(admin["_id"]),
        "_id": str(admin["_id"]),
        "name": admin["name"],
        "email": admin["email"],
        "role": "admin"
    }
    
    return TokenResponse(
        access_token=token,
        token_type="bearer",
        role="admin",
        user=user_data
    )

@router.get("/me")
def get_admin_profile(authorization: str = Header(...)):
    """Get current admin profile"""
    token = get_token_from_header(authorization)
    decoded = verify_token(token)
    
    # Verify admin role
    if decoded.get("role") != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    
    admin = admins_collection.find_one(
        {"email": decoded["email"]},
        {"password": 0}
    )
    
    if not admin:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Admin not found"
        )
    
    admin["_id"] = str(admin["_id"])
    admin["id"] = str(admin["_id"])
    admin["role"] = "admin"
    return admin

# ========== STUDENT MANAGEMENT ==========

@router.get("/students")
def get_all_students(
    authorization: str = Header(...),
    skip: int = 0,
    limit: int = 100
):
    """Get all students (paginated)"""
    token = get_token_from_header(authorization)
    decoded = verify_token(token)
    
    # Verify admin role
    if decoded.get("role") != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    
    # Get total count
    total = students_collection.count_documents({})
    
    # Get students
    students = list(
        students_collection.find({}, {"password": 0})
        .skip(skip)
        .limit(limit)
    )
    
    for student in students:
        student["_id"] = str(student["_id"])
        student["id"] = str(student["_id"])
    
    return {
        "students": students,
        "total": total,
        "skip": skip,
        "limit": limit
    }

@router.get("/students/{student_id}")
def get_student_details(
    student_id: str,
    authorization: str = Header(...)
):
    """Get detailed student information"""
    token = get_token_from_header(authorization)
    decoded = verify_token(token)
    
    # Verify admin role
    if decoded.get("role") != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    
    from bson import ObjectId
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
    
    student["_id"] = str(student["_id"])
    student["id"] = str(student["_id"])
    
    return student
