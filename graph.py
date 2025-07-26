from langgraph.graph import StateGraph, END          # For defining the graph and its end
from typing import TypedDict, Literal, List           # For type-safe state definitions
from qa_agent import answer_question
from search import search_arxiv
from summarizer import summarize_text

class Paper(TypedDict):
    title: str
    id: str
    authors: List[str]
    summary: str
    pdf_url: str
    published: str
    simple_summary: str  # This will be filled by Gemini

class ResearchState(TypedDict):
    query: str
    status: Literal["searching", "summarizing", "ready_for_qa"]
    papers: List[Paper]
    question : str
    answer : str
    

def search_node(state : ResearchState) -> ResearchState:
    query = state["query"]
    papers = search_arxiv(query)["papers"]
    
    for p in papers:
        p["simple_summary"] = ""
    
    return{
        "query" : query,
        "status" : "summarizing",
        "papers" : papers
    
    }
    
def summarize_node(state : ResearchState) -> ResearchState:
    updated_papers = []
    
    for paper in state["papers"]:
        simplified = summarize_text(paper["summary"])
        paper["simple_summary"] = simplified
        updated_papers.append(paper)

    return {
        "query": state["query"],
        "status": "ready_for_qa",
        "papers": updated_papers
    }    

def qa_node(state : ResearchState) -> ResearchState:
    question = state["question"]
    # concat all chunks
    context = "\n\n".join([p["simple_summary"] for p in state["papers"]])
    final_answer = answer_question(question = question,context =  context)
    
    return {
        "query": state["query"],
        "papers": state["papers"],
        "question": question,
        "answer": final_answer.strip(),
        "status": "answered"
    }


def build_graph():
    builder = StateGraph(ResearchState)
    builder.add_node("search", search_node)
    builder.add_node("summarize", summarize_node)
    builder.add_node("qa", qa_node)
    
    builder.set_entry_point("search")
    builder.add_edge("search","summarize")
    builder.add_edge("summarize","qa")
    builder.add_edge("qa", END)
    
    return builder.compile()

graph = build_graph()