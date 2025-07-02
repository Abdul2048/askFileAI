from requirements import START, END, StateGraph, TypedDict, io, contextlib, os, sys, re, json ,requests  
from append_file import append_to_file
from state import AgentState


def extract_python_code(agent_state: AgentState) -> AgentState:
    """
    Extract Python code from LLM response.
    """
 
    code_blocks = re.findall(r"```python\s(.*?)```", agent_state["s"], re.DOTALL) 

    if not code_blocks:
        code_blocks = re.findall(r"```\s*(.*?)```", agent_state["s"], re.DOTALL) 

    extracted_code = "\n".join(code_blocks) if code_blocks else ""
    
    if extracted_code:
        print("Code extracted successfully!")
    else:
        print("No code blocks found in LLM response")
   
    append_to_file("log.txt", f"\nExtracted Code:\n{extracted_code}\n","extract_python_code")
    return AgentState(
        s=extracted_code,
        file_path=agent_state.get("file_path", ""),
        file_content=agent_state.get("file_content", "")
    )