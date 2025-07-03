from .state import ResearchState
from .tools import search_web

from langchain_community.document_loaders import WebBaseLoader
from langchain_core.documents import Document
from typing import List
from .clean_data import clean_text
from langgraph.constants import Send

def get_sources_urls(state: ResearchState) -> ResearchState:
    """
    Searches the web based on the latest user message and stores the resulting sources in the state.

    Args:
        state (ResearchState): The current research state containing the conversation.

    Returns:
        ResearchState: The updated state with a list of sources.
    """
    human_query = state.get('messages')[-1].content
    sources = search_web(human_query)
    state['sources'] = sources
    return state


def continue_read_web_pages(state: ResearchState) -> List[Send]:
    """
    Creates a list of Send instructions to trigger reading of each web page source.

    Args:
        state (ResearchState): The current research state with collected source URLs.

    Returns:
        List[Send]: A list of Send actions with each source URL.
    """
    return [Send("read_web_page", {"url": s[1]}) for s in state['sources']]  # s is a tuple (title, url)

def get_reduced_text(doc: Document) -> str:
    """
    Extracts the main part  of the document's text.

    Args:
        doc (Document): The original document.

    Returns:
        str: The reduced text that is clean.
    """
    full_text = doc.page_content
    half_length = int(len(full_text) * 0.25)
    reducecd_doc = full_text[:half_length]
    return clean_text(reducecd_doc)

def read_web_page(url: str) -> ResearchState:
    """
    Loads and cleans the content from the given URL.

    Args:
        url (str): The URL to load.

    Returns:
        ResearchState: A partial state containing the cleaned content from the web page.
    """
    print(f"🔍 Reading web page: {url}" )
    loader = WebBaseLoader(url['url'])

    try:
        document  = loader.load()
        content = get_reduced_text(document[0])
    except Exception as e:
        content = f"Error loading content from {url}: {e}"

    return {"researched_content": [content]}


