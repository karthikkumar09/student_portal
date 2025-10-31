import os
from fastapi import APIRouter, HTTPException, status, Header
from bson import ObjectId
from datetime import datetime
from typing import Optional
import httpx

from app.models.schemas import (
    EnrollmentCreate,
    EnrollmentDrop,
    ProgressUpdate,
    EnrollmentResponse,
    EnrollmentWithDetails,
    StudentProgress,
    CourseEnrollments,
    CompleteRequest
)
from app.utils.database import enrollments_collection
from app.utils.jwt_handler import verify_token, get_token_from_header

router = APIRouter(prefix="/enrollments", tags=["Enrollments"])

@router.get("/service")
def service_status():
    return {"service": "Enrollment Service", "status": "running"}

STUDENT_SERVICE_URL = os.getenv("STUDENT_SERVICE_URL", "http://localhost:8001")
COURSE_SERVICE_URL = os.getenv("COURSE_SERVICE_URL", "http://localhost:8000")

def get_current_user(authorization: str):
    """Extract and verify user from token"""
    token = get_token_from_header(authorization)
    return verify_token(token)

def verify_admin(authorization: str):
    """Verify that the user is an admin"""
    decoded = get_current_user(authorization)
    if decoded.get("role") != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    return decoded

def verify_student_or_admin(authorization: str, student_id: str):
    """Verify user is the student or an admin"""
    decoded = get_current_user(authorization)
    
    if decoded.get("role") == "admin":
        return decoded
    
    if decoded.get("id") != student_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this resource"
        )
    
    return decoded

# ========== ENROLLMENT OPERATIONS ==========

@router.post("", response_model=EnrollmentResponse, status_code=status.HTTP_201_CREATED)
async def enroll_in_course(enrollment: EnrollmentCreate, authorization: str = Header(...)):
    """Enroll a student in a course"""
    decoded = get_current_user(authorization)
    
    # Verify student is enrolling themselves (unless admin)
    if decoded.get("role") != "admin" and decoded.get("id") != enrollment.student_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Can only enroll yourself"
        )
    
    # Verify student exists
    async with httpx.AsyncClient(timeout=10.0) as client:
        try:
            student_response = await client.get(
                f"{STUDENT_SERVICE_URL}/students/{enrollment.student_id}"
            )
            if student_response.status_code != 200:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Student not found"
                )
        except httpx.RequestError:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Student service unavailable"
            )
    
    # Verify course exists
    async with httpx.AsyncClient(timeout=10.0) as client:
        try:
            course_response = await client.get(
                f"{COURSE_SERVICE_URL}/courses/{enrollment.course_id}"
            )
            if course_response.status_code != 200:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Course not found"
                )
            course_data = course_response.json()
        except httpx.RequestError:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Course service unavailable"
            )
    
    # Check if already enrolled
    existing = enrollments_collection.find_one({
        "student_id": enrollment.student_id,
        "course_id": enrollment.course_id,
        "status": {"$in": ["enrolled", "completed"]}
    })
    
    if existing:
        if existing["status"] == "enrolled":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Already enrolled in this course"
            )
        elif existing["status"] == "completed":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Already completed this course"
            )
    
    # Check if course is full
    if course_data.get("max_students"):
        current_enrollments = enrollments_collection.count_documents({
            "course_id": enrollment.course_id,
            "status": "enrolled"
        })
        if current_enrollments >= course_data["max_students"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Course is full"
            )
    
    # Create enrollment
    enrollment_doc = {
        "student_id": enrollment.student_id,
        "course_id": enrollment.course_id,
        "status": "enrolled",
        "progress": 0,
        "enrollment_date": datetime.utcnow().isoformat(),
        "completion_date": None,
        "drop_date": None,
        "drop_reason": None
    }
    
    result = enrollments_collection.insert_one(enrollment_doc)
    created_enrollment = enrollments_collection.find_one({"_id": result.inserted_id})
    
    return EnrollmentResponse(
        id=str(created_enrollment["_id"]),
        student_id=created_enrollment["student_id"],
        course_id=created_enrollment["course_id"],
        status=created_enrollment["status"],
        progress=created_enrollment["progress"],
        enrollment_date=created_enrollment["enrollment_date"],
        completion_date=created_enrollment.get("completion_date"),
        drop_date=created_enrollment.get("drop_date"),
        drop_reason=created_enrollment.get("drop_reason")
    )

@router.post("/drop", response_model=EnrollmentResponse)
async def drop_course(drop_request: EnrollmentDrop, authorization: str = Header(...)):
    """Drop a course with reason"""
    decoded = get_current_user(authorization)
    
    # Verify student is dropping their own course (unless admin)
    if decoded.get("role") != "admin" and decoded.get("id") != drop_request.student_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Can only drop your own courses"
        )
    
    # Find enrollment
    enrollment = enrollments_collection.find_one({
        "student_id": drop_request.student_id,
        "course_id": drop_request.course_id,
        "status": "enrolled"
    })
    
    if not enrollment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Active enrollment not found"
        )
    
    # Update enrollment
    update_data = {
        "status": "dropped",
        "drop_date": datetime.utcnow().isoformat(),
        "drop_reason": drop_request.drop_reason
    }
    
    enrollments_collection.update_one(
        {"_id": enrollment["_id"]},
        {"$set": update_data}
    )
    
    updated_enrollment = enrollments_collection.find_one({"_id": enrollment["_id"]})
    
    return EnrollmentResponse(
        id=str(updated_enrollment["_id"]),
        student_id=updated_enrollment["student_id"],
        course_id=updated_enrollment["course_id"],
        status=updated_enrollment["status"],
        progress=updated_enrollment["progress"],
        enrollment_date=updated_enrollment["enrollment_date"],
        completion_date=updated_enrollment.get("completion_date"),
        drop_date=updated_enrollment.get("drop_date"),
        drop_reason=updated_enrollment.get("drop_reason")
    )

# ========== PROGRESS MANAGEMENT ==========

@router.put("/{enrollment_id}/progress", response_model=EnrollmentResponse)
async def update_progress(enrollment_id: str, progress_update: ProgressUpdate, authorization: str = Header(...)):
    """Update course progress (admin only)"""
    verify_admin(authorization)
    
    if not ObjectId.is_valid(enrollment_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid enrollment ID format"
        )
    
    enrollment = enrollments_collection.find_one({
        "_id": ObjectId(enrollment_id),
        "status": "enrolled"
    })
    
    if not enrollment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Active enrollment not found"
        )
    
    # Update progress
    update_data = {"progress": progress_update.progress}
    
    # Auto-complete if progress reaches 100%
    if progress_update.progress >= 100:
        update_data["status"] = "completed"
        update_data["completion_date"] = datetime.utcnow().isoformat()
        update_data["progress"] = 100
    
    enrollments_collection.update_one(
        {"_id": ObjectId(enrollment_id)},
        {"$set": update_data}
    )
    
    updated_enrollment = enrollments_collection.find_one({"_id": ObjectId(enrollment_id)})
    
    return EnrollmentResponse(
        id=str(updated_enrollment["_id"]),
        student_id=updated_enrollment["student_id"],
        course_id=updated_enrollment["course_id"],
        status=updated_enrollment["status"],
        progress=updated_enrollment["progress"],
        enrollment_date=updated_enrollment["enrollment_date"],
        completion_date=updated_enrollment.get("completion_date"),
        drop_date=updated_enrollment.get("drop_date"),
        drop_reason=updated_enrollment.get("drop_reason")
    )

@router.post("/complete")
async def mark_complete(data: CompleteRequest, authorization: str = Header(...)):
    """Mark a course as completed (admin only)"""
    verify_admin(authorization)
    
    enrollment = enrollments_collection.find_one({
        "student_id": data.student_id,
        "course_id": data.course_id,
        "status": "enrolled"
    })
    
    if not enrollment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Active enrollment not found"
        )
    
    # Update to completed
    enrollments_collection.update_one(
        {"_id": enrollment["_id"]},
        {"$set": {
            "status": "completed",
            "progress": 100,
            "completion_date": datetime.utcnow().isoformat()
        }}
    )
    
    return {
        "message": "Course marked as completed",
        "student_id": data.student_id,
        "course_id": data.course_id
    }

# ========== STUDENT ENROLLMENTS ==========

@router.get("/student/{student_id}", response_model=StudentProgress)
async def get_student_enrollments(student_id: str, authorization: str = Header(...)):
    """Get all enrollments for a student with progress"""
    verify_student_or_admin(authorization, student_id)
    
    # Get all enrollments
    enrollments = list(enrollments_collection.find({"student_id": student_id}))
    
    if not enrollments:
        return StudentProgress(
            total_enrolled=0,
            total_completed=0,
            total_dropped=0,
            total_credits_enrolled=0,
            total_credits_completed=0,
            enrollments=[]
        )
    
    # Fetch student details
    student_data = {}
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            student_response = await client.get(
                f"{STUDENT_SERVICE_URL}/students/{student_id}"
            )
            if student_response.status_code == 200:
                student_data = student_response.json()
    except:
        pass
    
    # Fetch course details
    course_ids = [e["course_id"] for e in enrollments]
    courses_map = {}
    
    async with httpx.AsyncClient(timeout=10.0) as client:
        for course_id in course_ids:
            try:
                course_response = await client.get(
                    f"{COURSE_SERVICE_URL}/courses/{course_id}"
                )
                if course_response.status_code == 200:
                    course_data = course_response.json()
                    courses_map[course_id] = course_data
            except:
                continue
    
    # Build detailed enrollments
    detailed_enrollments = []
    total_credits_enrolled = 0
    total_credits_completed = 0
    
    for enrollment in enrollments:
        course_data = courses_map.get(enrollment["course_id"], {})
        
        if enrollment["status"] in ["enrolled", "completed"]:
            total_credits_enrolled += course_data.get("credits", 0)
        
        if enrollment["status"] == "completed":
            total_credits_completed += course_data.get("credits", 0)
        
        detailed_enrollments.append(EnrollmentWithDetails(
            id=str(enrollment["_id"]),
            student_id=enrollment["student_id"],
            course_id=enrollment["course_id"],
            student_name=student_data.get("name", "Unknown"),
            student_email=student_data.get("email", "Unknown"),
            course_title=course_data.get("title", "Unknown Course"),
            course_credits=course_data.get("credits", 0),
            status=enrollment["status"],
            progress=enrollment["progress"],
            enrollment_date=enrollment["enrollment_date"],
            completion_date=enrollment.get("completion_date"),
            drop_date=enrollment.get("drop_date"),
            drop_reason=enrollment.get("drop_reason")
        ))
    
    return StudentProgress(
        total_enrolled=len([e for e in enrollments if e["status"] == "enrolled"]),
        total_completed=len([e for e in enrollments if e["status"] == "completed"]),
        total_dropped=len([e for e in enrollments if e["status"] == "dropped"]),
        total_credits_enrolled=total_credits_enrolled,
        total_credits_completed=total_credits_completed,
        enrollments=detailed_enrollments
    )

# ========== COURSE ENROLLMENTS ==========

@router.get("/course/{course_id}", response_model=CourseEnrollments)
async def get_course_enrollments(course_id: str, authorization: str = Header(...)):
    """Get all enrollments for a course (admin only)"""
    verify_admin(authorization)
    
    # Get course details
    async with httpx.AsyncClient(timeout=10.0) as client:
        try:
            course_response = await client.get(
                f"{COURSE_SERVICE_URL}/courses/{course_id}"
            )
            if course_response.status_code != 200:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Course not found"
                )
            course_data = course_response.json()
        except httpx.RequestError:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Course service unavailable"
            )
    
    # Get enrollments
    enrollments = list(enrollments_collection.find({"course_id": course_id}))
    
    # Get student details
    students = []
    async with httpx.AsyncClient(timeout=10.0) as client:
        for enrollment in enrollments:
            try:
                student_response = await client.get(
                    f"{STUDENT_SERVICE_URL}/students/{enrollment['student_id']}"
                )
                if student_response.status_code == 200:
                    student_data = student_response.json()
                    students.append({
                        "id": student_data["id"],
                        "name": student_data["name"],
                        "email": student_data["email"],
                        "status": enrollment["status"],
                        "progress": enrollment["progress"],
                        "enrollment_date": enrollment["enrollment_date"]
                    })
            except:
                continue
    
    return CourseEnrollments(
        course_id=course_id,
        course_title=course_data["title"],
        total_enrollments=len(enrollments),
        active_enrollments=len([e for e in enrollments if e["status"] == "enrolled"]),
        completed_enrollments=len([e for e in enrollments if e["status"] == "completed"]),
        dropped_enrollments=len([e for e in enrollments if e["status"] == "dropped"]),
        students=students
    )

# ========== UTILITY ENDPOINTS ==========

@router.get("/course/{course_id}/count")
async def get_course_enrollment_count(course_id: str):
    """Get enrollment count for a course (public)"""
    count = enrollments_collection.count_documents({
        "course_id": course_id,
        "status": {"$in": ["enrolled", "completed"]}
    })
    return {"count": count}

@router.get("/counts")
async def get_all_enrollment_counts():
    """Get enrollment counts for all courses (public)"""
    pipeline = [
        {"$match": {"status": {"$in": ["enrolled", "completed"]}}},
        {"$group": {"_id": "$course_id", "count": {"$sum": 1}}}
    ]
    
    results = list(enrollments_collection.aggregate(pipeline))
    return {item["_id"]: item["count"] for item in results}

@router.get("/stats")
async def get_enrollment_stats(authorization: str = Header(...)):
    """Get overall enrollment statistics (admin only)"""
    verify_admin(authorization)
    
    total = enrollments_collection.count_documents({})
    enrolled = enrollments_collection.count_documents({"status": "enrolled"})
    completed = enrollments_collection.count_documents({"status": "completed"})
    dropped = enrollments_collection.count_documents({"status": "dropped"})
    
    return {
        "total": total,
        "enrolled": enrolled,
        "completed": completed,
        "dropped": dropped
    }

@router.get("")
async def get_all_enrollments(authorization: str = Header(...), skip: int = 0, limit: int = 100):
    """Get all enrollments (admin only)"""
    verify_admin(authorization)
    
    total = enrollments_collection.count_documents({})
    enrollments = list(
        enrollments_collection.find()
        .skip(skip)
        .limit(limit)
        .sort("enrollment_date", -1)
    )
    
    for enrollment in enrollments:
        enrollment["_id"] = str(enrollment["_id"])
    
    return {
        "enrollments": enrollments,
        "total": total,
        "skip": skip,
        "limit": limit
    }
