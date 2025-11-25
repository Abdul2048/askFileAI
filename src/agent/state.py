from typing import TypedDict, List, Dict, Any

class AgentState(TypedDict):
    """State for LangGraph agent"""
    file_path: str
    question: str
    file_content: str
    chunks: List[Dict]
    embeddings: List[List[float]]
    retrieved_docs: List[Dict]
    answer: str
    conversation_history: List[Dict]
    error: str


# 
