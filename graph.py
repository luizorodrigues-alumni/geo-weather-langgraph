from typing import Literal
from state import State
from langchain.chat_models import init_chat_model
from langgraph.graph.state import CompiledStateGraph, StateGraph, START
from langgraph.checkpoint.memory import InMemorySaver
from langchain.messages import AIMessage, ToolMessage
from tools import TOOLS, TOOLS_BY_NAME
from dotenv import load_dotenv

load_dotenv()

def call_llm(state: State) -> State:
    """
    Calls the LLM with the current state's messages and returns the updated state with new messages.
    Args:
        state (State): The current state containing messages.
    Returns:
        State: The updated state with new messages from the LLM.    
    """
    print("call_llm")

    # LLM model with tools
    # llm = init_chat_model("ollama:llama3.1:8b").bind_tools(TOOLS)
    llm = init_chat_model("google_genai:gemini-2.5-flash-lite").bind_tools(TOOLS)

    # Invoking
    result = llm.invoke(state["messages"])
    return {"messages":result}

def tool_node(state: State) -> State:
    """
    Executes the tool call specified in the latest AI message of the state.
    Args:
        state (State): The current state containing messages.
    Returns:
        State: The updated state with the tool message added.
    """

    print("tool_node")

    # Get the last LLM response
    llm_response = state["messages"][-1]

    # Check for tool calls
    if not isinstance(llm_response, AIMessage) or not getattr(llm_response, "tool_calls"):
        return state
    
    # Get the last tool call and execute it
    call = llm_response.tool_calls[-1]
    name, args, _id = call["name"], call["args"], call["id"]
    try:
        content = TOOLS_BY_NAME[name].invoke(args)
    except (KeyError, IndexError, TypeError, ValueError) as e:
        content = f"Fix your mistakes: {e}"
    
    # Create ToolMessage and return updated state
    tool_message = ToolMessage(content=content, tool_call_id=_id)
    return {"messages":tool_message}

def router(state: State) -> Literal["tool_node", "call_llm", "__end__"]:
    """
    Routes the flow based on whether the last LLM message contains tool calls.
    Args:
        state (State): The current state containing messages.
    Returns:
        Literal["tool_node", "call_llm", "__end__"]: The next node to route to.
    """
    print("router")

    # Get the last LLM response
    llm_response = state["messages"][-1]

    # Routing logic
    if getattr(llm_response, "tool_calls"):
        return "tool_node"
    if isinstance(llm_response, AIMessage) and (not llm_response.content or llm_response.content.strip().lower() == ""):
        return "call_llm"
    return "__end__"



def build_graph() -> CompiledStateGraph[State, None, State, State]:
    """
    Builds and compiles the state graph for the application.
    Returns:
        CompiledStateGraph[State, None, State, State]: The compiled state graph.
    """
    # Graph builder
    builder = StateGraph(state_schema=State)

    # Adding nodes
    builder.add_node("call_llm", call_llm)
    builder.add_node("tool_node", tool_node)

    # Adding edges
    builder.add_edge(START, "call_llm")
    builder.add_conditional_edges("call_llm", router)
    builder.add_edge("tool_node", "call_llm")

    return builder.compile(checkpointer=InMemorySaver())
