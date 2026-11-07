def generate_assessment_blueprint(candidate_skills: list[str], 
                                  job_skills: list[str], 
                                  gap_analysis: dict, 
                                  company_profile: dict = None):
    """
    Generates a 3-part assessment blueprint (Core Skills, Gap Verification, CS Fundamentals).
    Incorporates the Company Assessment Profile to determine difficulty and length.
    """
    if not company_profile:
        company_profile = {
            "mcq_difficulty": "Medium",
            "coding_difficulty": "Medium",
            "preferred_topics": ["Data Structures", "OOP", "OS", "Computer Networks"],
            "max_questions": 10
        }
        
    common_skills = [item['candidate_has'] for item in gap_analysis.get('common', [])]
    missing_skills = gap_analysis.get('missing', [])
    
    # 1. Core Skills (Intersecting skills between Candidate and Job)
    core_assessment = {
        "topics": common_skills[:4] if common_skills else ["Python", "JavaScript"],
        "priority": "High"
    }
    
    # 2. Skill Gap Verification (Skills missing from resume but required by job)
    gap_assessment = {
        "topics": missing_skills[:3],
        "priority": "Medium"
    }
    
    # 3. CS Fundamentals (Role independent)
    fundamentals_assessment = {
        "topics": company_profile.get("preferred_topics", ["OOP", "OS", "Computer Networks"]),
        "priority": "Standard"
    }
    
    blueprint = {
        "target_mcq_difficulty": company_profile["mcq_difficulty"],
        "target_coding_difficulty": company_profile["coding_difficulty"],
        "max_questions_allowed": company_profile["max_questions"],
        "structure": {
            "core_skills": core_assessment,
            "skill_gap_verification": gap_assessment,
            "fundamentals": fundamentals_assessment
        }
    }
    
    return blueprint

def generate_blueprint_from_skills(candidate_skills: list[str], role: str = "Backend Developer", missing_skills: list[str] = None) -> dict:
    """
    Generate an assessment blueprint directly from candidate skills and inferred role.
    """
    missing_skills = missing_skills or []
    common = candidate_skills[:4] if candidate_skills else ["Python"]
    
    gap_mock = {
        "common": [{"candidate_has": s} for s in common],
        "missing": missing_skills[:3]
    }
    return generate_assessment_blueprint(candidate_skills, [], gap_mock)
