from dotenv import load_dotenv
import json , re , tempfile 
from pathlib import Path
from langchain_experimental.tools import PythonREPLTool
from langchain_core.tools import tool 
from ddgs import DDGS



load_dotenv()

@tool
def web_search(query):
    """Web Searching tool to search for a specific query"""
    try : 
        res = list(DDGS().text(query , max_results = 5))
        if not res : 
            return f"No results for {query}" 
        formmated_res = [f"Search results for {query} : \n"]
        for i,res in enumerate(res,1) : 
            title = res.get("title" , "no title")
            body = res.get("body", "No description availabe")
            href = res.get("href" , "")
            formmated_res.append(f"{i}. **{title}**\n  {href}\n\n  {body}\n ")
            return "\n\n".join(formmated_res)
    except Exception as e:
        return str(e)

@tool
def math(expressions):
    """Math tool for calculate math expressions"""
    math_tool = PythonREPLTool(expressions)
    return math_tool
