from fastapi import FastAPI, UploadFile, Form, File
from fastapi.responses import JSONResponse
from agent import run_agent

app = FastAPI()

@app.post("/evaluate_candidate")
async def evaluate_candidate(
    candidate_name: str = Form(...),
    resume_file: UploadFile = File(...),
    job_description: str = Form(...)
):
    result = await run_agent(candidate_name, resume_file, job_description)
    return JSONResponse(content=result)
