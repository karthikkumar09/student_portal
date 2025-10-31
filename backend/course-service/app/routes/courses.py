from fastapi import APIRouter, HTTPException, status, Header
from bson import ObjectId
from datetime import datetime
from typing import Optional
import httpx

from app.models.schemas import (
    CourseCreate,
    CourseUpdate,
    CourseResponse,
    CourseListResponse
)
from app.utils.database import courses_collection, db
from app.utils.jwt_handler import verify_token, get_token_from_header

router = APIRouter(prefix="/courses", tags=["Courses"])

ENROLLMENT_SERVICE_URL = "http://localhost:8002"

def verify_admin(authorization: str):
    """Verify that the user is an admin"""
    token = get_token_from_header(authorization)
    decoded = verify_token(token)
    
    if decoded.get("role") != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    return decoded

# ========== COURSE CRUD OPERATIONS ==========

@router.post("", response_model=CourseResponse, status_code=status.HTTP_201_CREATED)
async def create_course(course: CourseCreate, authorization: str = Header(...)):
    """Create a new course (admin only)"""
    verify_admin(authorization)
    
    # Check if course with same title exists
    existing = courses_collection.find_one({"title": course.title})
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Course with this title already exists"
        )
    
    # Create course document
    course_doc = {
        **course.dict(),
        "current_enrollments": 0,
        "created_at": datetime.utcnow().isoformat(),
        "updated_at": datetime.utcnow().isoformat()
    }
    
    try:
        result = courses_collection.insert_one(course_doc)
        created_course = courses_collection.find_one({"_id": result.inserted_id})
    except Exception as e:
        # Handle duplicate key errors gracefully
        error_msg = str(e)
        if "duplicate key error" in error_msg.lower() or "E11000" in error_msg:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="A course with this information already exists. Please check the title and try again."
            )
        # Re-raise other errors
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create course: {error_msg}"
        )
    
    return CourseResponse(
        id=str(created_course["_id"]),
        title=created_course["title"],
        description=created_course.get("description"),
        credits=created_course["credits"],
        instructor=created_course.get("instructor"),
        duration_weeks=created_course.get("duration_weeks"),
        max_students=created_course.get("max_students"),
        current_enrollments=created_course.get("current_enrollments", 0),
        created_at=created_course.get("created_at"),
        updated_at=created_course.get("updated_at")
    )

@router.get("", response_model=CourseListResponse)
async def get_all_courses(skip: int = 0, limit: int = 100):
    """Get all courses (paginated)"""
    total = courses_collection.count_documents({})
    
    courses = list(
        courses_collection.find()
        .skip(skip)
        .limit(limit)
        .sort("created_at", -1)
    )
    
    # Get enrollment counts from enrollment service
    enrollment_counts = {}
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get(f"{ENROLLMENT_SERVICE_URL}/enrollments/counts")
            if response.status_code == 200:
                enrollment_counts = response.json()
    except:
        pass  # Continue with empty counts if service unavailable
    
    course_list = []
    for course in courses:
        course_id = str(course["_id"])
        course_list.append(CourseResponse(
            id=course_id,
            title=course["title"],
            description=course.get("description"),
            credits=course["credits"],
            instructor=course.get("instructor"),
            duration_weeks=course.get("duration_weeks"),
            max_students=course.get("max_students"),
            current_enrollments=enrollment_counts.get(course_id, 0),
            created_at=course.get("created_at"),
            updated_at=course.get("updated_at")
        ))
    
    return CourseListResponse(
        courses=course_list,
        total=total,
        skip=skip,
        limit=limit
    )

@router.get("/{course_id}", response_model=CourseResponse)
async def get_course(course_id: str):
    """Get a specific course"""
    if not ObjectId.is_valid(course_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid course ID format"
        )
    
    course = courses_collection.find_one({"_id": ObjectId(course_id)})
    
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found"
        )
    
    # Get enrollment count
    enrollment_count = 0
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get(
                f"{ENROLLMENT_SERVICE_URL}/enrollments/course/{course_id}/count"
            )
            if response.status_code == 200:
                enrollment_count = response.json().get("count", 0)
    except:
        pass  # Continue with 0 if service unavailable
    
    return CourseResponse(
        id=str(course["_id"]),
        title=course["title"],
        description=course.get("description"),
        credits=course["credits"],
        instructor=course.get("instructor"),
        duration_weeks=course.get("duration_weeks"),
        max_students=course.get("max_students"),
        current_enrollments=enrollment_count,
        created_at=course.get("created_at"),
        updated_at=course.get("updated_at")
    )

@router.put("/{course_id}", response_model=CourseResponse)
async def update_course(
    course_id: str,
    course_update: CourseUpdate,
    authorization: str = Header(...)
):
    """Update a course (admin only)"""
    verify_admin(authorization)
    
    if not ObjectId.is_valid(course_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid course ID format"
        )
    
    # Check if course exists
    existing_course = courses_collection.find_one({"_id": ObjectId(course_id)})
    if not existing_course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found"
        )
    
    # Prepare update fields
    update_fields = {
        k: v for k, v in course_update.dict(exclude_unset=True).items()
        if v is not None
    }
    
    if not update_fields:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No fields to update"
        )
    
    # Check if title is being changed and already exists
    if "title" in update_fields:
        duplicate = courses_collection.find_one({
            "title": update_fields["title"],
            "_id": {"$ne": ObjectId(course_id)}
        })
        if duplicate:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Course with this title already exists"
            )
    
    update_fields["updated_at"] = datetime.utcnow().isoformat()
    
    # Update course
    courses_collection.update_one(
        {"_id": ObjectId(course_id)},
        {"$set": update_fields}
    )
    
    # Get updated course
    updated_course = courses_collection.find_one({"_id": ObjectId(course_id)})
    
    # Get enrollment count
    enrollment_count = 0
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get(
                f"{ENROLLMENT_SERVICE_URL}/enrollments/course/{course_id}/count"
            )
            if response.status_code == 200:
                enrollment_count = response.json().get("count", 0)
    except:
        pass
    
    return CourseResponse(
        id=str(updated_course["_id"]),
        title=updated_course["title"],
        description=updated_course.get("description"),
        credits=updated_course["credits"],
        instructor=updated_course.get("instructor"),
        duration_weeks=updated_course.get("duration_weeks"),
        max_students=updated_course.get("max_students"),
        current_enrollments=enrollment_count,
        created_at=updated_course.get("created_at"),
        updated_at=updated_course.get("updated_at")
    )

@router.delete("/{course_id}")
async def delete_course(course_id: str, authorization: str = Header(...)):
    """Delete a course (admin only)"""
    verify_admin(authorization)
    
    if not ObjectId.is_valid(course_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid course ID format"
        )
    
    # Check if course has enrollments
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get(
                f"{ENROLLMENT_SERVICE_URL}/enrollments/course/{course_id}/count"
            )
            if response.status_code == 200:
                enrollment_count = response.json().get("count", 0)
                
                if enrollment_count > 0:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"Cannot delete course with {enrollment_count} active enrollments. "
                               "Please remove all enrollments first."
                    )
    except HTTPException:
        raise
    except:
        pass  # If service unavailable, allow deletion
    
    # Delete course
    result = courses_collection.delete_one({"_id": ObjectId(course_id)})
    
    if result.deleted_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found"
        )
    
    return {
        "message": "Course deleted successfully",
        "course_id": course_id
    }