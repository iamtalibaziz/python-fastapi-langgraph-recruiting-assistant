from fastapi import HTTPException
from langchain_openai import ChatOpenAI
from app.helpers.helper import extract_text_from_resume, search_candidate_web
from app.helpers.llm_prompts import resume_node_prompt, jd_node_prompt, compare_node_prompt
from app.helpers.mock_data import resume_node_mock_data, jd_node_mock_data, compare_node_mock_data
import json
import re
import os
from app.configs.app_config import app_config

os.environ['OPENAI_API_KEY'] = app_config.OPENAI_API_KEY
is_mock_test = app_config.MOCK_TEST

llm = ChatOpenAI(model="gpt-4", temperature=0.2)

def search_node(state):
    name = state['candidate_name']
    return {"web_data": search_candidate_web(name)}

def resume_node(state):
    resume_file = state['resume_file']
    text = extract_text_from_resume(resume_file)
    if not text:  # Check if the value is empty
        raise HTTPException(status_code=400, detail="Error: Invalid resume file, only (.pdf, .docx) allowed")
    
    prompt = resume_node_prompt(text)
    if (is_mock_test):
        return {"resume_data": resume_node_mock_data()}
    
    content = llm.invoke(prompt).content
    json_data = parse_llm_content_to_json(content)
    if (json_data):
        return {"resume_data": json_data}
    
    return {"resume_data": {}}


def jd_node(state):
    jd = state['job_description']
    prompt = jd_node_prompt(jd)
    if (is_mock_test):
        return {"jd_summary": jd_node_mock_data()}

    summary = llm.invoke(prompt).content
    json_data = parse_llm_content_to_json(summary)
    if (json_data):
        return {"jd_summary": json_data}
    
    return {"jd_summary": {}}


def compare_node(state):
    resume_data = state['resume_data']
    jd_summary = state['jd_summary']

    prompt = compare_node_prompt(resume_data, jd_summary)
    if (is_mock_test):
        return compare_node_mock_data()
    
    comparison_content = llm.invoke(prompt).content
    json_data = parse_llm_content_to_json(comparison_content)
    if (json_data):
        return json_data
    
    return { "fit_score": "", "comparison_matrix": { "skills_matched": [], "experience": "" }, "explanation": "" }
    
def parse_llm_content_to_json(content):
    match = re.search(r"\{.*\}", content, re.DOTALL)
    if match:
        try:
            json_data = json.loads(match.group())
            return json_data
        except json.JSONDecodeError as e:
            print("parse_llm_content_to_json JSON decode error:", e)
    else:
        print("parse_llm_content_to_json No JSON object found in the response.")
    return None