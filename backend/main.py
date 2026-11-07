from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional

from services.parser import extract_text
from services.nlp_engine import extract_skills, compute_embeddings
from services.matcher import compute_gap_analysis
from services.role_mapper import infer_role_from_skills, infer_role_skills
from services.blueprint_generator import generate_blueprint_from_skills
from routers import assessment

app = FastAPI(title="SARTA Backend", description="Semantic Adaptive Recruitment and Technical Assessment Framework")

app.include_router(assessment.router)

# Enable CORS for Next.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class RoleInferRequest(BaseModel):
    skills: List[str]

class BlueprintRequest(BaseModel):
    candidate_skills: List[str]
    role: Optional[str] = "Backend Developer"
    missing_skills: Optional[List[str]] = []

@app.get("/")
def read_root():
    return {"message": "SARTA API is running", "framework": "Semantic Adaptive Recruitment and Technical Assessment"}

@app.post("/api/analyze-gap")
async def analyze_gap(resume: UploadFile = File(...), jd: UploadFile = File(...)):
    """
    Endpoint to process a candidate's resume and a target job description:
    - Extracts text via pdfplumber/python-docx
    - Identifies technical skills via spaCy NER + taxonomy
    - Computes semantic similarity via SBERT and Hungarian bipartite matching
    - Infers candidate role mapping
    """
    if not resume.filename or not jd.filename:
        raise HTTPException(status_code=400, detail="Both Resume and JD must be provided.")
        
    try:
        resume_bytes = await resume.read()
        jd_bytes = await jd.read()
        
        resume_text = extract_text(resume_bytes, resume.filename)
        jd_text = extract_text(jd_bytes, jd.filename)
        
        cand_skills = extract_skills(resume_text)
        job_skills = extract_skills(jd_text)
        
        cand_emb = compute_embeddings(cand_skills)
        job_emb = compute_embeddings(job_skills)
        
        gap_analysis = compute_gap_analysis(cand_skills, job_skills, cand_emb, job_emb)
        
        # Section 4.3: Role Mapping
        inferred_role_data = infer_role_from_skills(cand_skills)
        
        return {
            "status": "success",
            "candidate_skills_extracted": len(cand_skills),
            "candidate_skills": cand_skills,
            "job_skills_extracted": len(job_skills),
            "job_skills": job_skills,
            "inferred_role": inferred_role_data,
            "gap_analysis": gap_analysis
        }
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

@app.post("/api/infer-role")
def api_infer_role(req: RoleInferRequest):
    """Infers best-fit role profile from extracted candidate skills."""
    return infer_role_from_skills(req.skills)

@app.post("/api/generate-blueprint")
def api_generate_blueprint(req: BlueprintRequest):
    """Generates an assessment blueprint based on candidate skills and role."""
    return generate_blueprint_from_skills(
        candidate_skills=req.candidate_skills,
        role=req.role,
        missing_skills=req.missing_skills
    )
