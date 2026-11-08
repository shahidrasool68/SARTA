"""MongoDB Skill Tree — Knowledge Graph, not a flat list.

Each node = one skill at one difficulty level.
Node schema:
    { skill, difficulty, question_ids[], prerequisites[] }

Arrows in the graph represent prerequisite relationships:
    DSA → Python → Django
    DSA → Python → FastAPI
    DBMS → SQL → Redis
    HTML/CSS → JavaScript → React → Next.js
    etc.

This module seeds MongoDB with the full skill tree and question bank.
"""

import os
import sys
from pymongo import MongoClient

# Allow running this file directly (python database/mongo_skill_tree.py)
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import MONGO_URI, MONGO_DB_NAME


def get_db():
    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=2000, connectTimeoutMS=2000)
    return client[MONGO_DB_NAME]


# ── Skill Prerequisite Graph ────────────────────────────────────────────
# Maps each skill to its prerequisites (skills that should be mastered first).
SKILL_PREREQUISITES = {
    # Foundations (no prerequisites)
    "Data Structures": [],
    "OOP": [],
    "Computer Networks": [],
    "OS": [],

    # Languages build on fundamentals
    "Python": ["Data Structures"],
    "JavaScript": ["Data Structures"],
    "SQL": ["Data Structures"],

    # Frameworks build on languages
    "React": ["JavaScript"],
    "Django": ["Python"],
    "FastAPI": ["Python"],
    "Next.js": ["React", "JavaScript"],
    "Node.js": ["JavaScript"],
    "Express": ["Node.js", "JavaScript"],
    "Flask": ["Python"],
    "Spring Boot": ["Java", "OOP"],

    # Advanced topics build on foundations
    "Machine Learning": ["Python", "Data Structures"],
    "Deep Learning": ["Machine Learning", "Python"],
    "System Design": ["OOP", "Data Structures", "Computer Networks"],

    # Databases
    "MongoDB": ["Data Structures"],
    "Redis": ["SQL", "Data Structures"],
    "PostgreSQL": ["SQL"],
    "Aptitude": [],

    # DevOps / Cloud
    "Docker": ["Linux"],
    "Kubernetes": ["Docker"],
    "AWS": ["Computer Networks"],
    "CI/CD": ["Git"],

    # Tools
    "Git": [],
    "Linux": ["OS"],
}


# ── Question Bank ───────────────────────────────────────────────────────
# Mirrors the FALLBACK_QUESTIONS from assessment.py but with MongoDB IDs.
# Each question is stored as a document in the `questions` collection.
QUESTION_BANK = {
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
        "Easy": [{"question": "Which React hook is used to manage local component state in functional components?", "options": ["useState", "useEffect", "useMemo", "useContext"], "correct_answer": "useState"}],
        "Medium": [{"question": "Why should you pass a unique `key` prop when rendering a list of elements in React?", "options": ["To help React's virtual DOM identify which items changed, were added, or removed", "To apply unique CSS styles to list items", "To enable automatic caching in localStorage", "It is purely optional and has no performance benefit"], "correct_answer": "To help React's virtual DOM identify which items changed, were added, or removed"}],
        "Hard": [{"question": "When does the callback inside `useLayoutEffect` execute relative to browser painting?", "options": ["Synchronously after DOM mutations but before the browser paints", "Asynchronously after the browser has completed painting", "Before any reconciliation process starts", "Inside a web worker thread"], "correct_answer": "Synchronously after DOM mutations but before the browser paints"}]
    },
    "OOP": {
        "Easy": [{"question": "Which OOP concept describes bundling data and methods that operate on that data within a single unit?", "options": ["Encapsulation", "Polymorphism", "Inheritance", "Abstraction"], "correct_answer": "Encapsulation"}],
        "Medium": [{"question": "Which principle in SOLID states that software entities should be open for extension, but closed for modification?", "options": ["Open/Closed Principle (OCP)", "Single Responsibility Principle (SRP)", "Liskov Substitution Principle (LSP)", "Interface Segregation Principle (ISP)"], "correct_answer": "Open/Closed Principle (OCP)"}],
        "Hard": [{"question": "In Design Patterns, how does the Abstract Factory pattern differ from the Factory Method pattern?", "options": ["Abstract Factory produces families of related objects without specifying their concrete classes", "Factory Method can only produce singleton objects", "Abstract Factory relies solely on static inheritance", "Factory Method requires asynchronous promises"], "correct_answer": "Abstract Factory produces families of related objects without specifying their concrete classes"}]
    },
    "Data Structures": {
        "Easy": [{"question": "Which data structure operates on a Last-In, First-Out (LIFO) basis?", "options": ["Stack", "Queue", "Binary Tree", "Linked List"], "correct_answer": "Stack"}],
        "Medium": [{"question": "What is the worst-case time complexity of quicksort when poor pivots are chosen?", "options": ["O(n^2)", "O(n log n)", "O(n)", "O(log n)"], "correct_answer": "O(n^2)"}],
        "Hard": [{"question": "What is the amortized cost per operation for union and find in a Disjoint Set (Union-Find) with path compression and union by rank?", "options": ["O(α(n)) (Inverse Ackermann)", "O(log n)", "O(1) strict", "O(n)"], "correct_answer": "O(α(n)) (Inverse Ackermann)"}]
    },
    "SQL": {
        "Easy": [{"question": "Which SQL clause is used to filter rows returned by a SELECT query?", "options": ["WHERE", "ORDER BY", "GROUP BY", "HAVING"], "correct_answer": "WHERE"}],
        "Medium": [{"question": "What is the primary difference between WHERE and HAVING clauses in SQL?", "options": ["WHERE filters individual rows before grouping; HAVING filters aggregated groups after GROUP BY", "WHERE operates only on indexed columns; HAVING operates on unindexed columns", "HAVING is used exclusively with subqueries", "There is no difference; they are interchangeable aliases"], "correct_answer": "WHERE filters individual rows before grouping; HAVING filters aggregated groups after GROUP BY"}],
        "Hard": [{"question": "How does the window function DENSE_RANK() differ from RANK() in SQL when handling tied values?", "options": ["DENSE_RANK does not skip subsequent ranking numbers after ties; RANK leaves gaps", "RANK does not skip numbers; DENSE_RANK leaves gaps", "DENSE_RANK only works with partitioned tables", "RANK can only be used with numeric sorting"], "correct_answer": "DENSE_RANK does not skip subsequent ranking numbers after ties; RANK leaves gaps"}]
    },
    "Machine Learning": {
        "Easy": [{"question": "Which type of machine learning uses labeled training datasets to learn mapping functions?", "options": ["Supervised Learning", "Unsupervised Learning", "Reinforcement Learning", "Self-Organizing Maps"], "correct_answer": "Supervised Learning"}],
        "Medium": [{"question": "What common problem does L1 regularization (Lasso) mitigate by driving feature coefficients to zero?", "options": ["Overfitting by performing automatic feature selection", "Vanishing gradients in deep neural networks", "Class imbalance in binary classification", "Exploding learning rates"], "correct_answer": "Overfitting by performing automatic feature selection"}],
        "Hard": [{"question": "In the Bias-Variance tradeoff, what symptom characterizes a model with high variance?", "options": ["Low training error but significantly higher cross-validation / test error (overfitting)", "High training error and high test error (underfitting)", "Consistently stable predictions across diverse training subsets", "Premature convergence during gradient descent"], "correct_answer": "Low training error but significantly higher cross-validation / test error (overfitting)"}]
    },
    "OS": {
        "Easy": [{"question": "What is the main role of the Operating System kernel?", "options": ["Manage system hardware resources and facilitate inter-process communication", "Provide a compiler for user programming languages", "Display graphics on the monitor directly", "Render web pages in browser engines"], "correct_answer": "Manage system hardware resources and facilitate inter-process communication"}],
        "Medium": [{"question": "Which condition is NOT one of Coffman's four necessary conditions for deadlock to occur?", "options": ["Preemption allowed", "Mutual Exclusion", "Hold and Wait", "Circular Wait"], "correct_answer": "Preemption allowed"}],
        "Hard": [{"question": "What is the phenomenon called when excessive paging causes the CPU to spend more time swapping pages than executing instructions?", "options": ["Thrashing", "Starvation", "Context Inversion", "Belady's Anomaly"], "correct_answer": "Thrashing"}]
    },
    "Computer Networks": {
        "Easy": [{"question": "Which layer of the OSI model does the TCP protocol belong to?", "options": ["Transport Layer", "Network Layer", "Application Layer", "Data Link Layer"], "correct_answer": "Transport Layer"}],
        "Medium": [{"question": "What is the primary function of the Address Resolution Protocol (ARP)?", "options": ["Map an IP address (IPv4) to a physical MAC address on a local network", "Translate domain names into IP addresses", "Establish encrypted TLS connections between client and server", "Route packets across autonomous systems"], "correct_answer": "Map an IP address (IPv4) to a physical MAC address on a local network"}],
        "Hard": [{"question": "In TCP Congestion Control, how is congestion window (cwnd) adjusted during the Fast Recovery phase upon receiving three duplicate ACKs?", "options": ["ssthresh is set to half of cwnd, cwnd is set to ssthresh + 3 MSS, and cwnd grows linearly per additional duplicate ACK", "cwnd is immediately reset to 1 MSS and slow start restarts", "cwnd is doubled unconditionally", "The connection is terminated and re-established"], "correct_answer": "ssthresh is set to half of cwnd, cwnd is set to ssthresh + 3 MSS, and cwnd grows linearly per additional duplicate ACK"}]
    },
}


def seed_skill_tree():
    """Seed MongoDB with the full skill tree (knowledge graph).
    
    Creates two collections:
      - `skill_tree`: Nodes of the skill graph (one per skill × difficulty)
      - `questions`: Individual MCQ questions with stable IDs
    """
    db = get_db()
    skill_tree_col = db["skill_tree"]
    questions_col = db["questions"]

    # ── Merge Curated PDF Question Bank (300 questions from 5 domain PDFs) ──
    try:
        try:
            from database.pdf_extractor import load_cached_pdf_questions
        except ImportError:
            from pdf_extractor import load_cached_pdf_questions
        pdf_questions = load_cached_pdf_questions()
        for skill, levels in pdf_questions.items():
            if skill not in QUESTION_BANK:
                QUESTION_BANK[skill] = {"Easy": [], "Medium": [], "Hard": []}
            for diff in ("Easy", "Medium", "Hard"):
                if diff in levels:
                    QUESTION_BANK[skill][diff] = levels[diff]
    except Exception as e:
        print(f"Notice: Could not load PDF questions for seeding: {e}")

    # ── Seed Questions ───────────────────────────────────────────────────
    print("Seeding questions into MongoDB...")
    total_q_seeded = 0
    for skill, difficulties in QUESTION_BANK.items():
        for difficulty, questions in difficulties.items():
            for idx, q in enumerate(questions):
                q_id = f"{skill}:{difficulty}:{idx}"
                doc = {
                    "_id": q_id,
                    "skill": skill,
                    "difficulty": difficulty,
                    "difficulty_score": q.get("difficulty_score", 5.0),
                    "question": q["question"],
                    "options": q["options"],
                    "correct_answer": q["correct_answer"],
                }
                questions_col.update_one(
                    {"_id": q_id}, {"$set": doc}, upsert=True
                )
                total_q_seeded += 1

    # ── Seed Skill Tree Nodes ────────────────────────────────────────────
    print("Seeding skill tree nodes into MongoDB...")
    difficulties = ["Easy", "Medium", "Hard"]

    for skill in QUESTION_BANK:
        prereqs = SKILL_PREREQUISITES.get(skill, [])
        for difficulty in difficulties:
            # Collect question IDs for this skill×difficulty
            question_ids = [
                f"{skill}:{difficulty}:{idx}"
                for idx in range(len(QUESTION_BANK[skill].get(difficulty, [])))
            ]
            node_id = f"{skill}:{difficulty}"
            node = {
                "_id": node_id,
                "skill": skill,
                "difficulty": difficulty,
                "question_ids": question_ids,
                "prerequisites": prereqs,
            }
            skill_tree_col.update_one(
                {"_id": node_id}, {"$set": node}, upsert=True
            )

    # Also seed skill tree nodes for skills that have prerequisites but no questions yet
    for skill, prereqs in SKILL_PREREQUISITES.items():
        if skill not in QUESTION_BANK:
            for difficulty in difficulties:
                node_id = f"{skill}:{difficulty}"
                node = {
                    "_id": node_id,
                    "skill": skill,
                    "difficulty": difficulty,
                    "question_ids": [],
                    "prerequisites": prereqs,
                }
                skill_tree_col.update_one(
                    {"_id": node_id}, {"$set": node}, upsert=True
                )

    # ── Summary ──────────────────────────────────────────────────────────
    q_count = questions_col.count_documents({})
    node_count = skill_tree_col.count_documents({})
    print(f"MongoDB seeded: {q_count} questions, {node_count} skill tree nodes.")


def get_skill_prerequisites(skill: str) -> list:
    """Get prerequisite skills for a given skill from the knowledge graph."""
    return SKILL_PREREQUISITES.get(skill, [])


def get_skill_tree_node(skill: str, difficulty: str) -> dict | None:
    """Fetch a skill tree node from MongoDB."""
    try:
        db = get_db()
        return db["skill_tree"].find_one({"_id": f"{skill}:{difficulty}"})
    except Exception:
        return None


def get_questions_from_mongo(skill: str, difficulty: str) -> list:
    """Fetch questions for a skill×difficulty from MongoDB."""
    try:
        db = get_db()
        return list(db["questions"].find({"skill": skill, "difficulty": difficulty}))
    except Exception:
        return []


if __name__ == "__main__":
    seed_skill_tree()
