from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from services.gemini_service import GeminiService
import os
from dotenv import load_dotenv

load_dotenv()

router = APIRouter()

class CodeExplainRequest(BaseModel):
    code: str
    language: str = "python"

class CodeExplainResponse(BaseModel):
    explanation: str
    step_by_step: list[str]
    key_concepts: list[str]

@router.post("/explain", response_model=CodeExplainResponse)
async def explain_code(request: CodeExplainRequest):
    if not request.code.strip():
        raise HTTPException(status_code=400, detail="Code cannot be empty")
    
    try:
        gemini_service = GeminiService()
        result = await gemini_service.explain_code(request.code, request.language)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))