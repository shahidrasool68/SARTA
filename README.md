# SARTA — Semantic Adaptive Recruitment and Technical Assessment

B.Tech Computer Engineering minor project — Jamia Millia Islamia, New Delhi  
Syed Anas Ahmed (23BCS020), Md Shahid Rasool (23BCS021)  
Supervisor: Dr. S M Faisal Malik

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

The repository is a prototype with a small curated question bank; meaningful deployment and scientific evaluation require a real sandbox, broader reviewed content, authentication and a user study. No field-study results are claimed by this README.