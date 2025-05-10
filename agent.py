from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from helper import extract_text_from_resume, parse_resume, search_candidate_web, compare_profile_to_jd
from schemas import FitResult, CandidateProfile
import os
from dotenv import load_dotenv
from typing import TypedDict, Any
import json

# Load environment variables
load_dotenv()
os.environ['OPENAI_API_KEY'] = os.getenv("OPENAI_API_KEY")


llm = ChatOpenAI(model="gpt-4", temperature=0.2)

def search_node(state):
    name = state['candidate_name']
    return {"web_data": search_candidate_web(name)}

def resume_node(state):
    resume_file = state['resume_file']
    text = extract_text_from_resume(resume_file)
    prompt = """
    Parses and analyzes the candidate resume mentioned below:\n
    Resume Content: {text}\n
    Return the experience, required skills and required qualifications as JSON format like : { name: 'abc', email: 'abc@gmail.com', phone: '99898393', experience: 'x', skills: ['a', 'b', 'c'], qualifications: ['a', 'b'], certifications: ['a', 'b'], publications: ['a', 'b'], projects: ['a', 'b'] }
    if Not matched then return as empty JSON format like : { name: '', email: '', phone: '', experience: '', skills: [], qualifications: [], certifications: [], publications: [], projects: [] }
    """
    data = llm.invoke(prompt)
    resume_data = json.loads(data.content)
    return {"resume_data": resume_data}

def jd_node(state):
    jd = state['job_description']
    prompt = """
    Summarize and extract core requirements from this job description:\n
    Job Description:{jd}\n
    Return the experience, required skills and required qualifications as JSON format like : { experience: 'x', skills: ['a', 'b', 'c'], qualifications: ['a', 'b'] }
    if Not matched then return as empty JSON format like :  { experience: 'x', skills: [], qualifications: [] }
    """
    summary = llm.invoke(prompt)
    jd_summary = json.loads(summary.content)
    return {"jd_summary": jd_summary}

def compare_node(state):
    resume_data = state['resume_data']
    jd_summary = state['jd_summary']
    score, matrix, explanation = compare_profile_to_jd(resume_data, jd_summary)
    return {
        "fit_score": score,
        "comparison_matrix": matrix,
        "explanation": explanation
    }


class AgentState(TypedDict):
    candidate_name: str
    resume_file: Any  # UploadFile or file-like object
    job_description: str
    web_data: dict
    resume_data: dict
    jd_summary: dict
    fit_score: str
    comparison_matrix: dict
    explanation: str

# Define LangGraph workflow
graph = StateGraph(state_schema=AgentState)
graph.add_node("search", search_node)
graph.add_node("resume", resume_node)
graph.add_node("jd_parse", jd_node)
graph.add_node("compare", compare_node)

graph.set_entry_point("search")
graph.add_edge("search", "resume")
graph.add_edge("resume", "jd_parse")
graph.add_edge("jd_parse", "compare")
graph.set_finish_point("compare")

workflow = graph.compile()

async def run_agent(candidate_name, resume_file, job_description):
    state = {
        "candidate_name": candidate_name,
        "resume_file": resume_file,
        "job_description": job_description,
    }
    result = workflow.invoke(state)

    profile_data = {
        "name": candidate_name,
        **result.get("resume_data", {}),
        "web_links": result.get("web_data", {})
    }
    profile = CandidateProfile(**profile_data)
    output = FitResult(
        fit_score=result["fit_score"],
        profile=profile,
        comparison_matrix=result["comparison_matrix"],
        explanation=result["explanation"]
    )
    return output.dict()