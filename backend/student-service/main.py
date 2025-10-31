from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import students, admin

app = FastAPI(
    title="Student Service",
    description="Handles student and admin authentication and management",
    version="1.0.0"
)

# Configure CORS - Allow all origins in development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]
)

app.include_router(students.router)
app.include_router(admin.router)

@app.get("/")
def root():
    return {
        "service": "Student Service",
        "status": "running",
        "version": "1.0.0"
    }

@app.get("/health")
def health_check():
    return {"status": "healthy"}
