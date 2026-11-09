"""PDF Question Bank Extractor for SARTA.

Extracts all 300 curated questions across the 5 domain PDFs:
  - OS_questions.pdf (Operating Systems)
  - CN_questions.pdf (Computer Networks)
  - OOP_questions.pdf (Object-Oriented Programming)
  - LLD_HLD_questions.pdf (System Design / LLD & HLD)
  - Aptitude_questions.pdf (Aptitude & Logical Reasoning)

Each question has:
  - question text
  - 4 options (A, B, C, D)
  - correct answer (full string matching the correct option)
  - difficulty score (0.5 to 10.0 in 0.5 steps)
  - calibrated difficulty level:
      * Easy   (0.5 <= diff <= 3.5)  -> 21 questions per topic
      * Medium (4.0 <= diff <= 7.0)  -> 21 questions per topic
      * Hard   (7.5 <= diff <= 10.0) -> 18 questions per topic

Exports to:
  1. backend/database/parsed_pdf_questions.json (local cache for instant offline access)
  2. MongoDB 'questions' collection (if MongoDB is reachable)
"""

import json
import os
import re
import sys
from pathlib import Path

# Add backend root to path
_BACKEND_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_BACKEND_DIR))

try:
    import pdfplumber
except ImportError:
    pdfplumber = None

from config import MONGO_URI, MONGO_DB_NAME

PDF_DIR = _BACKEND_DIR / "database" / "pdfs"
JSON_CACHE_PATH = _BACKEND_DIR / "database" / "parsed_pdf_questions.json"

PDF_SKILL_MAP = {
    "OS_questions.pdf": "OS",
    "CN_questions.pdf": "Computer Networks",
    "OOP_questions.pdf": "OOP",
    "LLD_HLD_questions.pdf": "System Design",
    "Aptitude_questions.pdf": "Aptitude",
}


def score_to_difficulty(score: float) -> str:
    """Map 0.5-10.0 numerical difficulty to Easy / Medium / Hard."""
    if score <= 3.5:
        return "Easy"
    elif score <= 7.0:
        return "Medium"
    else:
        return "Hard"


def extract_all_pdf_questions() -> dict:
    """Parse all 5 question PDFs and return a structured dictionary."""
    if not pdfplumber:
        raise RuntimeError("pdfplumber is required to extract PDF questions.")

    if not PDF_DIR.exists():
        raise FileNotFoundError(f"PDF directory not found: {PDF_DIR}")

    results = {}

    for filename, skill_name in PDF_SKILL_MAP.items():
        pdf_path = PDF_DIR / filename
        if not pdf_path.exists():
            print(f"[pdf_extractor] Warning: {filename} not found at {pdf_path}")
            continue

        text = ""
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                extracted = page.extract_text()
                if extracted:
                    text += extracted + "\n"

        # Match questions: Q<num>. [Difficulty: <diff>] <question text>
        # followed by A) ... B) ... C) ... D) ... Answer: <letter>
        blocks = re.split(r'\n(?=Q\d+\.\s*\[Difficulty:)', text)
        questions_by_level = {"Easy": [], "Medium": [], "Hard": []}

        for block in blocks:
            match = re.search(
                r'Q(\d+)\.\s*\[Difficulty:\s*([\d\.]+)\]\s*(.*?)\n\s*A\)\s*(.*?)\n\s*B\)\s*(.*?)\n\s*C\)\s*(.*?)\n\s*D\)\s*(.*?)\n\s*Answer:\s*([A-D])',
                block,
                re.DOTALL,
            )
            if not match:
                continue

            q_num, diff_str, q_text, opt_a, opt_b, opt_c, opt_d, ans_letter = match.groups()
            diff_score = float(diff_str)
            level = score_to_difficulty(diff_score)

            options = [opt_a.strip(), opt_b.strip(), opt_c.strip(), opt_d.strip()]
            opt_map = {"A": options[0], "B": options[1], "C": options[2], "D": options[3]}
            correct_val = opt_map.get(ans_letter.strip(), options[0])

            q_obj = {
                "question_num": int(q_num),
                "difficulty_score": diff_score,
                "difficulty": level,
                "question": q_text.strip(),
                "options": options,
                "correct_answer": correct_val,
                "answer_letter": ans_letter.strip(),
            }
            questions_by_level[level].append(q_obj)

        total_extracted = sum(len(q_list) for q_list in questions_by_level.values())
        print(f"[pdf_extractor] {skill_name}: extracted {total_extracted} questions "
              f"({len(questions_by_level['Easy'])} Easy, "
              f"{len(questions_by_level['Medium'])} Medium, "
              f"{len(questions_by_level['Hard'])} Hard)")

        results[skill_name] = questions_by_level

    # Save to JSON cache
    try:
        with open(JSON_CACHE_PATH, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        print(f"[pdf_extractor] Saved structured questions to {JSON_CACHE_PATH}")
    except Exception as e:
        print(f"[pdf_extractor] Failed to save JSON cache: {e}")

    return results


def load_cached_pdf_questions() -> dict:
    """Load previously parsed PDF questions from JSON cache, or extract if cache is missing."""
    if JSON_CACHE_PATH.exists():
        try:
            with open(JSON_CACHE_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return extract_all_pdf_questions()


def sync_to_mongodb():
    """Extract PDF questions and sync them directly to MongoDB."""
    from pymongo import MongoClient

    questions_data = load_cached_pdf_questions()
    try:
        client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=8000, connectTimeoutMS=8000)
        db = client[MONGO_DB_NAME]
        col = db["questions"]

        total_synced = 0
        for skill, levels in questions_data.items():
            for level, q_list in levels.items():
                for idx, q in enumerate(q_list):
                    q_id = f"{skill}:{level}:{idx}"
                    doc = {
                        "_id": q_id,
                        "skill": skill,
                        "difficulty": level,
                        "difficulty_score": q.get("difficulty_score", 5.0),
                        "question": q["question"],
                        "options": q["options"],
                        "correct_answer": q["correct_answer"],
                    }
                    col.update_one({"_id": q_id}, {"$set": doc}, upsert=True)
                    total_synced += 1

        print(f"[pdf_extractor] Successfully synced {total_synced} PDF questions to MongoDB ({MONGO_DB_NAME}.questions)")
    except Exception as e:
        print(f"[pdf_extractor] MongoDB unavailable, questions remain cached locally in JSON ({e})")


if __name__ == "__main__":
    extract_all_pdf_questions()
    sync_to_mongodb()
