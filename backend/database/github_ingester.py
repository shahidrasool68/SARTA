import os
import csv
from mongo_skill_tree import get_db

REPO_DIR = "database/leetcode-company-wise-problems"

def fetch_dsa_questions():
    db = get_db()
    coding_col = db["coding_questions"]
    
    if not os.path.exists(REPO_DIR):
        print(f"Directory {REPO_DIR} not found. Please clone the repository first.")
        return
        
    inserted = 0
    # Walk through the directory structure
    for root, dirs, files in os.walk(REPO_DIR):
        company_name = os.path.basename(root)
        if company_name.startswith('.') or company_name == REPO_DIR:
            continue
            
        for file in files:
            if file.endswith(".csv"):
                filepath = os.path.join(root, file)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        reader = csv.DictReader(f)
                        for row in reader:
                            # Upsert to avoid duplicates, using Title as unique key for simplicity
                            doc = {
                                "title": row.get("Title", "Unknown"),
                                "difficulty": row.get("Difficulty", "MEDIUM"),
                                "link": row.get("Link", ""),
                                "topics": [t.strip() for t in row.get("Topics", "").split(",") if t.strip()],
                                "company": company_name
                            }
                            coding_col.update_one(
                                {"title": doc["title"]},
                                {"$set": doc, "$addToSet": {"companies": company_name}},
                                upsert=True
                            )
                            inserted += 1
                except Exception as e:
                    print(f"Error parsing {filepath}: {e}")
                    
    print(f"Successfully ingested {inserted} LeetCode questions across companies!")

if __name__ == "__main__":
    fetch_dsa_questions()
