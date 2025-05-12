from langgraph.graph import StateGraph, END
from typing import TypedDict, Any
from app.helpers.agent_nodes import search_node, resume_node, jd_node, compare_node

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
# Define LangGraph edges
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