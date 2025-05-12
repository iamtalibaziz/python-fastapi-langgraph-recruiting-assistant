from fastapi import APIRouter, UploadFile, Form, File
from fastapi.responses import JSONResponse
from app.helpers.agent import run_agent

router = APIRouter()

@router.post("/evaluate_candidate")
async def evaluate_candidate(
    candidate_name: str = Form(...),
    resume_file: UploadFile = File(...),
    job_description: str = Form(...)
):
    result = await run_agent(candidate_name, resume_file, job_description)
    return JSONResponse(content=result)