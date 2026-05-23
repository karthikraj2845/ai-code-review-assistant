from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.review_router import router as review_router
from routes.explain_router import router as explain_router
from routes.optimize_router import router as optimize_router

app = FastAPI(
    title="AI Code Review Assistant",
    description="A full-stack web application for code review using Gemini API",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(review_router, prefix="/api", tags=["review"])
app.include_router(explain_router, prefix="/api", tags=["explain"])
app.include_router(optimize_router, prefix="/api", tags=["optimize"])

@app.get("/")
async def root():
    return {"message": "Welcome to AI Code Review Assistant API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}