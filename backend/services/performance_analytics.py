def generate_performance_report(assessment_responses: list[dict], coding_results: list[dict] = None) -> dict:
    """
    Intelligence Layer & Output Layer: Performance Analytics (Section 4.7)
    Aggregates skill-wise analysis, scoring, difficulty progression, 
    coding performance, and generates an explainable evaluation report.
    
    assessment_responses format:
    [{'skill': 'Python', 'difficulty': 'Medium', 'is_correct': True, 'question_id': '...'}, ...]
    
    coding_results format:
    [{'title': 'Two Sum', 'difficulty': 'Easy', 'passed': True, 'time': '0.04s', 'language': 'Python'}, ...]
    """
    skill_stats = {}
    diff_weights = {"Easy": 1, "Medium": 2, "Hard": 3}
    difficulty_progression = []

    for resp in assessment_responses:
        skill = resp.get('skill', 'General')
        diff = resp.get('difficulty', 'Medium')
        is_corr = bool(resp.get('is_correct', False))
        
        difficulty_progression.append({
            "skill": skill,
            "difficulty": diff,
            "is_correct": is_corr
        })

        if skill not in skill_stats:
            skill_stats[skill] = {
                "total": 0,
                "correct": 0,
                "highest_difficulty_passed": None,
                "accuracy": 0.0,
                "difficulties_tested": []
            }
            
        stats = skill_stats[skill]
        stats["total"] += 1
        if diff not in stats["difficulties_tested"]:
            stats["difficulties_tested"].append(diff)

        if is_corr:
            stats["correct"] += 1
            curr_highest = stats["highest_difficulty_passed"]
            if not curr_highest or diff_weights.get(diff, 1) > diff_weights.get(curr_highest, 1):
                stats["highest_difficulty_passed"] = diff

    # Calculate percentages per skill
    strengths = []
    weaknesses = []
    needs_practice = []

    for skill, stats in skill_stats.items():
        acc = round((stats["correct"] / stats["total"]) * 100, 1) if stats["total"] > 0 else 0.0
        stats["accuracy"] = acc
        if not stats["highest_difficulty_passed"]:
            stats["highest_difficulty_passed"] = "None"

        if acc >= 66.0:
            strengths.append(skill)
        elif acc < 50.0:
            weaknesses.append(skill)
        else:
            needs_practice.append(skill)

    # Coding results aggregation
    coding_results = coding_results or []
    coding_total = len(coding_results)
    coding_passed = sum(1 for c in coding_results if c.get('passed', False))
    tested_cases = sum(int(c.get("test_cases_total", 0)) for c in coding_results)
    passed_cases = sum(int(c.get("test_cases_passed", 0)) for c in coding_results)
    coding_score = round(100 * passed_cases / tested_cases, 1) if tested_cases else (round(100 * coding_passed / coding_total, 1) if coding_total else 0.0)

    # MCQ overall score
    total_mcq_correct = sum(s["correct"] for s in skill_stats.values())
    total_mcq_questions = len(assessment_responses)
    mcq_score = round((total_mcq_correct / total_mcq_questions * 100), 1) if total_mcq_questions > 0 else 0.0

    # Composite overall score
    if coding_total > 0 and total_mcq_questions > 0:
        overall_percentage = round((0.6 * mcq_score) + (0.4 * coding_score), 1)
    elif total_mcq_questions > 0:
        overall_percentage = mcq_score
    elif coding_total > 0:
        overall_percentage = coding_score
    else:
        overall_percentage = 0.0

    # Recommendation
    if overall_percentage >= 75.0:
        recommendation = "Suitable"
        recommendation_text = "Demonstrates strong conceptual mastery and adaptive proficiency across assessed competencies."
    elif overall_percentage >= 50.0:
        recommendation = "Needs Improvement"
        recommendation_text = "Good foundational competencies with targeted skill gaps identified in advanced difficulty items."
    else:
        recommendation = "Not Suitable"
        recommendation_text = "Significant gaps observed in core role prerequisites and problem-solving accuracy."

    return {
        "overall_percentage": overall_percentage,
        "mcq_score": mcq_score,
        "coding_score": coding_score,
        "total_mcqs": total_mcq_questions,
        "total_mcqs_correct": total_mcq_correct,
        "coding_summary": {
            "total": coding_total,
            "passed": coding_passed,
            "score": coding_score,
            "test_cases_passed": passed_cases,
            "test_cases_total": tested_cases,
            "submissions": coding_results
        },
        "skill_breakdown": skill_stats,
        "strengths": strengths,
        "weaknesses": weaknesses,
        "needs_practice": needs_practice,
        "difficulty_progression": difficulty_progression,
        "final_recommendation": recommendation,
        "recommendation_text": recommendation_text
    }
