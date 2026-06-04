"""
NexusAI — LangGraph ReAct agent.

Graph architecture:
    START → tool_calling_llm ↔ tools → END

Tools registered:
    - TavilySearch  (web search)
    - multiply      (integer multiplication)
"""
import os
from pathlib import Path
from typing import Annotated
from typing_extensions import TypedDict

from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, AIMessage
from langchain_groq import ChatGroq
from langchain_tavily import TavilySearch
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition

# Load .env from project root regardless of working directory
load_dotenv(dotenv_path=Path(__file__).parent.parent.parent / ".env", override=True)


class State(TypedDict):
    messages: Annotated[list, add_messages]


def build_agent():
    """Build and return the compiled LangGraph ReAct agent."""
    llm = ChatGroq(
        model="llama-3.3-70b-versatile",
        api_key=os.getenv("GROQ_API_KEY"),
    )

    search = TavilySearch(max_results=2)

    def multiply(a: int, b: int) -> int:
        """Multiply a and b.

        Args:
            a: first integer
            b: second integer

        Returns:
            Product of a and b
        """
        return a * b

    tools = [search, multiply]
    llm_with_tools = llm.bind_tools(tools)

    def tool_calling_llm(state: State):
        return {"messages": [llm_with_tools.invoke(state["messages"])]}

    builder = StateGraph(State)
    builder.add_node("tool_calling_llm", tool_calling_llm)
    builder.add_node("tools", ToolNode(tools))

    builder.add_edge(START, "tool_calling_llm")
    builder.add_conditional_edges("tool_calling_llm", tools_condition)
    builder.add_edge("tools", "tool_calling_llm")  # ReAct loop

    return builder.compile()


def run_agent(agent, user_message: str, chat_history: list = None) -> str:
    """Run the agent and return the final text response.

    Args:
        agent: compiled LangGraph graph from build_agent()
        user_message: current user prompt
        chat_history: list of {"role": "user"|"assistant", "content": str}

    Returns:
        Final AI response string
    """
    messages = []

    if chat_history:
        for msg in chat_history:
            if msg["role"] == "user":
                messages.append(HumanMessage(content=msg["content"]))
            elif msg["role"] == "assistant":
                messages.append(AIMessage(content=msg["content"]))

    messages.append(HumanMessage(content=user_message))

    result = agent.invoke({"messages": messages})
    return result["messages"][-1].content
