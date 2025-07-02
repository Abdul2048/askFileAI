from typing import TypedDict

class AgentState(TypedDict):
    s: str
    file_path: str
    file_content: str