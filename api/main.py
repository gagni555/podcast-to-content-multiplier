from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import routers
from api.routers import auth, episodes

# Import settings
from config import settings

# Create FastAPI app
app = FastAPI(
    title="Podcast-to-Content Multiplier API",
    description="Transform podcast episodes into multiple content formats",
    version="0.1.0",
    debug=settings.debug
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Authentication"])
app.include_router(episodes.router, prefix="/api/v1/episodes", tags=["Episodes"])

@app.get("/")
async def root():
    return {"message": "Welcome to Podcast-to-Content Multiplier API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "api"}

# Additional endpoints can be added here