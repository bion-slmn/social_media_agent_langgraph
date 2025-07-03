from .state import ResearchState
from .nodes import get_sources_urls, read_web_page, continue_read_web_pages
from langgraph.graph import StateGraph, START

def create_research_graph() -> StateGraph:
    """
    Creates and compiles a LangGraph workflow for research.

    Steps:
    1. `get_urls`: Searches the web using the latest user query and stores a list of source URLs.
    2. `read_web_page`: Dynamically triggered for each URL to load and clean the content.

    Returns:
        StateGraph: A compiled LangGraph state graph for research.
    """
    workflow = StateGraph(ResearchState)

    # Add nodes
    workflow.add_node('get_urls', get_sources_urls)
    workflow.add_node('read_web_page', read_web_page)

    # Define graph flow
    workflow.add_edge(START, 'get_urls')
    workflow.add_conditional_edges(
        'get_urls',
        continue_read_web_pages,
        ['read_web_page']
    )

    # Compile and return the graph
    return workflow.compile()
