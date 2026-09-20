from typing import TypedDict, Any
from langgraph.graph import StateGraph, START, END
from langchain_core.tools import tool
from .normalizer import normalize_skills, normalize_skill

class CareerState(TypedDict, total=False):
    profile: dict[str, Any]; free_only: bool; trace: list[dict[str, Any]]
    matched_jobs: list[dict[str, Any]]; gaps: dict[str, list[str]]
    courses: dict[str, list[dict[str, Any]]]; roadmap: dict[str, Any]
    sources: list[dict[str, Any]]; kb: Any

def log(state, agent, status, detail, tool_name=None):
    trace=list(state.get("trace",[])); row={"agent":agent,"status":status,"detail":detail}
    if tool_name: row["tool"]=tool_name
    trace.append(row); return trace

@tool
def normalize_profile_skills(skills: list[str]) -> list[str]:
    """Normalize aliases such as SpringBoot/Postgres/JS into canonical skills."""
    return normalize_skills(skills)

@tool
def score_job(candidate_skills: list[str], required_skills: list[str]) -> dict:
    """Deterministically score required skill coverage and return matched/missing skills."""
    cand={normalize_skill(x).lower() for x in candidate_skills}
    req=[normalize_skill(x) for x in required_skills]
    matched=[x for x in req if x.lower() in cand]
    missing=[x for x in req if x.lower() not in cand]
    return {"matched_skills":matched,"missing_skills":missing,"match_score":round(100*len(matched)/max(1,len(req)))}

@tool
def opportunity_count(jobs: list[dict], skill: str, location: str) -> int:
    """Count local curated jobs whose requirements include the requested skill."""
    s=normalize_skill(skill).lower(); loc=location.lower().strip()
    return sum(1 for j in jobs if (not loc or j["location"].lower()==loc) and any(normalize_skill(x).lower()==s for x in j["required_skills"]))

@tool
def calculate_time_and_cost(courses: list[dict]) -> dict:
    """Calculate sequential total duration and total course cost."""
    return {"weeks":sum(int(c["duration_weeks"]) for c in courses),"cost":sum(int(c["cost"]) for c in courses)}

def profile_agent(state):
    p=dict(state["profile"]); p["skills"]=normalize_profile_skills.invoke({"skills":p.get("skills",[])})
    return {"profile":p,"trace":log(state,"Profile Parser","complete",f"Normalized {len(p['skills'])} canonical skills","normalize_profile_skills")}

def job_agent(state):
    p=state["profile"]; query=" ".join(p.get("skills",[])+p.get("interests",[]))
    hits=state["kb"].search_jobs(query,p.get("location",""),8); jobs=[]; sources=[]
    for hit in hits:
        raw=dict(hit["item"]); scored=score_job.invoke({"candidate_skills":p["skills"],"required_skills":raw["required_skills"]})
        raw.update(scored); raw["retrieval_score"]=round(hit["score"],4); raw["evidence_chunk"]=hit["chunk"]
        jobs.append(raw); sources.append({"type":"job","id":raw["id"],"title":raw["title"],"location":raw["location"],"retrieval_score":round(hit["score"],4),"evidence":hit["chunk"]})
    jobs.sort(key=lambda x:(x["match_score"],x["retrieval_score"]),reverse=True)
    return {"matched_jobs":jobs,"sources":sources,"trace":log(state,"Job Retrieval + Matching","complete",f"Retrieved {len(jobs)} local/semantic opportunities","score_job")}

def gap_agent(state):
    gaps={j["id"]:j["missing_skills"] for j in state["matched_jobs"]}; total=sum(map(len,gaps.values()))
    return {"gaps":gaps,"trace":log(state,"Gap Analysis","complete",f"Found {total} job-specific skill gaps")}

def course_agent(state):
    out={}; sources=list(state.get("sources",[]))
    for job in state["matched_jobs"]:
        choices=[]
        for skill in job["missing_skills"]:
            for hit in state["kb"].search_courses(skill,state.get("free_only",False),5):
                raw=dict(hit["item"]); raw.update({"skill":skill,"retrieval_score":round(hit["score"],4),"evidence_chunk":hit["chunk"]})
                choices.append(raw); sources.append({"type":"course","id":raw["id"],"title":raw["title"],"skill":skill,"retrieval_score":round(hit["score"],4),"evidence":hit["chunk"]})
        # Deduplicate, retain best semantic score.
        best={}
        for c in choices:
            if c["id"] not in best or c["retrieval_score"]>best[c["id"]]["retrieval_score"]: best[c["id"]]=c
        out[job["id"]]=list(best.values())
    return {"courses":out,"sources":sources,"trace":log(state,"Course Retrieval + Recommendation","complete",f"Grounded recommendations for {len(out)} jobs")}

def roadmap_agent(state):
    jobs=state["matched_jobs"]
    if not jobs: return {"roadmap":{"weeks":0,"cost":0,"target_job":None,"steps":[]},"trace":log(state,"Time-to-Ready + ROI","complete","No matching jobs")}
    target=jobs[0]; choices=state["courses"].get(target["id"],[]); by_skill={}
    for c in choices:
        s=normalize_skill(c["skill"]).lower()
        if s not in by_skill or (c["duration_weeks"],c["cost"],-c["retrieval_score"])<(by_skill[s]["duration_weeks"],by_skill[s]["cost"],-by_skill[s]["retrieval_score"]): by_skill[s]=c
    steps=list(by_skill.values()); totals=calculate_time_and_cost.invoke({"courses":steps})
    opportunities=[]
    all_jobs=[j.model_dump() for j in state["kb"].jobs]
    for skill in target["missing_skills"]:
        opportunities.append({"skill":skill,"jobs_unlocked":opportunity_count.invoke({"jobs":all_jobs,"skill":skill,"location":state["profile"].get("location","")})})
    opportunities.sort(key=lambda x:x["jobs_unlocked"],reverse=True)
    roadmap={"target_job":target["title"],"target_job_id":target["id"],"weeks":totals["weeks"],"cost":totals["cost"],"steps":steps,"missing_skills":target["missing_skills"],"opportunities":opportunities,"potential_skill_coverage":len(steps)}
    return {"roadmap":roadmap,"trace":log(state,"Time-to-Ready + ROI","complete",f"Calculated {totals['weeks']} weeks, ₹{totals['cost']} and ranked opportunity gain","calculate_time_and_cost")}

def build_graph(kb):
    g=StateGraph(CareerState)
    for name,fn in [("profile",profile_agent),("jobs",job_agent),("gaps",gap_agent),("courses",course_agent),("roadmap",roadmap_agent)]: g.add_node(name,fn)
    g.add_edge(START,"profile"); g.add_edge("profile","jobs"); g.add_edge("jobs","gaps"); g.add_edge("gaps","courses"); g.add_edge("courses","roadmap"); g.add_edge("roadmap",END)
    return g.compile()
