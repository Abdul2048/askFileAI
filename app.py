from requirements import START, END, StateGraph, TypedDict, io, contextlib, os, sys, re, json ,requests  
from append_file import append_to_file
from file_input import get_file_input
from askllm import ask_llm
from extract_code import extract_python_code
from run_code import run_python_code
from state import AgentState

graph = StateGraph(AgentState)

graph.add_node("get_file_input", get_file_input)
graph.add_node("ask", ask_llm)
graph.add_node("extract_pythoncode", extract_python_code)
graph.add_node("run_py", run_python_code)

graph.add_edge(START, "get_file_input")
graph.add_edge("get_file_input", "ask")
graph.add_edge("ask", "extract_pythoncode")
graph.add_edge("extract_pythoncode", "run_py")
graph.add_edge("run_py", END)

app = graph.compile()

initial_state = AgentState(
    s="",
    file_path="",
    file_content=""
)
result = app.invoke(initial_state)

print("\n=== Final Result ===")
print(result["s"])
