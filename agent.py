from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from helper import extract_text_from_resume, search_candidate_web, compare_profile_to_jd
import os
from dotenv import load_dotenv
from typing import TypedDict, Any
import json
import re

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
    prompt = f"""
    Parses and analyzes the candidate resume mentioned below:\n
    Resume Content:
    {text}\n
    Return the experience, required skills and required qualifications as JSON format like : {{ name: 'abc', email: 'abc@gmail.com', phone: '99898393', experience: 'x', skills: ['a', 'b', 'c'], qualifications: ['a', 'b'], certifications: ['a', 'b'], publications: ['a', 'b'], projects: ['a', 'b'] }}
    if Not matched then return as empty JSON format like : {{ name: '', email: '', phone: '', experience: '', skills: [], qualifications: [], certifications: [], publications: [], projects: [] }}
    """
    # mockJSON = {'name': 'John', 'email': 'john.test@gmail.com', 'phone': '+91240343093', 'experience': 'Over 8+ years of experience with JavaScript, Node.js, MongoDB, Express.js, Nest.js, TypeScript, ES6, React.js and Redux, jQuery, MySQL, Ajax, Socket.IO, Redis. Experienced in developing large Application. Experienced in implementing Payment system using Stripe. Experienced in writing complex database queries.', 'skills': ['JavaScript', 'Node.js', 'MongoDB', 'Express.js', 'Nest.js', 'TypeScript', 'ES6', 'React.js and Redux', 'jQuery', 'MySQL', 'Ajax', 'Socket.IO', 'Redis', 'Python', 'FastAPI', 'Generative AI'], 'qualifications': ['MCA from Sikkim Manipal University (January, 2014)'], 'certifications': [], 'publications': [], 'projects': []}
    # return {"resume_data": mockJSON}
    content = llm.invoke(prompt).content
    match = re.search(r"\{.*\}", content, re.DOTALL)
    if match:
        try:
            resume_data = json.loads(match.group())
            print("Parsed JSON:", resume_data)
            return {"resume_data": resume_data}
        except json.JSONDecodeError as e:
            print("JSON decode error:", e)
            return {"resume_data": {}}
    else:
        print("No JSON object found in the response.")
        return {"resume_data": {}}

def jd_node(state):
    jd = state['job_description']
    prompt = f"""
    Summarize and extract core requirements from this job description:\n
    Job Description:{jd}\n
    Return the experience, required skills and required qualifications as JSON format like : {{ experience: 'x', skills: ['a', 'b', 'c'], qualifications: ['a', 'b'] }}
    if Not matched then return as empty JSON format like :  {{ experience: 'x', skills: [], qualifications: [] }}
    """
    # mockJSON = {'experience': '5 years', 'skills': ['JavaScript', 'Python', 'AI', 'Generative AI', 'MySQL'], 'qualifications': ['B.Tech', 'MCA']}
    # return {"jd_summary": mockJSON}
    summary = llm.invoke(prompt).content
    match = re.search(r"\{.*\}", summary, re.DOTALL)
    if match:
        try:
            jd_summary = json.loads(match.group())
            print("Parsed JSON:", jd_summary)
            return {"jd_summary": jd_summary}
        except json.JSONDecodeError as e:
            print("JSON decode error:", e)
            return {"jd_summary": {}}
    else:
        print("No JSON object found in the response.")
        return {"jd_summary": {}}

def compare_node(state):
    resume_data = state['resume_data']
    jd_summary = state['jd_summary']

    prompt = f"""
    Analyze resume data and job description requirements.\n
    Resume Data: {resume_data}
    Job Description:{jd_summary}\n
    Return the data as JSON format like: {{
        "fit_score": "Strong Fit, Moderate Fit, or Not a Fit",
        "comparison_matrix": {{
            "skills_matched": ["JavaScript", "Python"],
            "experience": "Return the experience"
        }},
        "explanation": "Explanation of the decision"
    }}
    if Not matched then return as empty JSON format like : {{
        "fit_score": "",
        "comparison_matrix": {{
            "skills_matched": [],
            "experience": ""
        }},
        "explanation": ""
    }}
    """
    # mockJSON = {
    #     "fit_score": "Strong Fit",
    #     "comparison_matrix": {
    #         "skills_matched": ["JavaScript", "Python", "Generative AI", "MySQL"],
    #         "experience": "Over 8+ years"
    #     },
    #     "explanation": "The candidate has over 8 years of experience, exceeding the required 5 years. They possess strong expertise in 4 out of 5 required skills (JavaScript, Python, Generative AI, MySQL) and meet the qualification requirement with an MCA. This makes them a strong fit for the position."
    # }
    # return mockJSON
    comparison_content = llm.invoke(prompt).content
    match = re.search(r"\{.*\}", comparison_content, re.DOTALL)
    if match:
        try:
            comparison_data = json.loads(match.group())
            print("comparison_data parsed JSON:", comparison_data)
            return comparison_data
        except json.JSONDecodeError as e:
            print("comparison_data JSON decode error:", e)
            return { "fit_score": "", "comparison_matrix": { "skills_matched": [], "experience": "" }, "explanation": "" }
    else:
        print("comparison_data No JSON object found in the response.")
        return { "fit_score": "", "comparison_matrix": { "skills_matched": [], "experience": "" }, "explanation": "" }


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
    return {
        "profile": profile_data,
        "fit_score": result["fit_score"],
        "comparison_matrix": result["comparison_matrix"],
        "explanation": result["explanation"]
    }