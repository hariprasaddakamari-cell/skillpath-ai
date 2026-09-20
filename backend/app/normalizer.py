import re

ALIASES = {
    "springboot": "Spring Boot", "spring boot framework": "Spring Boot",
    "spring": "Spring", "postgres": "PostgreSQL", "postgres db": "PostgreSQL",
    "postgresql database": "PostgreSQL", "js": "JavaScript", "reactjs": "React",
    "rest": "REST API", "restful api": "REST API", "github actions": "CI/CD",
    "cicd": "CI/CD", "ci cd": "CI/CD", "k8s": "Kubernetes", "aws cloud": "AWS",
    "core java": "Java", "data structures & algorithms": "Data Structures",
}

def normalize_skill(skill: str) -> str:
    s = re.sub(r"\s+", " ", skill.strip())
    key = re.sub(r"[^a-z0-9+#]+", " ", s.lower()).strip()
    return ALIASES.get(key, s)

def normalize_skills(skills: list[str]) -> list[str]:
    out=[]; seen=set()
    for skill in skills:
        if not skill: continue
        n=normalize_skill(skill)
        k=n.lower()
        if k not in seen:
            seen.add(k); out.append(n)
    return out
