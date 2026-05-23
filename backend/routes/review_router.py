from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from services.gemini_service import GeminiService
import os
from dotenv import load_dotenv

load_dotenv()

router = APIRouter()

class CodeReviewRequest(BaseModel):
    code: str
    language: str = "python"

class CodeReviewResponse(BaseModel):
    bugs: list[str]
    optimizations: list[str]
    explanation: str
    best_practices: list[str]
    complexity_feedback: str

@router.post("/review", response_model=CodeReviewResponse)
async def review_code(request: CodeReviewRequest):
    if not request.code.strip():
        raise HTTPException(status_code=400, detail="Code cannot be empty")
    
    try:
        gemini_service = GeminiService()
        result = await gemini_service.review_code(request.code, request.language)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))