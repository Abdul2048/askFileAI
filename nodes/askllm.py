from nodes.requirements import START, END, StateGraph, TypedDict, io, contextlib, os, sys, re, json ,requests  
from append_file import append_to_file
from nodes.state import AgentState

#
def ask_llm(state: AgentState) -> AgentState:
    """
    Function to send a question to the Ollama API and return the response.
    """
    print("=== Asking LLM ===")
    url = "http://localhost:11434/api/chat"
    payload = {
        "model": "qwen2:7b", 
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
            if line: 
                try:
                    json_data = json.loads(line)
                    if "message" in json_data and "content" in json_data["message"]:
                        ret["s"] = ret["s"] + json_data["message"]["content"]
                except json.JSONDecodeError:
                    print(f"\nFailed to parse line: {line}")
                    return ret
        print() 
        append_to_file("log.txt", ret["s"],"ask_llm")   
        return ret
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
        append_to_file("log.txt", f"Error: {response.status_code}\n{response.text}","ask_llm")
        return ret