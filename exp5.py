from langgraph.graph import StateGraph, START, END
from math import sqrt
from typing import TypedDict
import os
import sys
import io
import contextlib
import re
import requests
import json


def append_to_file(file_path, text_to_append,header=""):
    """
    Appends a string to the specified file.
    
    Args:
        file_path (str): Path to the file
        text_to_append (str): String to append to the file
    
    Returns:
        bool: True if successful, False if an error occurred
    """
    try:

        text_to_append= f"{header}\n==============\n{text_to_append}\n\n\n\n"
        with open(file_path, 'a', encoding='utf-8') as file:
            file.write(text_to_append)
            
        print(" appendedED ")
        return True
    except Exception as e:
        print(f"Error appending to file: {e}")
        return False







class AgentState(TypedDict):
    s: str
    file_path: str
    file_content: str

def get_file_input(state: AgentState) -> AgentState:
    """
    Function to get file path and task description from user, then read the file.
    """
    
    
    # Get file path from user
    file_path = input("Enter the file path: ").strip()
    
    # Get task description
    task_description = input("What would you like to do with this file? ").strip()
    
    # Try to read the file
    file_content = ""
    try:
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                file_content = f.read()
            print(f"Successfully read file: {file_path}")
        else:
            print(f"Warning: File not found at {file_path}")
            file_content = f"File not found at {file_path}"
    except Exception as e:
        print(f"Error reading file: {e}")
        file_content = f"Error reading file: {e}"
    
    
    combined_prompt = f"""
Task: {task_description}

File Path: {file_path}

File Content:
{file_content}

Please provide Python code to accomplish the requested task with this file.
"""
    append_to_file("log.txt", combined_prompt,"get_file_input")  # Append the prompt to the file
    return AgentState(
        s=combined_prompt,
        file_path=file_path,
        file_content=file_content
    )   

def ask_llm(state: AgentState) -> AgentState:
    """
    Function to send a question to the Ollama API and return the response.
    """
    print("=== Asking LLM ===")
    url = "http://localhost:11434/api/chat"
    payload = {
        "model": "qwen2:7b",  # Ensure this matches the model you pulled
        "messages": [{"role": "user", "content": state["s"]}]
    }
    
    response = requests.post(url, json=payload, stream=True)

    ret = AgentState(
        s="",
        file_path=state.get("file_path", ""),
        file_content=state.get("file_content", "")
    )
    
    if response.status_code == 200:
        for line in response.iter_lines(decode_unicode=True):
            if line:  # Ignore empty lines
                try:
                    json_data = json.loads(line)
                    if "message" in json_data and "content" in json_data["message"]:
                        ret["s"] = ret["s"] + json_data["message"]["content"]
                except json.JSONDecodeError:
                    print(f"\nFailed to parse line: {line}")
                    return ret
        print() 
        print("LLM response received successfully!")
        append_to_file("log.txt", ret["s"],"ask_llm")   
        return ret
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
        append_to_file("log.txt", f"Error: {response.status_code}\n{response.text}","ask_llm")
        return ret
    
def extract_python_code(agent_state: AgentState) -> AgentState:
    """
    Extract Python code from LLM response.
    """
 
    
    # Match code blocks marked with ```python ... ```
    code_blocks = re.findall(r"```python\s(.*?)```", agent_state["s"], re.DOTALL) # type: ignore

    # If no language tag, try generic code blocks (``` ... ```)
    if not code_blocks:
        code_blocks = re.findall(r"```\s*(.*?)```", agent_state["s"], re.DOTALL) # type: ignore

    # Combine all code blocks into one string
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
        # Create a globals dictionary with common imports and the file info
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

# Create the graph
graph = StateGraph(AgentState)

# Add nodes
graph.add_node("get_file_input", get_file_input)
graph.add_node("ask_llm", ask_llm)
graph.add_node("extract_python_code", extract_python_code)
graph.add_node("run_py", run_python_code)

# Define the flow
graph.add_edge(START, "get_file_input")
graph.add_edge("get_file_input", "ask_llm")
graph.add_edge("ask_llm", "extract_python_code")
graph.add_edge("extract_python_code", "run_py")
graph.add_edge("run_py", END)

# Compile the graph
app = graph.compile()




# Start with empty state - the file input node will populate it
initial_state = AgentState(s="", file_path="", file_content="")
result = app.invoke(initial_state)

print("\n=== Final Result ===")
print(result["s"])