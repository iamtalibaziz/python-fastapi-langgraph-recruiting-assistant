from langchain_openai import ChatOpenAI
from app.helpers.helper import extract_text_from_resume, search_candidate_web
from app.helpers.llm_prompts import resume_node_prompt, jd_node_prompt, compare_node_prompt
from app.helpers.mock_data import resume_node_mock_data, jd_node_mock_data, compare_node_mock_data
from dotenv import load_dotenv
import json
import re
import os

# Load environment variables
load_dotenv()
os.environ['OPENAI_API_KEY'] = os.getenv("OPENAI_API_KEY")
is_mock_test = os.getenv("MOCK_TEST", "False").lower() in ("true", "1", "yes")

llm = ChatOpenAI(model="gpt-4", temperature=0.2)

def search_node(state):
    name = state['candidate_name']
    return {"web_data": search_candidate_web(name)}

def resume_node(state):
    resume_file = state['resume_file']
    text = extract_text_from_resume(resume_file)
    prompt = resume_node_prompt(text)
    if (is_mock_test):
        return {"resume_data": resume_node_mock_data()}
    
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
    prompt = jd_node_prompt(jd)
    if (is_mock_test):
        return {"jd_summary": jd_node_mock_data()}

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

    prompt = compare_node_prompt(resume_data, jd_summary)
    if (is_mock_test):
        return compare_node_mock_data()
    
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