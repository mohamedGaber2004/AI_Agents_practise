# groq_graph.py

from langgraph.graph import StateGraph
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_groq import ChatGroq
from langchain.tools import tool
from langchain_core.messages import AnyMessage
from typing import TypedDict, List, Annotated
import operator
from dotenv import load_dotenv

load_dotenv()

class AgentState(TypedDict):
    messages: Annotated[List[AnyMessage], operator.add]

llm = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0
)

@tool
def add(a: int, b: int) -> int:
    """
    Add two numbers together.

    Args:
        a (int): The first number.
        b (int): The second number.

    Returns:
        int: The sum of a and b.
    """
    return a + b


@tool
def multiply(a: int, b: int) -> int:
    """
    Multiply two numbers together.

    Args:
        a (int): The first number.
        b (int): The second number.

    Returns:
        int: The product of a and b.
    """
    return a * b


@tool
def divide(a: float, b: float) -> float:
    """
    Divide one number by another.

    Args:
        a (float): The numerator.
        b (float): The denominator.

    Returns:
        float: The result of a divided by b.

    Raises:
        ValueError: If b is zero.
    """
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b

tools = [add, multiply, divide]

def agent_node(state: AgentState):
    llm_with_tools = llm.bind_tools(tools)
    response = llm_with_tools.invoke(state["messages"])
    return {"messages": [response]}

def build_graph():
    workflow = StateGraph(AgentState)

    workflow.add_node("agent", agent_node)
    workflow.add_node("tools", ToolNode(tools))

    workflow.set_entry_point("agent")
    workflow.add_conditional_edges("agent", tools_condition)
    workflow.add_edge("tools", "agent")

    return workflow.compile()

# 🔑 IMPORTANT: exposed graph
graph = build_graph()
