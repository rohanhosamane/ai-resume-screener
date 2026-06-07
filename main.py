from fastapi import FastAPI, UploadFile, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.parser import extract_text
from app.screener import screen_resume
from app.database import create_table, save_result, get_history
from dotenv import load_dotenv
load_dotenv()
import os

app = FastAPI(title="AI Resume Screener")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve frontend
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.on_event("startup")
def startup():
    try:
        create_table()
    except Exception as e:
        print(f"DB init skipped: {e}")

@app.get("/")
def index():
    return FileResponse("static/index.html")

@app.post("/screen")
async def screen(
    resume: UploadFile,
    job_description: str = Form(...)
):
    if not resume.filename.lower().endswith((".pdf", ".docx")):
        raise HTTPException(status_code=400, detail="Only PDF or DOCX files are supported.")

    file_bytes = await resume.read()

    if len(file_bytes) > 5 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="File too large. Max size is 5MB.")

    try:
        resume_text = extract_text(file_bytes, resume.filename)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Could not parse file: {str(e)}")

    if not resume_text.strip():
        raise HTTPException(status_code=400, detail="Could not extract text from the file. Try a different file.")

    try:
        result = screen_resume(resume_text, job_description)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI screening failed: {str(e)}")

    try:
        save_result(resume.filename, result)
    except Exception as e:
        print(f"DB save skipped: {e}")

    return result

@app.get("/history")
def history():
    try:
        return get_history()
    except Exception as e:
        return []

@app.get("/health")
def health():
    return {"status": "running"}
