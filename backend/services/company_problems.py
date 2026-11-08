"""Load company-specific LeetCode problems from the CSV dataset.

Uses `5. All.csv` inside each company folder (months-based CSVs are mostly empty).
Provides functions to load, filter, and sample problems for a target company.
"""

import csv
import os
import random
from pathlib import Path
from typing import List, Optional

# Path relative to the backend directory
_BASE_DIR = Path(__file__).resolve().parent.parent / "database" / "leetcode-company-wise-problems"


def _get_company_dir(company_name: str) -> Optional[Path]:
    """Find the company folder (case-insensitive match)."""
    if not _BASE_DIR.exists():
        return None
    # Direct name match first
    direct = _BASE_DIR / company_name
    if direct.is_dir():
        return direct
    # Case-insensitive fallback
    name_lower = company_name.strip().lower()
    for entry in _BASE_DIR.iterdir():
        if entry.is_dir() and entry.name.lower() == name_lower:
            return entry
    return None


def get_available_companies() -> List[str]:
    """Return list of all company names with problem data."""
    if not _BASE_DIR.exists():
        return []
    return sorted([
        d.name for d in _BASE_DIR.iterdir()
        if d.is_dir() and not d.name.startswith(".")
    ])


def load_company_problems(company_name: str) -> List[dict]:
    """Load all problems from a company's `5. All.csv`.
    
    Returns a list of dicts with keys:
        difficulty, title, frequency, acceptance_rate, link, topics
    """
    company_dir = _get_company_dir(company_name)
    if not company_dir:
        return []
    
    csv_path = company_dir / "5. All.csv"
    if not csv_path.exists():
        # Fallback: try any CSV
        csvs = list(company_dir.glob("*.csv"))
        if not csvs:
            return []
        csv_path = csvs[-1]  # Last one (usually the largest)
    
    problems = []
    try:
        with open(csv_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                problems.append({
                    "title": row.get("Title", "Unknown"),
                    "difficulty": row.get("Difficulty", "MEDIUM").upper(),
                    "frequency": float(row.get("Frequency", 0)),
                    "acceptance_rate": float(row.get("Acceptance Rate", 0)),
                    "link": row.get("Link", ""),
                    "topics": [t.strip() for t in row.get("Topics", "").split(",") if t.strip()],
                    "company": company_name,
                })
    except Exception as e:
        print(f"[company_problems] Error loading {csv_path}: {e}")
    
    return problems


def get_problems_by_difficulty(company_name: str, difficulty: str = None) -> List[dict]:
    """Get problems filtered by difficulty (EASY/MEDIUM/HARD)."""
    problems = load_company_problems(company_name)
    if difficulty:
        return [p for p in problems if p["difficulty"] == difficulty.upper()]
    return problems


def get_top_problems(company_name: str, n: int = 10, difficulty: str = None) -> List[dict]:
    """Get top N most frequently asked problems for a company.
    
    Sorted by frequency (descending). Optionally filtered by difficulty.
    """
    problems = get_problems_by_difficulty(company_name, difficulty)
    problems.sort(key=lambda p: p["frequency"], reverse=True)
    return problems[:n]


def sample_problems_for_assessment(company_name: str, n: int = 3) -> List[dict]:
    """Sample a diverse set of problems for coding assessment.
    
    Aims for a mix of difficulties, weighted by frequency.
    Returns at most `n` problems.
    """
    problems = load_company_problems(company_name)
    if not problems:
        return []
    
    # Aim for 1 easy, 1 medium, 1 hard if available
    by_diff = {"EASY": [], "MEDIUM": [], "HARD": []}
    for p in problems:
        diff = p["difficulty"]
        if diff in by_diff:
            by_diff[diff].append(p)
    
    selected = []
    for diff in ["EASY", "MEDIUM", "HARD"]:
        pool = by_diff.get(diff, [])
        if pool:
            # Prefer higher-frequency problems
            pool.sort(key=lambda p: p["frequency"], reverse=True)
            top_pool = pool[:max(5, len(pool) // 4)]  # Top 25% or at least 5
            selected.append(random.choice(top_pool))
    
    # Fill remaining slots if needed
    remaining = [p for p in problems if p not in selected]
    while len(selected) < n and remaining:
        pick = random.choice(remaining)
        selected.append(pick)
        remaining.remove(pick)
    
    return selected[:n]


def get_company_problem_stats(company_name: str) -> dict:
    """Get summary statistics about a company's problem bank."""
    problems = load_company_problems(company_name)
    if not problems:
        return {"total": 0, "easy": 0, "medium": 0, "hard": 0, "top_topics": []}
    
    easy = sum(1 for p in problems if p["difficulty"] == "EASY")
    medium = sum(1 for p in problems if p["difficulty"] == "MEDIUM")
    hard = sum(1 for p in problems if p["difficulty"] == "HARD")
    
    # Count topic frequencies
    topic_counts: dict = {}
    for p in problems:
        for t in p["topics"]:
            topic_counts[t] = topic_counts.get(t, 0) + 1
    top_topics = sorted(topic_counts, key=topic_counts.get, reverse=True)[:10]
    
    return {
        "total": len(problems),
        "easy": easy,
        "medium": medium,
        "hard": hard,
        "top_topics": top_topics,
    }

