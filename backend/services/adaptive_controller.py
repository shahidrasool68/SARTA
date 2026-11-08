"""Lightweight adaptive testing with conservative per-skill calibration."""
LEVELS = ("Easy", "Medium", "Hard")

def select_next_question(current_skill: str, current_difficulty: str, is_last_correct: bool,
                         streak: int, accuracy: float = None):
    if current_difficulty not in LEVELS:
        raise ValueError("Invalid difficulty")
    index = LEVELS.index(current_difficulty)
    # Require two consecutive successes; optionally require >= 60% running accuracy.
    if is_last_correct and streak >= 2 and (accuracy is None or accuracy >= 0.6):
        index = min(index+1, 2)
    elif not is_last_correct:
        index = max(index-1, 0)
    return {"skill": current_skill, "next_difficulty": LEVELS[index],
            "is_level_changed": LEVELS[index] != current_difficulty}
