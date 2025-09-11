from langchain.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from models import RecruiterDesc

model = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)
structured_des = model.with_structured_output(RecruiterDesc)

def select_best_candidate(eligible_candidates):
    template = PromptTemplate(
        template="""
        You are an expert technical recruiter.
        The role is "Backend AI Developer" which requires strong backend skills in Python and Django,
        and AI-related expertise (like RAG, NLP, LangChain, Generative AI) is a big plus.

        Candidates:
        {eligible}

        Task:
        1. From these candidates, select only the single best fit for the role.
        2. Provide a short explanation why this candidate is stronger than others.
        """,
        input_variables=["eligible"],
    )

    formatted = template.format(eligible=eligible_candidates)
    response = structured_des.invoke(formatted)
    return response.model_dump()
