import operator
from typing import Annotated, TypedDict
from langgraph.graph import  MessagesState


class Sources(TypedDict):
    title: str
    url: str

class ResearchState(MessagesState):
    researched_content: Annotated[list[str], operator.add]
    sources: list[Sources]