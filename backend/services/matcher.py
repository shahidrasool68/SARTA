from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from scipy.optimize import linear_sum_assignment

def compute_gap_analysis(candidate_skills: list[str], job_skills: list[str], 
                         candidate_emb, job_emb, threshold=0.35):
    """
    Compare candidate and job skill profiles using cosine similarity.
    Calculates common, missing, and additional skills.
    """
    common_skills = []
    missing_skills = []
    additional_skills = []
    
    if len(job_skills) == 0:
        return {"match_score": 100.0, "common": [], "missing": [], "additional": candidate_skills}
        
    if len(candidate_skills) == 0:
        return {"match_score": 0.0, "common": [], "missing": job_skills, "additional": []}
        
    # Similarity matrix: Job Skills (rows) x Candidate Skills (cols)
    sim_matrix = cosine_similarity(job_emb, candidate_emb)
    
    # Use Hungarian Algorithm (linear_sum_assignment) to find optimal 1-to-1 matching
    # We want to maximize similarity, so we pass negative of sim_matrix to minimize cost
    row_ind, col_ind = linear_sum_assignment(-sim_matrix)
    
    matched_job_indices = set()
    matched_cand_indices = set()
    bipartite_matches = []
    
    for r, c in zip(row_ind, col_ind):
        score = float(sim_matrix[r][c])
        is_match = score >= threshold
        
        bipartite_matches.append({
            "resume_skill": candidate_skills[c],
            "jd_skill": job_skills[r],
            "similarity": score,
            "is_match": is_match
        })
        
        if is_match:
            common_skills.append({
                "required": job_skills[r],
                "candidate_has": candidate_skills[c],
                "similarity_score": score
            })
            matched_job_indices.add(r)
            matched_cand_indices.add(c)
            
    # Any job skill not matched above the threshold is missing
    for i, job_skill in enumerate(job_skills):
        if i not in matched_job_indices:
            missing_skills.append(job_skill)
            
    # Any candidate skill not matched above the threshold is additional
    for j, cand_skill in enumerate(candidate_skills):
        if j not in matched_cand_indices:
            additional_skills.append(cand_skill)
            
    match_score = (len(common_skills) / len(job_skills)) * 100 if job_skills else 0
    
    return {
        "match_score": round(match_score, 2),
        "common": common_skills,
        "missing": missing_skills,
        "additional": additional_skills,
        "bipartite_matches": bipartite_matches
    }
