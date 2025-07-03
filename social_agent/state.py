import operator
from typing import Optional, List, TypedDict, Annotated
from langgraph.graph import MessagesState
from research_agent.state import Sources

class SocialMediaState(MessagesState):
    tone: str
    posts: str

    image_instruction: Optional[str]
    include_image: bool
    image_url: Optional[str]

    feedback: Optional[str]
    approved: Optional[bool]

    researched_content: Annotated[list[str], operator.add]
    sources: List[Sources]


class ShouldResearch(TypedDict):
    should_research: bool


