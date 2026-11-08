# SARTA — Layers 3 and 4 implementation guide

This delivery retains the uploaded resume parsing and semantic matching layers and replaces the prototype assessment API with a server-authoritative assessment and intelligence implementation. The existing Next.js/Monaco interface and evaluation report are integrated with the replacement API.

## Features

**Layer 3 — Assessment**
- Role-driven three-question-per-skill MCQ sessions for Web Development, Frontend Developer, Backend Developer, Data Science, Data Scientist and Software Engineer.
- Curated questions tagged `Easy`, `Medium`, `Hard`. A question is delivered at most once within a session. Answers are *never* included with the question payload. The API grades on the server and rejects duplicate answers and unissued questions.
- Coding assessment using a fixed, reviewed stdin/stdout Two Sum challenge. One public sample and three private hidden tests run against Judge0 CE. Four language IDs supported: Python 71, JavaScript 63, Java 62, C++ 54 (confirm your Judge0 version supports these IDs).
- Sample-only `run` and hidden-test `submit` actions. Judge0 must be running; an unavailable sandbox produces HTTP 503 and no fabricated score.

**Layer 4 — Intelligence**
- Per-skill correct-answer streak, cumulative accuracy and adaptive Easy/Medium/Hard levels. Two consecutive correct answers and >=60% accuracy increase difficulty one level; an incorrect answer decreases it one level.
- Skill-wise breakdown, accuracy, peak successfully attempted difficulty, difficulty progression, strengths/weaknesses, coding hidden-test pass ratio, combined score and outcome summary.
- SQLite persistence of sessions and server-side results, with reports retrievable by session ID after restart.

## Setup

1. Install Python 3.10+ and Node.js suitable for Next.js 16 (Node.js 20.9+).
2. In `backend`, create a virtual environment and install `pip install -r requirements.txt`.
3. Run `uvicorn main:app --reload --port 8000` from the `backend` directory.
4. In `frontend`, run `npm ci` then `npm run dev` and open `http://localhost:3000`.
5. **For real code grading**, separately deploy the official Judge0 CE sandbox locally or on a trusted server, and set `JUDGE0_URL` to the sandbox's HTTP URL (default `http://127.0.0.1:2358`). Judge0 CE must allow synchronous submissions (`wait=true`) and use its own isolation and resource limits. Never execute candidate code directly in the SARTA FastAPI process.
6. Optional: provide `MONGO_URI` to access the skill taxonomy database. The current assessed questions are curated locally; MongoDB is not required for assessment.
7. Optional: set `SARTA_ASSESSMENT_DB` to the full filesystem path of the assessment SQLite database. Default: `backend/assessment_sessions.sqlite3`.

**Secrets:** The hardcoded MongoDB Atlas credential found in the uploaded source has been removed. **Rotate or revoke that database password immediately**; removing it from this ZIP does not undo exposure in copies or commit history.

## API endpoints

| Method | Path | Purpose |
|---|---|---|
| GET | `/api/assessment/catalog` | Supported assessment topics and challenges |
| POST | `/api/assessment/start-session` | Allocate role-based assessment |
| POST | `/api/assessment/next-mcq` | Issue one server-tracked question |
| POST | `/api/assessment/submit-answer` | Grade one issued question and adapt difficulty |
| GET | `/api/assessment/coding-question/General` | Public challenge and visible example only |
| POST | `/api/assessment/evaluate-code` | `mode=run` samples or `mode=submit` all tests |
| POST | `/api/assessment/complete` | Persist final verified report |
| GET | `/api/assessment/report/{session_id}` | Retrieve final report |

API documentation at `http://localhost:8000/docs` once backend is running.

## Testing

From `backend`: `pytest -q tests/test_assessment.py`. Tests use a mocked Judge0 client to exercise scoring/failure handling without pretending that a real Judge0 deployment was tested. Verify real Judge0 submission separately with a working sandbox and sample code:

```python
n = int(input())
nums = list(map(int, input().split()))
target = int(input())
seen = {}
for i, v in enumerate(nums):
    if target-v in seen:
        print(seen[target-v], i)
        break
    seen[v] = i
```

## Limitations and production hardening

This is a research/undergraduate prototype, not a production high-stakes recruiting system. The curated bank is small (one to two questions at each difficulty for most skills) and the coding catalog currently has one reviewed challenge. The deployment needs a running Judge0 CE service; without it coding submissions explicitly fail. The project does not yet include authentication, candidate consent/retention controls, multi-user authorization, proctoring, rate limiting, concurrency/locking across several API workers, a recruiter dashboard, or validated empirical research results. For real recruiting use, add these safeguards and broaden/audit the bank before drawing hiring conclusions. In research documentation, do not present simulated benchmark numbers as field study results.

If `pytest` is not installed, run `python -m pip install pytest` before running the automated test suite.
