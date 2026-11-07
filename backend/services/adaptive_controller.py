def select_next_question(current_skill: str, 
                         current_difficulty: str, 
                         is_last_correct: bool, 
                         streak: int):
    """
    Intelligence Layer: Adaptive Difficulty Controller.
    Adjusts the difficulty of the next question based on running accuracy 
    for a SPECIFIC skill, bypassing the need for a massive IRT item bank.
    
    Difficulty states: 'Easy', 'Medium', 'Hard'
    """
    difficulty_levels = ['Easy', 'Medium', 'Hard']
    current_idx = difficulty_levels.index(current_difficulty)
    
    next_idx = current_idx
    
    if is_last_correct:
        # If candidate got it right and has a streak of 2, bump difficulty up
        if streak >= 2 and current_idx < len(difficulty_levels) - 1:
            next_idx += 1
    else:
        # If candidate got it wrong, immediately drop difficulty down to build confidence/find baseline
        if current_idx > 0:
            next_idx -= 1
            
    next_difficulty = difficulty_levels[next_idx]
    
    return {
        "skill": current_skill,
        "next_difficulty": next_difficulty,
        "is_level_changed": next_idx != current_idx
    }
