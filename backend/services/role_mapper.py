# A predefined dictionary mapping common job roles to a list of core technical skills.
# This serves as the taxonomy profile for role identification and topic selection.

ROLE_PROFILES = {
    "Frontend Developer": [
        "React", "Next.js", "JavaScript", "TypeScript", "HTML", "CSS", 
        "Redux", "TailwindCSS", "Webpack", "Vue", "Angular", "Bootstrap", "jQuery"
    ],
    "Backend Developer": [
        "Python", "FastAPI", "Django", "Node.js", "Express", 
        "PostgreSQL", "MySQL", "MongoDB", "Redis", "Docker", "REST API", "GraphQL", "Microservices"
    ],
    "Full Stack Developer": [
        "JavaScript", "TypeScript", "React", "Node.js", "Express", "Python",
        "SQL", "MongoDB", "Git", "Docker", "REST API", "HTML", "CSS"
    ],
    "Data Scientist / ML Engineer": [
        "Python", "Pandas", "NumPy", "Scikit-learn", "TensorFlow", 
        "PyTorch", "SQL", "Statistics", "Machine Learning", "Deep Learning", "NLP"
    ],
    "DevOps / Cloud Engineer": [
        "AWS", "Docker", "Kubernetes", "Linux", "CI/CD", "Terraform",
        "Ansible", "GitHub Actions", "Jenkins", "Bash", "Nginx", "GCP", "Azure"
    ]
}

ROLE_ASSESSMENT_TOPICS = {
    "Backend Developer": ["System Design", "OS", "OOP", "Computer Networks"],
    "Frontend Developer": ["OOP", "Computer Networks", "System Design", "Aptitude"],
    "Full Stack Developer": ["System Design", "OOP", "OS", "Computer Networks"],
    "Data Scientist / ML Engineer": ["OOP", "OS", "System Design", "Aptitude"],
    "DevOps / Cloud Engineer": ["OS", "Computer Networks", "System Design", "Aptitude"],
}

def infer_role_skills(role_name: str) -> list[str]:
    """
    Given a role name (e.g. 'Frontend Developer'), return the predefined 
    list of required skills. If the role is unknown, return an empty list.
    """
    role_name = role_name.strip().lower()
    for role, skills in ROLE_PROFILES.items():
        if role.lower() == role_name:
            return skills
    return []

def infer_role_from_skills(candidate_skills: list[str]) -> dict:
    """
    Section 4.3 Role Mapping:
    Compares normalized candidate skills against predefined role profiles to 
    identify the most suitable role and select relevant assessment topics.
    """
    if not candidate_skills:
        default_role = "Backend Developer"
        return {
            "role": default_role,
            "confidence": 0.0,
            "matched_skills": [],
            "missing_core_skills": ROLE_PROFILES[default_role][:4],
            "assessment_skills": ROLE_ASSESSMENT_TOPICS[default_role]
        }
    
    cand_lower = {s.lower() for s in candidate_skills}
    best_role = "Backend Developer"
    best_overlap = -1
    best_matched = []
    best_missing = []
    
    for role, req_skills in ROLE_PROFILES.items():
        matched = [s for s in req_skills if s.lower() in cand_lower]
        missing = [s for s in req_skills if s.lower() not in cand_lower]
        overlap_score = len(matched) / len(req_skills) if req_skills else 0
        
        if len(matched) > best_overlap:
            best_overlap = len(matched)
            best_role = role
            best_matched = matched
            best_missing = missing

    confidence = round((len(best_matched) / len(ROLE_PROFILES[best_role])) * 100, 1) if best_role in ROLE_PROFILES else 0
    
    # Adaptive Assessment Targets: Map inferred role to calibrated CS foundation domains
    # (OOP, OS, System Design, Computer Networks, Aptitude from the curated 300-question PDF bank)
    assessment_skills = ROLE_ASSESSMENT_TOPICS.get(
        best_role, ["OOP", "OS", "System Design", "Computer Networks"]
    )

    return {
        "role": best_role,
        "confidence": confidence,
        "matched_skills": best_matched,
        "missing_core_skills": best_missing,
        "assessment_skills": assessment_skills
    }
