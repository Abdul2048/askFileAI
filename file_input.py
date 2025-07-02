from requirements import START, END, StateGraph, TypedDict, io, contextlib, os, sys, re, json ,requests  
from append_file import append_to_file
from state import AgentState


def get_file_input(state: AgentState) -> AgentState:
    """
    Function to get file path and task description from user, then read the file.
    """
    
    file_path = input("Enter the file path: ").strip()    
    task_description = input("What would you like to do with this file? ").strip()
    
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
    append_to_file("log.txt", combined_prompt,"get_file_input")  
    return AgentState(
        s=combined_prompt,
        file_path=file_path,
        file_content=file_content
    )   