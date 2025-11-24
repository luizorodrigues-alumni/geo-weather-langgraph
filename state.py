from typing import TypedDict, Annotated, Sequence
from langgraph.graph.message import BaseMessage, add_messages

class State(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]