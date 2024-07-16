from typing import Annotated, Sequence, TypedDict

from langchain_core.messages import BaseMessage, ToolMessage

from langgraph.graph.message import add_messages


class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]
    bases: Annotated[Sequence[ToolMessage], add_messages]
    rubricas: Annotated[Sequence[ToolMessage], add_messages]
    login: str