from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from services.gemini_service import GeminiService
import os
from dotenv import load_dotenv

load_dotenv()

router = APIRouter()

class CodeOptimizeRequest(BaseModel):
    code: str
    language: str = "python"

class CodeOptimizeResponse(BaseModel):
    optimized_code: str
    optimizations: list[str]
    explanation: str

@router.post("/optimize", response_model=CodeOptimizeResponse)
async def optimize_code(request: CodeOptimizeRequest):
    if not request.code.strip():
        raise HTTPException(status_code=400, detail="Code cannot be empty")
    
    try:
        gemini_service = GeminiService()
        result = await gemini_service.optimize_code(request.code, request.language)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))