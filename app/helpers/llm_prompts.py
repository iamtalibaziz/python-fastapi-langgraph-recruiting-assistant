def resume_node_prompt(resume_content) -> str:
    return f"""
    Parses and analyzes the candidate resume mentioned below:\n
    Resume Content:
    {resume_content}\n
    Return the experience, required skills and required qualifications as JSON format like : {{ name: 'abc', email: 'abc@gmail.com', phone: '99898393', experience: 'x', skills: ['a', 'b', 'c'], qualifications: ['a', 'b'], certifications: ['a', 'b'], publications: ['a', 'b'], projects: ['a', 'b'] }}
    if Not matched then return as empty JSON format like : {{ name: '', email: '', phone: '', experience: '', skills: [], qualifications: [], certifications: [], publications: [], projects: [] }}
    """

def jd_node_prompt(jd_content) -> str:
    return f"""
    Summarize and extract core requirements from this job description:\n
    Job Description:{jd_content}\n
    Return the experience, required skills and required qualifications as JSON format like : {{ experience: 'x', skills: ['a', 'b', 'c'], qualifications: ['a', 'b'] }}
    if Not matched then return as empty JSON format like :  {{ experience: 'x', skills: [], qualifications: [] }}
    """

def compare_node_prompt(resume_content, jd_summary_content) -> str:
    return f"""
    Analyze resume data and job description requirements.\n
    Resume Data: {resume_content}
    Job Description:{jd_summary_content}\n
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