from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .db import models
from .db.database import engine
from .api.endpoints import resumes

# This command tells SQLAlchemy to look at all the models that inherit from our
# 'Base' class (in this case, just the Resume model) and create the corresponding
# tables in the database if they don't already exist.
models.Base.metadata.create_all(bind=engine)

# Create the main FastAPI application instance.
# The title, description, and version will show up in the auto-generated API docs (e.g., at /docs).
app = FastAPI(
    title="Smart Resume Analyzer API",
    description="An API to upload resumes and get AI-powered analysis.",
    version="1.0.0"
)

# --- Middleware Setup ---

# CORS (Cross-Origin Resource Sharing) Middleware
# This is crucial to allow your React frontend (running on a different port/domain)
# to communicate with this backend API. Without it, the browser would block the requests.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # WARNING: For development only. In production, you should restrict this to your frontend's actual domain, e.g., ["https://your-frontend.com"].
    allow_credentials=True,
    allow_methods=["*"], # Allows all standard HTTP methods.
    allow_headers=["*"], # Allows all headers.
)

# --- API Routers ---

# Include the API router from our resumes endpoint file.
# This keeps our code organized by grouping related endpoints together.
# All routes in 'resumes.router' will now be prefixed with '/api'.
app.include_router(resumes.router, prefix="/api", tags=["Resumes"])

# --- Root Endpoint ---

@app.get("/", tags=["Root"])
def read_root():
    """
    A simple root endpoint to confirm the API is running.
    You can visit this in your browser to get a quick health check.
    """
    return {"message": "Welcome to the Smart Resume Analyzer API!"}