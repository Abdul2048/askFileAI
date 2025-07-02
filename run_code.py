from requirements import START, END, StateGraph, TypedDict, io, contextlib, os, sys, re, json ,requests  
from append_file import append_to_file
from state import AgentState

def run_python_code(state: AgentState) -> AgentState:
    """
    Execute the extracted Python code.
    """
   
    code_str = state["s"]
    output = io.StringIO()
    
    if not code_str.strip():
        append_to_file("log.txt", "No code to execute","run_python_code")
        return AgentState(
            s="No code to execute",
            file_path=state.get("file_path", ""),
            file_content=state.get("file_content", "")
        )
    
    try:
        globals_dict = {
            '__builtins__': __builtins__,
            'os': os,
            'sys': sys,
            'io': io,
            're': re,
            'json': json,
            'file_path': state.get("file_path", ""),
            'file_content': state.get("file_content", "")
        }
        
        with contextlib.redirect_stdout(output), contextlib.redirect_stderr(output):
            exec(code_str, globals_dict)
    except Exception as e:
        output.write(f"Exception: {e}")
    
    append_to_file("log.txt", f"\nExecution Output:\n{output.getvalue()}\n","run_python_code")
    return AgentState(
        s=output.getvalue(),
        file_path=state.get("file_path", ""),
        file_content=state.get("file_content", "")
    )
