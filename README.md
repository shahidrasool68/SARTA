# SARTA — Semantic Adaptive Recruitment and Technical Assessment

SARTA implements resume parsing, semantic skill extraction, role matching, adaptive MCQ assessment, Judge0-based coding evaluation and explainable reports. The original Layer 1/2 code has been retained; Layer 3/4 code has been corrected and integrated.

**[Read the full setup, implementation details, API guide, testing instructions and limitations](ASSESSMENT_IMPLEMENTATION.md).**

## Quick start

```bash
# Terminal A
cd backend
python -m pip install -r requirements.txt
uvicorn main:app --reload --port 8000

# Terminal B
cd frontend
npm ci
npm run dev
```

Open http://localhost:3000. Coding submissions require a separate, running Judge0 CE sandbox at the address in `JUDGE0_URL` (default http://localhost:2358). No fabricated coding success is returned if Judge0 is offline.

## Tests

```bash
cd backend
pytest -q tests/test_assessment.py
```
