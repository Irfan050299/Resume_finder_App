from fastapi import FastAPI
from parser import load_resumes, parse_resumes, tag_candidates
from recruiters import select_best_candidate

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Resume Parser API is running 🚀"}

@app.post("/process_resumes/")
def process_resumes(folder_path: str):
    resumes = load_resumes(folder_path)
    parsed = parse_resumes(resumes)
    tagged = tag_candidates(parsed)

    eligible = [c for c in tagged if c["isbackend"] and c["isPython"] and c["isAI"] and "Django" in c["Technical skills"]]
    
    if not eligible:
        return {"message": "No eligible candidate found"}
    
    best_candidate = select_best_candidate(eligible)
    return {
        "parsed": parsed,
        "eligible": eligible,
        "best_candidate": best_candidate
    }

