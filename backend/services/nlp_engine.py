import os
os.environ.setdefault("HF_HUB_OFFLINE", "1")
os.environ.setdefault("TRANSFORMERS_OFFLINE", "1")

import spacy
from spacy.matcher import PhraseMatcher
from sentence_transformers import SentenceTransformer
import re

# Ensure spacy model is downloaded or handle it gracefully
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    print("Downloading spaCy model en_core_web_sm...")
    os.system("python -m spacy download en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")

# Lazy SBERT model loader
_model = None

def get_model():
    global _model
    if _model is None:
        print("Loading SentenceTransformer model...")
        try:
            _model = SentenceTransformer('all-MiniLM-L6-v2', local_files_only=True)
        except Exception:
            _model = SentenceTransformer('all-MiniLM-L6-v2')
        print("Model loaded.")
    return _model

# ─── Curated Skill Taxonomy ────────────────────────────────────────────
# This is the canonical list of skills that SARTA recognizes.
# spaCy NER alone cannot reliably extract tech skills because it was
# trained on news articles, not resumes. A PhraseMatcher over a known
# taxonomy is the standard approach for domain-specific NER.
SKILL_TAXONOMY = [
    # Languages
    "Python", "JavaScript", "TypeScript", "Java", "C++", "C#", "C",
    "Go", "Rust", "Ruby", "PHP", "Swift", "Kotlin", "Scala", "R",
    "Perl", "Lua", "Dart", "Elixir", "Haskell", "MATLAB",
    # Frontend
    "React", "Angular", "Vue", "Vue.js", "Next.js", "Nuxt.js",
    "Svelte", "HTML", "CSS", "Sass", "SCSS", "TailwindCSS", "Tailwind",
    "Bootstrap", "jQuery", "Redux", "Webpack", "Vite",
    # Backend
    "Node.js", "Express", "Express.js", "Django", "Flask", "FastAPI",
    "Spring", "Spring Boot", ".NET", "ASP.NET", "Ruby on Rails", "Rails",
    "Laravel", "NestJS", "Gin", "Fiber",
    # Databases
    "SQL", "PostgreSQL", "MySQL", "MongoDB", "Redis", "Cassandra",
    "DynamoDB", "SQLite", "Oracle", "MariaDB", "Neo4j", "Elasticsearch",
    "Firebase", "Firestore", "CouchDB",
    # Cloud & DevOps
    "AWS", "Azure", "GCP", "Google Cloud", "Docker", "Kubernetes",
    "Terraform", "Ansible", "Jenkins", "GitHub Actions", "CI/CD",
    "CI", "CD", "CircleCI", "Travis CI", "ArgoCD", "Helm",
    "Nginx", "Apache", "Linux", "Bash",
    # Data / ML / AI
    "Machine Learning", "Deep Learning", "TensorFlow", "PyTorch",
    "Keras", "Scikit-learn", "Pandas", "NumPy", "Spark", "Hadoop",
    "Kafka", "Airflow", "NLP", "Computer Vision", "OpenCV",
    "LLM", "GPT", "Transformers", "Hugging Face",
    # Tools & Practices
    "Git", "GitHub", "GitLab", "Bitbucket", "JIRA", "Confluence",
    "Agile", "Scrum", "REST", "REST API", "GraphQL", "gRPC",
    "Microservices", "System Design", "Design Patterns",
    "Object Oriented Programming", "OOP", "Data Structures",
    "Algorithms", "Unit Testing", "Integration Testing",
    "Jest", "Mocha", "Pytest", "Selenium", "Cypress",
    # Mobile
    "React Native", "Flutter", "SwiftUI", "Android", "iOS",
    "Xamarin", "Ionic",
    # Misc
    "RabbitMQ", "WebSocket", "OAuth", "JWT", "SAML",
    "Figma", "Adobe XD", "Photoshop",
    "Power BI", "Tableau", "D3.js",
    "Blockchain", "Solidity", "Web3",
    "Version Control",
]

# ─── Deduplication / Subsumption Rules ──────────────────────────────
# Maps a "parent" skill to its children that should be removed when
# the parent is present. Also handles merge rules (CI + CD → CI/CD).
SKILL_MERGE_RULES = [
    # If both CI and CD are found, merge them into CI/CD and drop the parts
    {"parts": {"CI", "CD"}, "merged": "CI/CD"},
]

SKILL_SUBSUMPTIONS = {
    # If Git is present, Version Control is redundant
    "Git": ["Version Control"],
    # Add more rules as needed, e.g.:
    # "AWS": ["Cloud Computing"],
}

def _deduplicate_skills(skills: set[str]) -> set[str]:
    """
    Post-process extracted skills to remove redundant / overlapping entries:
    1. Merge rules: e.g. CI + CD → CI/CD
    2. Subsumption: e.g. Git present → drop Version Control
    """
    result = set(skills)

    # ── Merge rules ───────────────────────────────────────────────────
    for rule in SKILL_MERGE_RULES:
        if rule["parts"].issubset(result):
            result -= rule["parts"]
            result.add(rule["merged"])

    # ── Subsumption rules ─────────────────────────────────────────────
    for parent, children in SKILL_SUBSUMPTIONS.items():
        if parent in result:
            for child in children:
                result.discard(child)

    return result

def _build_phrase_matcher():
    """Build a spaCy PhraseMatcher from the skill taxonomy."""
    matcher = PhraseMatcher(nlp.vocab, attr="LOWER")
    patterns = [nlp.make_doc(skill) for skill in SKILL_TAXONOMY]
    matcher.add("SKILLS", patterns)
    return matcher

_phrase_matcher = _build_phrase_matcher()

def extract_skills(text: str) -> list[str]:
    """
    Extract technical skills from text using a two-pass approach:
    
    Pass 1 — PhraseMatcher: Scans the text against our curated skill taxonomy
             using spaCy's fast PhraseMatcher (case-insensitive). This catches
             exact and near-exact matches like "Python", "CI/CD", "Machine Learning".
    
    Pass 2 — Regex comma/bullet splitter: Resumes often list skills in 
             comma-separated or bullet-point lists. We split those and check
             each token against the taxonomy for any stragglers the matcher missed.
    """
    doc = nlp(text)
    found_skills = set()

    # ── Pass 1: PhraseMatcher ──────────────────────────────────────────
    matches = _phrase_matcher(doc)
    for match_id, start, end in matches:
        span_text = doc[start:end].text.strip()
        # Normalize to canonical taxonomy casing
        lower = span_text.lower()
        for canonical in SKILL_TAXONOMY:
            if canonical.lower() == lower:
                found_skills.add(canonical)
                break

    # ── Pass 2: Split comma / bullet lists and check taxonomy ─────────
    # Handles lines like "Python, JavaScript, React, Node.js, Express"
    taxonomy_lower = {s.lower(): s for s in SKILL_TAXONOMY}
    # Split on commas, bullet chars, pipes, semicolons, and newlines
    # NOTE: Do NOT split on '/' — it breaks compound skills like "CI/CD"
    tokens = re.split(r'[,\n;|•·]', text)
    for token in tokens:
        cleaned = token.strip().rstrip('.').strip('- ')
        if cleaned.lower() in taxonomy_lower:
            found_skills.add(taxonomy_lower[cleaned.lower()])

    # ── Post-processing: Deduplicate / merge / subsume ────────────────
    found_skills = _deduplicate_skills(found_skills)

    return sorted(found_skills)

def compute_embeddings(skills: list[str]):
    """
    Convert a list of skill strings into SBERT embeddings for semantic matching.
    """
    if not skills:
        return []
    return get_model().encode(skills)
