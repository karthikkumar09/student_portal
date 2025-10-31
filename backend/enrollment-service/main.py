from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import enrollments
from fastapi.responses import RedirectResponse

app = FastAPI(
    title="Enrollment Service",
    description="Handles course enrollments, progress tracking, and completions",
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

app.include_router(enrollments.router)

@app.get("/")
def root():
    return RedirectResponse(url="/docs")

@app.get("/health")
def health_check():
    return {"status": "healthy"}
