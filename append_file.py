#from requirements import START, END, StateGraph, TypedDict, io, contextlib, os, sys, re, json ,requests  
#
#def append_to_file(file_path, text_to_append,header=""):
#    """
#    Appends a string to the specified file.
#    
#    Args:
#        file_path (str): Path to the file
#        text_to_append (str): String to append to the file
#    
#    Returns:
#        bool: True if successful, False if an error occurred
#    """
#    try:
#
#        text_to_append= f"{header}\n==============\n{text_to_append}\n\n\n\n"
#        with open(file_path, 'a', encoding='utf-8') as file:
#            file.write(text_to_append)
#            
#        
#        return True
#    except Exception as e:
#        print(f"Error appending to file: {e}")
#        return False
#    
#
#




import os
import sys
import re
import json
import io
import contextlib
import requests
from typing import TypedDict
# If these are in your own module:
# from requirements import START, END, StateGraph

def append_to_file(file_path, text_to_append, header=""):
    """
    Appends a string (with optional header) to the specified file.

    Args:
        file_path (str): Path to the file
        text_to_append (str): String to append to the file
        header (str): Optional header to prepend to the text

    Returns:
        bool: True if successful, False if an error occurred
    """
    try:
        formatted_text = f"{header}\n==============\n{text_to_append}\n\n\n\n"
        with open(file_path, 'a', encoding='utf-8') as file:
            file.write(formatted_text)
        return True
    except Exception as e:
        print(f"Error appending to file: {e}")
        return False
