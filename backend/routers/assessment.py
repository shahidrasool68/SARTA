"""SARTA assessment API: server-authoritative MCQs and Judge0 grading."""
import os
import random
import re
import uuid
from typing import Any, Dict, List, Optional
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from services.adaptive_controller import select_next_question
from services.performance_analytics import generate_performance_report
from services.judge0_client import evaluate_code
from services.assessment_store import load_session, save_session
from services.coding_bank import get_public_problem, get_problem, select_problem_for_company, CODING_PROBLEMS
from services.company_classifier import get_company_assessment_config, classify_company_tier, initial_difficulty_for_tier
from services.company_problems import load_company_problems, get_top_problems, get_company_problem_stats, get_available_companies
import json
from pathlib import Path

router = APIRouter(prefix="/api/assessment", tags=["Assessment"])

FALLBACK_QUESTIONS = {
    "Python": {
        "Easy": [
            {
                "question": "What is the output of `type([])` in Python 3?",
                "options": ["<class 'list'>", "<class 'array'>", "<class 'dict'>", "<class 'tuple'>"],
                "correct_answer": "<class 'list'>"
            },
            {
                "question": "Which keyword is used to define a function in Python?",
                "options": ["func", "def", "function", "lambda"],
                "correct_answer": "def"
            }
        ],
        "Medium": [
            {
                "question": "What is the time complexity of looking up a key in an average Python dictionary?",
                "options": ["O(1)", "O(log n)", "O(n)", "O(n log n)"],
                "correct_answer": "O(1)"
            },
            {
                "question": "What does a generator function in Python return when invoked?",
                "options": ["A generator iterator object", "A list containing all yield values", "None", "The first yielded value"],
                "correct_answer": "A generator iterator object"
            }
        ],
        "Hard": [
            {
                "question": "How does Python's GIL (Global Interpreter Lock) affect multi-threaded CPU-bound programs on multi-core CPUs?",
                "options": [
                    "Prevents true parallel byte-code execution across cores",
                    "Distributes threads automatically across physical cores",
                    "Doubles the execution speed via thread-level parallelism",
                    "Disables memory garbage collection during threading"
                ],
                "correct_answer": "Prevents true parallel byte-code execution across cores"
            },
            {
                "question": "In Python metaclasses, which method is invoked to allocate the new class instance before `__init__`?",
                "options": ["__new__", "__call__", "__prepare__", "__build__"],
                "correct_answer": "__new__"
            }
        ]
    },
    "JavaScript": {
        "Easy": [
            {
                "question": "Which keyword declares a block-scoped variable in modern ECMAScript?",
                "options": ["let", "var", "scope", "global"],
                "correct_answer": "let"
            }
        ],
        "Medium": [
            {
                "question": "What is the output of `typeof null` in JavaScript?",
                "options": ["'object'", "'null'", "'undefined'", "'number'"],
                "correct_answer": "'object'"
            }
        ],
        "Hard": [
            {
                "question": "In the JavaScript Event Loop, which queue is given priority between tasks (macrotasks) and microtasks?",
                "options": [
                    "Microtasks queue runs to completion before the next macrotask",
                    "Macrotask queue runs completely before microtasks",
                    "They run alternately one by one",
                    "Priority is randomized by the V8 engine"
                ],
                "correct_answer": "Microtasks queue runs to completion before the next macrotask"
            }
        ]
    },
    "React": {
        "Easy": [
            {
                "question": "Which React hook is used to manage local component state in functional components?",
                "options": ["useState", "useEffect", "useMemo", "useContext"],
                "correct_answer": "useState"
            }
        ],
        "Medium": [
            {
                "question": "Why should you pass a unique `key` prop when rendering a list of elements in React?",
                "options": [
                    "To help React's virtual DOM identify which items changed, were added, or removed",
                    "To apply unique CSS styles to list items",
                    "To enable automatic caching in localStorage",
                    "It is purely optional and has no performance benefit"
                ],
                "correct_answer": "To help React's virtual DOM identify which items changed, were added, or removed"
            }
        ],
        "Hard": [
            {
                "question": "When does the callback inside `useLayoutEffect` execute relative to browser painting?",
                "options": [
                    "Synchronously after DOM mutations but before the browser paints",
                    "Asynchronously after the browser has completed painting",
                    "Before any reconciliation process starts",
                    "Inside a web worker thread"
                ],
                "correct_answer": "Synchronously after DOM mutations but before the browser paints"
            }
        ]
    },
    "OOP": {
        "Easy": [
            {
                "question": "Which OOP concept describes bundling data and methods that operate on that data within a single unit?",
                "options": ["Encapsulation", "Polymorphism", "Inheritance", "Abstraction"],
                "correct_answer": "Encapsulation"
            }
        ],
        "Medium": [
            {
                "question": "Which principle in SOLID states that software entities should be open for extension, but closed for modification?",
                "options": [
                    "Open/Closed Principle (OCP)",
                    "Single Responsibility Principle (SRP)",
                    "Liskov Substitution Principle (LSP)",
                    "Interface Segregation Principle (ISP)"
                ],
                "correct_answer": "Open/Closed Principle (OCP)"
            }
        ],
        "Hard": [
            {
                "question": "In Design Patterns, how does the Abstract Factory pattern differ from the Factory Method pattern?",
                "options": [
                    "Abstract Factory produces families of related objects without specifying their concrete classes",
                    "Factory Method can only produce singleton objects",
                    "Abstract Factory relies solely on static inheritance",
                    "Factory Method requires asynchronous promises"
                ],
                "correct_answer": "Abstract Factory produces families of related objects without specifying their concrete classes"
            }
        ]
    },
    "Data Structures": {
        "Easy": [
            {
                "question": "Which data structure operates on a Last-In, First-Out (LIFO) basis?",
                "options": ["Stack", "Queue", "Binary Tree", "Linked List"],
                "correct_answer": "Stack"
            }
        ],
        "Medium": [
            {
                "question": "What is the worst-case time complexity of quicksort when poor pivots are chosen?",
                "options": ["O(n^2)", "O(n log n)", "O(n)", "O(log n)"],
                "correct_answer": "O(n^2)"
            }
        ],
        "Hard": [
            {
                "question": "What is the amortized cost per operation for union and find in a Disjoint Set (Union-Find) with path compression and union by rank?",
                "options": ["O(α(n)) (Inverse Ackermann)", "O(log n)", "O(1) strict", "O(n)"],
                "correct_answer": "O(α(n)) (Inverse Ackermann)"
            }
        ]
    },
    "SQL": {
        "Easy": [
            {
                "question": "Which SQL clause is used to filter rows returned by a SELECT query?",
                "options": ["WHERE", "ORDER BY", "GROUP BY", "HAVING"],
                "correct_answer": "WHERE"
            }
        ],
        "Medium": [
            {
                "question": "What is the primary difference between WHERE and HAVING clauses in SQL?",
                "options": [
                    "WHERE filters individual rows before grouping; HAVING filters aggregated groups after GROUP BY",
                    "WHERE operates only on indexed columns; HAVING operates on unindexed columns",
                    "HAVING is used exclusively with subqueries",
                    "There is no difference; they are interchangeable aliases"
                ],
                "correct_answer": "WHERE filters individual rows before grouping; HAVING filters aggregated groups after GROUP BY"
            }
        ],
        "Hard": [
            {
                "question": "How does the window function DENSE_RANK() differ from RANK() in SQL when handling tied values?",
                "options": [
                    "DENSE_RANK does not skip subsequent ranking numbers after ties; RANK leaves gaps",
                    "RANK does not skip numbers; DENSE_RANK leaves gaps",
                    "DENSE_RANK only works with partitioned tables",
                    "RANK can only be used with numeric sorting"
                ],
                "correct_answer": "DENSE_RANK does not skip subsequent ranking numbers after ties; RANK leaves gaps"
            }
        ]
    },
    "Machine Learning": {
        "Easy": [
            {
                "question": "Which type of machine learning uses labeled training datasets to learn mapping functions?",
                "options": ["Supervised Learning", "Unsupervised Learning", "Reinforcement Learning", "Self-Organizing Maps"],
                "correct_answer": "Supervised Learning"
            }
        ],
        "Medium": [
            {
                "question": "What common problem does L1 regularization (Lasso) mitigate by driving feature coefficients to zero?",
                "options": [
                    "Overfitting by performing automatic feature selection",
                    "Vanishing gradients in deep neural networks",
                    "Class imbalance in binary classification",
                    "Exploding learning rates"
                ],
                "correct_answer": "Overfitting by performing automatic feature selection"
            }
        ],
        "Hard": [
            {
                "question": "In the Bias-Variance tradeoff, what symptom characterizes a model with high variance?",
                "options": [
                    "Low training error but significantly higher cross-validation / test error (overfitting)",
                    "High training error and high test error (underfitting)",
                    "Consistently stable predictions across diverse training subsets",
                    "Premature convergence during gradient descent"
                ],
                "correct_answer": "Low training error but significantly higher cross-validation / test error (overfitting)"
            }
        ]
    },
    "OS": {
        "Easy": [
            {
                "question": "What is the main role of the Operating System kernel?",
                "options": [
                    "Manage system hardware resources and facilitate inter-process communication",
                    "Provide a compiler for user programming languages",
                    "Display graphics on the monitor directly",
                    "Render web pages in browser engines"
                ],
                "correct_answer": "Manage system hardware resources and facilitate inter-process communication"
            }
        ],
        "Medium": [
            {
                "question": "Which condition is NOT one of Coffman's four necessary conditions for deadlock to occur?",
                "options": [
                    "Preemption allowed",
                    "Mutual Exclusion",
                    "Hold and Wait",
                    "Circular Wait"
                ],
                "correct_answer": "Preemption allowed"
            }
        ],
        "Hard": [
            {
                "question": "What is the phenomenon called when excessive paging causes the CPU to spend more time swapping pages than executing instructions?",
                "options": ["Thrashing", "Starvation", "Context Inversion", "Belady's Anomaly"],
                "correct_answer": "Thrashing"
            }
        ]
    },
    "Computer Networks": {
        "Easy": [
            {
                "question": "Which layer of the OSI model does the TCP protocol belong to?",
                "options": ["Transport Layer", "Network Layer", "Application Layer", "Data Link Layer"],
                "correct_answer": "Transport Layer"
            }
        ],
        "Medium": [
            {
                "question": "What is the primary function of the Address Resolution Protocol (ARP)?",
                "options": [
                    "Map an IP address (IPv4) to a physical MAC address on a local network",
                    "Translate domain names into IP addresses",
                    "Establish encrypted TLS connections between client and server",
                    "Route packets across autonomous systems"
                ],
                "correct_answer": "Map an IP address (IPv4) to a physical MAC address on a local network"
            }
        ],
        "Hard": [
            {
                "question": "In TCP Congestion Control, how is congestion window (cwnd) adjusted during the Fast Recovery phase upon receiving three duplicate ACKs?",
                "options": [
                    "ssthresh is set to half of cwnd, cwnd is set to ssthresh + 3 MSS, and cwnd grows linearly per additional duplicate ACK",
                    "cwnd is immediately reset to 1 MSS and slow start restarts",
                    "cwnd is doubled unconditionally",
                    "The connection is terminated and re-established"
                ],
                "correct_answer": "ssthresh is set to half of cwnd, cwnd is set to ssthresh + 3 MSS, and cwnd grows linearly per additional duplicate ACK"
            }
        ]
    }
}

# ── Integrate Curated PDF Question Bank (OS, CN, OOP, System Design, Aptitude) ──
_PDF_CACHE_FILE = Path(__file__).resolve().parent.parent / "database" / "parsed_pdf_questions.json"
if _PDF_CACHE_FILE.exists():
    try:
        with open(_PDF_CACHE_FILE, "r", encoding="utf-8") as _f:
            _pdf_bank = json.load(_f)
            for _skill, _levels in _pdf_bank.items():
                if _skill not in FALLBACK_QUESTIONS:
                    FALLBACK_QUESTIONS[_skill] = {"Easy": [], "Medium": [], "Hard": []}
                for _diff in ("Easy", "Medium", "Hard"):
                    if _diff in _levels:
                        # Add questions from the calibrated 60-question PDF bank
                        FALLBACK_QUESTIONS[_skill][_diff].extend(_levels[_diff])
    except Exception as _e:
        print(f"Notice: Could not load PDF question cache: {_e}")


DIFFICULTIES = ("Easy", "Medium", "Hard")
SUPPORTED_SKILLS = tuple(FALLBACK_QUESTIONS)
ROLE_SKILLS = {
    "web development": ("JavaScript", "React", "SQL", "OOP"),
    "frontend developer": ("JavaScript", "React", "OOP", "Data Structures"),
    "backend developer": ("Python", "SQL", "OS", "System Design"),
    "data science": ("Python", "Machine Learning", "SQL", "Data Structures"),
    "data scientist": ("Python", "Machine Learning", "SQL", "Data Structures"),
    "software engineer": ("Data Structures", "OOP", "OS", "Computer Networks"),
}

class StartSessionRequest(BaseModel):
    skills: List[str] = Field(default_factory=list)
    role: str = "Backend Developer"
    missing_skills: List[str] = Field(default_factory=list)
    target_company: Optional[str] = None

class MCQRequest(BaseModel):
    session_id: str
    skill: str
    # Legacy fields accepted but ignored; server owns adaptation.
    current_difficulty: str = "Medium"
    is_last_correct: bool = True
    streak: int = 0

class SubmitAnswerRequest(BaseModel):
    session_id: str
    question_id: str
    selected_answer: str
    # Legacy fields are ignored; never trust browser-sent answer/difficulty.
    skill: Optional[str] = None
    difficulty: Optional[str] = None
    correct_answer: Optional[str] = None

class CodeSubmission(BaseModel):
    session_id: str
    problem_id: str
    language_id: int
    source_code: str = Field(min_length=1, max_length=100000)
    mode: str = "submit"  # 'run' checks samples; 'submit' checks all hidden tests

class CompleteAssessmentRequest(BaseModel):
    session_id: str
    # Client-provided coding scores are ignored.
    coding_results: List[Dict[str, Any]] = Field(default_factory=list)


def session_or_404(session_id):
    session = load_session(session_id)
    if session is None:
        raise HTTPException(status_code=404, detail="Unknown assessment session")
    return session


def canonical_skill(skill):
    return next((s for s in SUPPORTED_SKILLS if s.casefold() == skill.casefold()), None)


def available_levels(skill):
    return [d for d in DIFFICULTIES if FALLBACK_QUESTIONS[skill].get(d)]


def make_question(skill, difficulty, seen):
    levels = sorted(available_levels(skill), key=lambda level: abs(DIFFICULTIES.index(level) - DIFFICULTIES.index(difficulty)))
    for level in levels:
        options = FALLBACK_QUESTIONS[skill][level]
        choices = [(i,q) for i,q in enumerate(options) if f"{skill}:{level}:{i}" not in seen]
        if choices:
            i, q = random.choice(choices)
            key = f"{skill}:{level}:{i}"
            # Shuffle options so the correct answer isn't always in the same position.
            # correct_answer is stored by value, so validation is unaffected.
            shuffled_options = list(q["options"])
            random.shuffle(shuffled_options)
            return key, {"_id": key, "skill": skill, "difficulty": level, "question": q["question"], "options": shuffled_options}, q["correct_answer"]
    return None


@router.get("/catalog")
def catalog():
    return {"skills": list(SUPPORTED_SKILLS), "difficulty_levels": list(DIFFICULTIES), "coding_problems": [get_public_problem(k) for k in CODING_PROBLEMS]}


@router.post("/start-session")
def start_assessment_session(req: StartSessionRequest):
    skills = []
    role_key = req.role.strip().lower()
    role_topics = ROLE_SKILLS.get(role_key, ROLE_SKILLS["software engineer"])
    # Prioritize skills demonstrated on the resume which overlap the chosen role;
    # include missing role prerequisites to verify gaps, then general fundamentals.
    ordered = [s for s in role_topics if s.casefold() in {x.casefold() for x in req.skills}]
    ordered += [s for s in role_topics if s.casefold() in {x.casefold() for x in req.missing_skills}]
    ordered += list(role_topics) + req.skills + req.missing_skills + ["OOP", "Python"]
    for requested in ordered:
        skill = canonical_skill(requested)
        if skill and skill not in skills:
            skills.append(skill)
        if len(skills) == 4:
            break
    if not skills:
        raise HTTPException(status_code=422, detail="No assessable skills selected")

    # ── Company-tier-based initial difficulty & coding challenge selection ─
    company_config = get_company_assessment_config(req.target_company or "")
    initial_diff = company_config["initial_difficulty"]  # Easy / Medium / Hard
    assigned_problem_id = select_problem_for_company(req.target_company or "", company_config["tier"])

    sid = str(uuid.uuid4())
    session = {
        "session_id": sid, "role": req.role, "skills_to_assess": skills,
        "target_company": req.target_company or None,
        "company_tier": company_config["tier"],
        "responses": [], "coding_results": [], "pending": None, "seen": [],
        "per_skill_state": {skill: {"difficulty": initial_diff, "streak": 0, "questions_answered": 0, "correct": 0} for skill in skills},
        "coding_problem_id": assigned_problem_id, "report": None, "completed": False,
    }
    save_session(session)
    return {"session_id": sid, "role": req.role, "skills_to_assess": skills,
            "target_company": req.target_company,
            "company_tier": company_config["tier"],
            "coding_problem_id": assigned_problem_id,
            "questions_per_skill": 3, "total_mcqs": len(skills)*3,
            "blueprint": {"role": req.role, "skills": skills, "initial_difficulty": initial_diff, "coding_challenge": assigned_problem_id}}


@router.post("/next-mcq")
def next_mcq(req: MCQRequest):
    session = session_or_404(req.session_id)
    if session["completed"]:
        raise HTTPException(status_code=409, detail="Assessment is already complete")
    if req.skill not in session["skills_to_assess"]:
        raise HTTPException(status_code=400, detail="Skill not in assessment")
    pending = session.get("pending")
    if pending:
        if pending["skill"] != req.skill:
            raise HTTPException(status_code=409, detail="Answer current question before moving on")
        return {"question": pending["public"], "adaptive_state": {"next_difficulty": pending["difficulty"]}}
    state = session["per_skill_state"][req.skill]
    if state["questions_answered"] >= 3:
        raise HTTPException(status_code=409, detail="Skill question limit reached")
    selected = make_question(req.skill, state["difficulty"], set(session["seen"]))
    if not selected:
        raise HTTPException(status_code=409, detail="Question bank exhausted")
    key, public, correct = selected
    session["seen"].append(key)
    session["pending"] = {"question_id": key, "skill": req.skill, "difficulty": public["difficulty"], "correct": correct, "public": public}
    save_session(session)
    return {"question": public, "adaptive_state": {"next_difficulty": public["difficulty"]}}


@router.post("/submit-answer")
def submit_answer(req: SubmitAnswerRequest):
    session = session_or_404(req.session_id)
    pending = session.get("pending")
    if session["completed"] or not pending or pending["question_id"] != req.question_id:
        raise HTTPException(status_code=409, detail="Question was not issued or already answered")
    if req.selected_answer not in pending["public"]["options"]:
        raise HTTPException(status_code=422, detail="Answer must match a supplied option")
    correct = req.selected_answer == pending["correct"]
    skill = pending["skill"]
    state = session["per_skill_state"][skill]
    state["questions_answered"] += 1
    state["correct"] += int(correct)
    state["streak"] = state["streak"] + 1 if correct else 0
    # Consistent CAT-inspired calibration: streak plus per-skill running accuracy.
    result = select_next_question(skill, pending["difficulty"], correct, state["streak"],
                                  accuracy=state["correct"]/state["questions_answered"])
    state["difficulty"] = result["next_difficulty"]
    session["responses"].append({"question_id": pending["question_id"], "skill": skill,
                                 "difficulty": pending["difficulty"], "selected_answer": req.selected_answer,
                                 "is_correct": correct})
    session["pending"] = None
    save_session(session)
    return {"is_correct": correct, "correct_answer": pending["correct"],
            "streak": state["streak"], "next_difficulty": state["difficulty"],
            "running_accuracy": round(100*state["correct"]/state["questions_answered"],1)}


@router.get("/coding-question/{company}")
def coding_question(company: str, session_id: Optional[str] = None):
    # Public statement and SAMPLE tests only; private hidden inputs never leave backend.
    prob_id = "two_sum"
    if session_id:
        try:
            session = session_or_404(session_id)
            prob_id = session.get("coding_problem_id", "two_sum")
        except Exception:
            prob_id = select_problem_for_company(company)
    else:
        prob_id = select_problem_for_company(company)

    problem = get_public_problem(prob_id)
    # Attach company-specific LeetCode problem stats if available
    company_stats = get_company_problem_stats(company) if company and company != "General" else None
    company_problems_list = get_top_problems(company, n=10) if company and company != "General" else []
    return {
        **problem,
        "company": company if company and company != "General" else "General",
        "company_stats": company_stats,
        "company_problems": company_problems_list,
    }


@router.get("/company-problems/{company}")
def company_problems_endpoint(company: str, difficulty: Optional[str] = None, limit: int = 20):
    """Get LeetCode problems frequently asked by a specific company."""
    problems = get_top_problems(company, n=limit, difficulty=difficulty)
    stats = get_company_problem_stats(company)
    return {
        "company": company,
        "stats": stats,
        "problems": problems,
    }


@router.get("/available-companies")
def available_companies():
    """List all companies with LeetCode problem data."""
    return {"companies": get_available_companies()}


@router.post("/evaluate-code")
async def evaluate_candidate_code(submission: CodeSubmission):
    session = session_or_404(submission.session_id)
    if session["completed"]:
        raise HTTPException(status_code=409, detail="Assessment is already complete")
    if submission.problem_id != session["coding_problem_id"]:
        raise HTTPException(status_code=400, detail="Problem not assigned to session")
    if submission.mode not in ("run", "submit"):
        raise HTTPException(status_code=422, detail="mode must be run or submit")
    if submission.language_id not in (71, 63, 62, 54):
        raise HTTPException(status_code=422, detail="Unsupported Judge0 language")
    problem = get_problem(submission.problem_id)
    tests = problem["test_cases"] if submission.mode == "submit" else [t for t in problem["test_cases"] if not t["hidden"]]
    results = []
    for test in tests:
        result = await evaluate_code(submission.language_id, submission.source_code, test["expected"], test["stdin"])
        results.append({"passed": result["success"], "status": result["status"], "time": result.get("time"),
                        "label": "Hidden test" if test["hidden"] else test["label"]})
        if result.get("status") == "Sandbox unavailable":
            raise HTTPException(status_code=503, detail="Judge0 is unavailable. No coding score has been awarded.")
    passed = sum(bool(r["passed"]) for r in results)
    response = {"success": passed == len(tests), "status": "Accepted" if passed == len(tests) else "Test cases failed",
                "test_cases_passed": passed, "test_cases_total": len(tests), "tests": results,
                "stdout": f"{passed}/{len(tests)} tests passed", "time": results[-1].get("time") if results else None}
    if submission.mode == "submit":
        record = {"title": problem["title"], "difficulty": problem["difficulty"], "language": submission.language_id,
                  "passed": response["success"], "test_cases_passed": passed, "test_cases_total": len(tests),
                  "time": response["time"]}
        session["coding_results"] = [record]
        save_session(session)
    return response


@router.post("/complete")
def complete(req: CompleteAssessmentRequest):
    session = session_or_404(req.session_id)
    if session["pending"]:
        raise HTTPException(status_code=409, detail="Please answer the current question first")
    if session["report"]:
        return {"status": "success", "session_id": req.session_id, "report": session["report"]}
    # Never trust coding_results supplied by the browser.
    report = generate_performance_report(session["responses"], session["coding_results"])
    report["role"] = session["role"]
    report["coding_status"] = "graded" if session["coding_results"] else "not_submitted"
    session["report"] = report
    session["completed"] = True
    save_session(session)
    return {"status": "success", "session_id": req.session_id, "report": report}


@router.get("/report/{session_id}")
def report(session_id: str):
    session = session_or_404(session_id)
    if not session.get("report"):
        raise HTTPException(status_code=404, detail="Report not ready")
    return session["report"]
