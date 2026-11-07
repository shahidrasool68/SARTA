import sqlite3
import json

# This module simulates the Skill Tree Question Bank (Knowledge Graph).
# It will load questions seeded via the Hybrid approach into an SQLite database.

DB_PATH = "skill_tree.db"

def init_db():
    """Initialize the SQLite database with the Skill Tree schema."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Skills / Nodes in the graph
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS skills (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE NOT NULL,
        prerequisite_id INTEGER,
        FOREIGN KEY(prerequisite_id) REFERENCES skills(id)
    )
    ''')
    
    # Questions Bank
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS questions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        skill_id INTEGER,
        difficulty TEXT CHECK( difficulty IN ('Easy', 'Medium', 'Hard') ),
        question_text TEXT NOT NULL,
        options TEXT NOT NULL, -- JSON string of options
        correct_answer TEXT NOT NULL,
        FOREIGN KEY(skill_id) REFERENCES skills(id)
    )
    ''')
    
    conn.commit()
    conn.close()

def seed_database():
    """
    Placeholder for the Hybrid Seeding Approach.
    In reality, this would read from a JSON file compiled from Open Source repos and LLMs.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Example seeding
    try:
        cursor.execute("INSERT INTO skills (name) VALUES ('Python')")
        cursor.execute("INSERT INTO skills (name, prerequisite_id) VALUES ('Django', 1)")
        conn.commit()
    except sqlite3.IntegrityError:
        pass # Already seeded
        
    conn.close()

if __name__ == "__main__":
    init_db()
    seed_database()
    print("Skill Tree database initialized successfully.")
