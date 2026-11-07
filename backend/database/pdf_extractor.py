import os
import pdfplumber
import re
from mongo_skill_tree import get_db

PDF_DIR = "database/pdfs/"

def extract_questions_from_pdf(filepath, skill_tag):
    db = get_db()
    questions_col = db["questions"]
    
    text = ""
    with pdfplumber.open(filepath) as pdf:
        for page in pdf.pages:
            extracted = page.extract_text()
            if extracted:
                text += extracted + "\n"
                
    # This is a generic parser. It assumes questions are numbered (e.g. "1. Question?")
    # and have options a), b), c), d) followed by "Answer: "
    # We will refine this regex based on the exact format of your provided PDFs.
    
    question_blocks = re.split(r'\n(?=\d+\.)', text)
    inserted = 0
    
    for block in question_blocks:
        if not block.strip() or not re.match(r'^\d+\.', block.strip()):
            continue
            
        try:
            # Very basic fallback extraction logic
            lines = [line.strip() for line in block.split('\n') if line.strip()]
            q_text = lines[0]
            options = [line for line in lines[1:] if not line.lower().startswith('answer')]
            answer = next((line for line in lines if line.lower().startswith('answer')), "Unknown")
            
            doc = {
                "skill": skill_tag,
                "question": q_text,
                "options": options,
                "correct_answer": answer,
                "difficulty": "Medium" # Default until adaptive controller scales it
            }
            questions_col.insert_one(doc)
            inserted += 1
        except Exception as e:
            print(f"Failed to parse block: {block[:50]}... Error: {e}")
            
    print(f"Extracted and inserted {inserted} questions for {skill_tag} from {filepath}")

def run_extraction():
    if not os.path.exists(PDF_DIR):
        os.makedirs(PDF_DIR)
        print(f"Created {PDF_DIR} directory. Please place your PDFs here.")
        return
        
    for filename in os.listdir(PDF_DIR):
        if filename.endswith(".pdf"):
            # Derive skill tag from filename (e.g., "OS_questions.pdf" -> "OS")
            skill_tag = filename.split('_')[0].upper()
            extract_questions_from_pdf(os.path.join(PDF_DIR, filename), skill_tag)

if __name__ == "__main__":
    run_extraction()
