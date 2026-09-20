from app.normalizer import normalize_skills

def test_aliases():
    assert normalize_skills(["springboot", "postgres", "js"]) == ["Spring Boot", "PostgreSQL", "JavaScript"]
