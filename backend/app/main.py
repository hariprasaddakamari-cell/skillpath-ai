from fastapi import FastAPI, UploadFile, File, Form, HTTPException
import os
from fastapi.middleware.cors import CORSMiddleware
from pypdf import PdfReader
import io, re
from .models import AnalyzeRequest, AnalyzeResponse, Profile, SimulationRequest
from .rag import KnowledgeBase
from .agents import build_graph, score_job
from .normalizer import normalize_skill, normalize_skills

app=FastAPI(title="SkillPath AI",version="1.0.0",description="C4 Skill-Gap-to-Job Matching Agent")

_origins=[x.strip() for x in os.getenv("CORS_ORIGINS", "http://localhost:5173").split(",") if x.strip()]
app.add_middleware(CORSMiddleware,allow_origins=_origins,allow_credentials=True,allow_methods=["*"],allow_headers=["*"])
KB=KnowledgeBase(); GRAPH=build_graph(KB)

@app.get("/api/health")
def health():
    return {"status":"ok","jobs":len(KB.jobs),"courses":len(KB.courses),"pipeline":["loader","splitter","embeddings","FAISS","retriever","LangGraph","tools"]}

@app.get("/api/jobs")
def jobs(): return [j.model_dump() for j in KB.jobs]
@app.get("/api/courses")
def courses(): return [c.model_dump() for c in KB.courses]


def run(profile, free_only=False):
    result=GRAPH.invoke({"profile":profile.model_dump(),"free_only":free_only,"trace":[],"sources":[],"kb":KB})
    return AnalyzeResponse(profile=result["profile"],jobs=result.get("matched_jobs",[]),skill_gaps=result.get("gaps",{}),courses=result.get("courses",{}),roadmap=result.get("roadmap",{}),trace=result.get("trace",[]),sources=result.get("sources",[]))

@app.post("/api/analyze",response_model=AnalyzeResponse)
def analyze(req:AnalyzeRequest): return run(req.profile,req.free_only)

SKILL_PATTERNS={
    "Java":[r"\bjava\b"],"Spring Boot":[r"spring\s*boot"],"Spring Security":[r"spring\s*security"],"SQL":[r"\bsql\b"],"PostgreSQL":[r"postgres(?:ql)?"],"React":[r"\breact(?:js)?\b"],"JavaScript":[r"javascript|\bjs\b"],"Git":[r"\bgit(?:hub)?\b"],"Docker":[r"\bdocker\b"],"Redis":[r"\bredis\b"],"Kafka":[r"\bkafka\b"],"AWS":[r"\baws\b|amazon web services"],"Kubernetes":[r"kubernetes|\bk8s\b"],"Linux":[r"\blinux\b"],"CI/CD":[r"ci\s*/?\s*cd|github actions"],"Python":[r"\bpython\b"],"FastAPI":[r"\bfastapi\b"],"REST API":[r"rest(?:ful)?\s*api|\brest\b"],"JPA":[r"\bjpa\b|hibernate"],"Data Structures":[r"data structures|algorithms"],"Postman":[r"\bpostman\b"]}

def extract_skills(text):
    low=text.lower(); found=[]
    for skill,patterns in SKILL_PATTERNS.items():
        if any(re.search(p,low) for p in patterns): found.append(skill)
    return normalize_skills(found)

@app.post("/api/analyze-resume",response_model=AnalyzeResponse)
async def analyze_resume(file:UploadFile=File(...),location:str=Form("Hyderabad"),interests:str=Form("Backend Development"),free_only:bool=Form(False)):
    if not file.filename or not file.filename.lower().endswith(".pdf"): raise HTTPException(400,"Upload a PDF resume")
    raw=await file.read()
    if len(raw)>5*1024*1024: raise HTTPException(413,"Resume PDF must be 5 MB or smaller")
    try:
        reader=PdfReader(io.BytesIO(raw)); text="\n".join(page.extract_text() or "" for page in reader.pages)
    except Exception as exc: raise HTTPException(400,f"Could not read PDF: {exc}")
    skills=extract_skills(text)
    if not skills: raise HTTPException(422,"No supported technical skills were detected. Add a Skills section or use manual profile entry.")
    profile=Profile(name=file.filename.rsplit(".",1)[0],location=location,interests=[x.strip() for x in interests.split(",") if x.strip()],skills=skills)
    return run(profile,free_only)

@app.post("/api/simulate-skill")
def simulate_skill(req:SimulationRequest):
    p=req.profile; before=normalize_skills(p.skills); added=normalize_skills(before+[req.added_skill]); job=KB.job_by_id(req.job_id)
    if not job: raise HTTPException(404,"Job not found")
    old=score_job.invoke({"candidate_skills":before,"required_skills":job.required_skills}); new=score_job.invoke({"candidate_skills":added,"required_skills":job.required_skills})
    skill=req.added_skill
    local=[j for j in KB.jobs if j.location.lower()==p.location.lower()]
    unlocked=sum(1 for j in local if normalize_skill(skill).lower() in {normalize_skill(x).lower() for x in j.required_skills})
    return {"job_id":req.job_id,"skill":normalize_skills([skill])[0],"before":old,"after":new,"match_gain":new["match_score"]-old["match_score"],"local_jobs_with_skill":unlocked}
