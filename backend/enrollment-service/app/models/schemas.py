from pydantic import BaseModel, Field
from typing import Optional, Literal
from datetime import datetime

class EnrollmentCreate(BaseModel):
    student_id: str
    course_id: str

class EnrollmentDrop(BaseModel):
    student_id: str
    course_id: str
    drop_reason: str = Field(..., min_length=10, max_length=500)

class ProgressUpdate(BaseModel):
    progress: int = Field(..., ge=0, le=100)

class EnrollmentResponse(BaseModel):
    id: str
    student_id: str
    course_id: str
    status: Literal["enrolled", "completed", "dropped"]
    progress: int = 0
    enrollment_date: str
    completion_date: Optional[str] = None
    drop_date: Optional[str] = None
    drop_reason: Optional[str] = None

class EnrollmentWithDetails(BaseModel):
    id: str
    student_id: str
    course_id: str
    student_name: str
    student_email: str
    course_title: str
    course_credits: int
    status: Literal["enrolled", "completed", "dropped"]
    progress: int
    enrollment_date: str
    completion_date: Optional[str] = None
    drop_date: Optional[str] = None
    drop_reason: Optional[str] = None

class StudentProgress(BaseModel):
    total_enrolled: int
    total_completed: int
    total_dropped: int
    total_credits_enrolled: int
    total_credits_completed: int
    enrollments: list[EnrollmentWithDetails]

class CourseEnrollments(BaseModel):
    course_id: str
    course_title: str
    total_enrollments: int
    active_enrollments: int
    completed_enrollments: int
    dropped_enrollments: int
    students: list[dict]

class CompleteRequest(BaseModel):
    student_id: str
    course_id: str
