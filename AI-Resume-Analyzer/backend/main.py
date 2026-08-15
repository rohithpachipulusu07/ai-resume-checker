from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware

import os
import shutil

from resume_parser import extract_text_from_pdf
from skill_extractor import extract_skills, generate_ats_suggestions, generate_interview_questions
from matcher import calculate_match_breakdown
from model_trainer import train_model


app = FastAPI(title="AI Resume Analyzer")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


UPLOAD_FOLDER = "../uploads"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.get("/")
def home():
    return {
        "message": "AI Resume Analyzer API is running"
    }


@app.post("/analyze")
async def analyze_resume(
    resume: UploadFile = File(...),
    job_description: str = Form(...),
    use_trained_model: bool = Form(default=True)
):

    file_path = os.path.join(UPLOAD_FOLDER, resume.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(resume.file, buffer)

    resume_text = extract_text_from_pdf(file_path)

    resume_skills = extract_skills(resume_text)
    job_skills = extract_skills(job_description)
    breakdown = calculate_match_breakdown(resume_text, job_description, use_trained_model=use_trained_model)

    missing_skills = [
        skill for skill in job_skills
        if skill not in resume_skills
    ]
    ats_suggestions = generate_ats_suggestions(resume_text)
    interview_questions = generate_interview_questions(resume_text)

    return {
        "overall_match": breakdown["overall_match"],
        "keyword_match": breakdown["keyword_match"],
        "semantic_match": breakdown["semantic_match"],
        "skill_match": breakdown["skill_match"],
        "resume_skills": resume_skills,
        "job_skills": job_skills,
        "missing_skills": missing_skills,
        "ats_suggestions": ats_suggestions,
        "interview_questions": interview_questions
    }


@app.post("/train")
async def train_model_endpoint(num_samples: int = 500):
    """
    Train the ML model on randomly generated resume-job description pairs.
    
    Args:
        num_samples: Number of training samples to generate (default: 500)
    
    Returns:
        Status message with training completion details
    """
    try:
        model, vectorizer = train_model(num_samples=num_samples)
        return {
            "status": "success",
            "message": f"Model trained successfully with {num_samples} samples",
            "samples": num_samples
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }