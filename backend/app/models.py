from typing import Any
from pydantic import BaseModel, Field

class Profile(BaseModel):
    name: str = "Candidate"
    education: str = "B.Tech"
    location: str = "Hyderabad"
    interests: list[str] = Field(default_factory=lambda: ["Backend Development"])
    skills: list[str] = Field(default_factory=list)

class AnalyzeRequest(BaseModel):
    profile: Profile
    free_only: bool = False

class SimulationRequest(BaseModel):
    profile: Profile
    job_id: str
    added_skill: str
    free_only: bool = False

class Job(BaseModel):
    id: str
    title: str
    company: str
    location: str
    required_skills: list[str]
    preferred_skills: list[str] = []
    experience: str = ""
    salary_min: int = 0
    salary_max: int = 0
    description: str = ""

class Course(BaseModel):
    id: str
    title: str
    provider: str
    skills: list[str]
    duration_weeks: int
    cost: int
    level: str
    url: str

class AnalyzeResponse(BaseModel):
    profile: dict[str, Any]
    jobs: list[dict[str, Any]]
    skill_gaps: dict[str, list[str]]
    courses: dict[str, list[dict[str, Any]]]
    roadmap: dict[str, Any]
    trace: list[dict[str, Any]]
    sources: list[dict[str, Any]]
