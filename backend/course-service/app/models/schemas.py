from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class CourseCreate(BaseModel):
    title: str = Field(..., min_length=3, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    credits: int = Field(..., ge=1, le=10)
    instructor: Optional[str] = Field(None, max_length=100)
    duration_weeks: Optional[int] = Field(None, ge=1, le=52)
    max_students: Optional[int] = Field(None, ge=1)

class CourseUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=3, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    credits: Optional[int] = Field(None, ge=1, le=10)
    instructor: Optional[str] = Field(None, max_length=100)
    duration_weeks: Optional[int] = Field(None, ge=1, le=52)
    max_students: Optional[int] = Field(None, ge=1)

class CourseResponse(BaseModel):
    id: str
    title: str
    description: Optional[str] = None
    credits: int
    instructor: Optional[str] = None
    duration_weeks: Optional[int] = None
    max_students: Optional[int] = None
    current_enrollments: int = 0
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

class CourseListResponse(BaseModel):
    courses: list[CourseResponse]
    total: int
    skip: int
    limit: int
