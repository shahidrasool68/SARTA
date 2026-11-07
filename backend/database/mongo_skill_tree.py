from pymongo import MongoClient

MONGO_URI = "mongodb+srv://thesyedanas01_db_user:4IfQNTC75xcjViVB@minor-project-cluster.rl4fsau.mongodb.net/?appName=minor-project-cluster"
DB_NAME = "sarta_db"

def get_db():
    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=1000, connectTimeoutMS=1000)
    return client[DB_NAME]

def seed_mongo_database():
    """
    Seed MongoDB with our conceptual Skill Tree.
    Instead of hard relational joins, we use document arrays.
    """
    db = get_db()
    questions_col = db["questions"]
    skills_col = db["skills"]
    
    # Example Conceptual Skill Tree nodes
    skills = [
        {"name": "Python", "prerequisites": []},
        {"name": "Django", "prerequisites": ["Python"]},
        {"name": "FastAPI", "prerequisites": ["Python"]},
        {"name": "React", "prerequisites": ["JavaScript", "HTML", "CSS"]},
        {"name": "Next.js", "prerequisites": ["React"]}
    ]
    
    # Upsert skills to avoid duplicates on multiple runs
    for skill in skills:
        skills_col.update_one({"name": skill["name"]}, {"$set": skill}, upsert=True)
        
    print("MongoDB Atlas conceptually seeded with Skill Tree prerequisites!")

if __name__ == "__main__":
    seed_mongo_database()