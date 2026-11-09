"""LLM-Powered Question Generator for SARTA.

Dynamically generates calibrated MCQ questions for any technical topic from a Job Description (JD).
Uses calibrated reference questions from SARTA's 300-question PDF bank as few-shot exemplars,
ensuring consistent difficulty rating (0.5 to 10.0 scale) and realistic distractors.

Supports:
1. Google Gemini (GEMINI_API_KEY)
2. Groq (GROQ_API_KEY — free & ultra-fast)
3. OpenAI / compatible (OPENAI_API_KEY / OPENAI_BASE_URL)
4. Graceful offline fallback to curated static bank
"""

import json
import logging
import os
import re
import time
from typing import Any, Dict, List, Optional
import httpx

from config import GEMINI_API_KEY, OPENAI_API_KEY, GROQ_API_KEY, OPENAI_BASE_URL

logger = logging.getLogger("sarta.llm_generator")

# ── Reference Calibrated Few-Shot Exemplars ─────────────────────────────
# Real calibrated questions from SARTA's PDF bank used to guide LLM style & difficulty.
REFERENCE_EXEMPLARS = {
    "Easy": {
        "difficulty_range": "0.5 - 3.5",
        "sample": {
            "question": "Which layer of the OSI model does the TCP protocol belong to?",
            "options": ["Transport Layer", "Network Layer", "Application Layer", "Data Link Layer"],
            "correct_answer": "Transport Layer",
            "difficulty_score": 1.5,
        }
    },
    "Medium": {
        "difficulty_range": "4.0 - 7.0",
        "sample": {
            "question": "What is the primary difference between optimistic and pessimistic locking in database transactions?",
            "options": [
                "Optimistic locking checks for conflicts at commit time via versioning; pessimistic locking acquires exclusive locks up front",
                "Optimistic locking locks rows permanently; pessimistic locking never locks",
                "Optimistic locking is only used in NoSQL key-value stores",
                "There is no difference; they are synonymous"
            ],
            "correct_answer": "Optimistic locking checks for conflicts at commit time via versioning; pessimistic locking acquires exclusive locks up front",
            "difficulty_score": 5.5,
        }
    },
    "Hard": {
        "difficulty_range": "7.5 - 10.0",
        "sample": {
            "question": "In TCP Congestion Control, how is congestion window (cwnd) adjusted during the Fast Recovery phase upon receiving three duplicate ACKs?",
            "options": [
                "ssthresh is set to half of cwnd, cwnd is set to ssthresh + 3 MSS, and cwnd grows linearly per additional duplicate ACK",
                "cwnd is immediately reset to 1 MSS and slow start restarts unconditionally",
                "cwnd is doubled unconditionally without altering ssthresh",
                "The connection is terminated and re-established with a fresh SYN"
            ],
            "correct_answer": "ssthresh is set to half of cwnd, cwnd is set to ssthresh + 3 MSS, and cwnd grows linearly per additional duplicate ACK",
            "difficulty_score": 8.5,
        }
    }
}


def _get_active_provider() -> Optional[str]:
    """Identify which LLM API key is configured."""
    if GEMINI_API_KEY:
        return "gemini"
    if GROQ_API_KEY:
        return "groq"
    if OPENAI_API_KEY:
        return "openai"
    return None


def _build_prompt(topic: str, difficulty: str, count: int = 3) -> str:
    exemplar = REFERENCE_EXEMPLARS.get(difficulty, REFERENCE_EXEMPLARS["Medium"])
    diff_range = exemplar["difficulty_range"]
    sample_json = json.dumps(exemplar["sample"], indent=2)

    prompt = f"""You are SARTA's Chief Technical Psychometrics Engine.
Your task is to generate {count} rigorous, calibrated Multiple Choice Questions (MCQs) for the technical topic: "{topic}".

Target Difficulty Level: {difficulty} (Numerical Rating Range: {diff_range} out of 10.0).

CALIBRATION CRITERIA:
- Easy (0.5 - 3.5): Fundamental concepts, standard API syntax, common CLI flags, core definitions.
- Medium (4.0 - 7.0): Implementation mechanics, architectural trade-offs, concurrency/state issues, complexity analysis.
- Hard (7.5 - 10.0): Deep runtime internals, memory layouts, race conditions, distributed system failure modes, low-level protocols.

REFERENCE FORMAT AND STANDARD (from SARTA's calibrated assessment bank):
{sample_json}

REQUIREMENTS:
1. Exactly 4 plausible, unambiguous options per question.
2. The correct_answer MUST match one of the 4 options character-for-character.
3. Distractors must be technically plausible (not trivial nonsense).
4. Assign an exact `difficulty_score` as a float between {diff_range}.
5. Return ONLY a valid JSON array of objects. No markdown formatting, no conversational text.

Generate {count} questions for "{topic}" at {difficulty} level:"""
    return prompt


def _parse_llm_json(raw_text: str) -> List[Dict[str, Any]]:
    """Clean markdown codeblocks and parse JSON array."""
    cleaned = raw_text.strip()
    if cleaned.startswith("```"):
        cleaned = re.sub(r"^```(?:json)?\s*", "", cleaned)
        cleaned = re.sub(r"\s*```$", "", cleaned)
    try:
        data = json.loads(cleaned)
        if isinstance(data, dict) and "questions" in data:
            data = data["questions"]
        if isinstance(data, list):
            valid = []
            for item in data:
                if (
                    isinstance(item, dict)
                    and "question" in item
                    and "options" in item
                    and "correct_answer" in item
                    and len(item["options"]) == 4
                    and item["correct_answer"] in item["options"]
                ):
                    valid.append(item)
            return valid
    except Exception as e:
        logger.warning(f"Could not parse LLM response as JSON: {e}")
    return []


async def _call_gemini(prompt: str) -> str:
    """Call Google Gemini REST API using httpx with automatic model fallback."""
    models = ["gemini-2.0-flash", "gemini-1.5-flash"]
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "temperature": 0.3,
            "responseMimeType": "application/json"
        }
    }
    last_err = None
    async with httpx.AsyncClient(timeout=25.0) as client:
        for model in models:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={GEMINI_API_KEY}"
            try:
                resp = await client.post(url, json=payload)
                if resp.status_code == 200:
                    data = resp.json()
                    return data["candidates"][0]["content"]["parts"][0]["text"]
                last_err = f"HTTP {resp.status_code}: {resp.text}"
            except Exception as e:
                last_err = str(e)
    raise RuntimeError(f"Gemini API call failed: {last_err}")


async def _call_groq_or_openai(prompt: str, provider: str) -> str:
    """Call Groq or OpenAI chat completions API."""
    if provider == "groq":
        base_url = "https://api.groq.com/openai/v1"
        api_key = GROQ_API_KEY
        model = "llama-3.3-70b-versatile"
    else:
        base_url = OPENAI_BASE_URL
        api_key = OPENAI_API_KEY
        model = "gpt-4o-mini"

    url = f"{base_url}/chat/completions"
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": "You are a professional computer science psychometrics assessment system. Return pure JSON only."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.3,
        "response_format": {"type": "json_object"}
    }
    async with httpx.AsyncClient(timeout=20.0) as client:
        resp = await client.post(url, headers=headers, json=payload)
        resp.raise_for_status()
        data = resp.json()
        return data["choices"][0]["message"]["content"]


async def generate_jd_questions(
    topic: str,
    difficulty: str = "Medium",
    count: int = 3,
    save_to_mongo: bool = True
) -> List[Dict[str, Any]]:
    """Generate calibrated questions for a JD topic using LLM with few-shot exemplars.
    
    If LLM is offline or no key is present, returns an empty list (caller falls back to local bank).
    If questions are generated, they are cached in MongoDB Atlas so future sessions reuse them.
    """
    provider = _get_active_provider()
    if not provider:
        return []

    prompt = _build_prompt(topic, difficulty, count)
    try:
        if provider == "gemini":
            raw_text = await _call_gemini(prompt)
        else:
            raw_text = await _call_groq_or_openai(prompt, provider)

        questions = _parse_llm_json(raw_text)
        if not questions:
            return []

        # If MongoDB is reachable, persist the generated questions for instant future reuse
        if save_to_mongo:
            try:
                from database.mongo_skill_tree import get_db
                db = get_db()
                q_col = db["questions"]
                timestamp = int(time.time())
                for i, q in enumerate(questions):
                    doc_id = f"{topic}:{difficulty}:llm_{timestamp}_{i}"
                    doc = {
                        "_id": doc_id,
                        "skill": topic,
                        "difficulty": difficulty,
                        "difficulty_score": float(q.get("difficulty_score", 5.0)),
                        "question": q["question"],
                        "options": q["options"],
                        "correct_answer": q["correct_answer"],
                        "generated_by": provider,
                    }
                    q_col.update_one({"_id": doc_id}, {"$set": doc}, upsert=True)
            except Exception as me:
                logger.debug(f"Could not save generated questions to MongoDB: {me}")

        return questions
    except Exception as e:
        logger.warning(f"LLM question generation failed for {topic} ({provider}): {e}")
        return []

