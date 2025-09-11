import glob
from langchain_community.document_loaders import PyPDFLoader
from langchain.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from models import ResumeModel
from dotenv import load_dotenv
import json

load_dotenv()

model = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)
structure_output = model.with_structured_output(ResumeModel)

def load_resumes(folder_path: str):
    files = glob.glob(folder_path + "/*.pdf")
    resumes = []
    for f in files:
        loader = PyPDFLoader(f)
        docs = loader.load()
        full_text = " ".join([d.page_content for d in docs])
        resumes.append({"text": full_text})
    return resumes

def parse_resumes(resume_texts):
    template = PromptTemplate(
        template="""
        You are a resume parser. Extract the following info and return strictly valid JSON:
        - name
        - email
        - phone
        - skills (list)
        - year_of_exp
        Resume Text:
        {context}
        """,
        input_variables=["context"],
    )

    results = []
    for resume in resume_texts:
        formatted = template.format(context=resume["text"])
        response = structure_output.invoke(formatted)
        results.append(response.model_dump())
    return results

def tag_candidates(parsed_resumes):
    emp_tag = []
    for i in parsed_resumes:
        tags = {
            "name": i["name"],
            "ExpYear": i["year_of_exp"],
            "isbackend": any(skill in ["Python", "Django", "SQL"] for skill in i["skills"]),
            "isFrontend": any(skill in ["React", "JavaScript", "HTML", "CSS"] for skill in i["skills"]),
            "isAI": any(skill in ['AI', 'ML', 'NLP', 'RAG', 'LangChain'] for skill in i["skills"]),
            "isPython": any(skill == "Python" for skill in i["skills"]),
            "Technical skills": i["skills"]
        }
        emp_tag.append(tags)
    return emp_tag
