from langchain_tavily import TavilySearch
from typing import List, Tuple
import os
from dotenv import load_dotenv
load_dotenv()

def search_web(query: str) -> List[Tuple[str, str]]:
    """
    Performs a web search using TavilySearch and returns a list of (title, URL) tuples.

    Args:
        query (str): The search query.

    Returns:
        List[Tuple[str, str]]: A list of search result titles and URLs.
    """
    webtool = TavilySearch(
        max_results=2,
        topic="general",
        tavily_api_key=os.getenv("TAVILY_API_KEY")
    )

    try:
        results = webtool.invoke(query)
        return [(res["title"], res["url"]) for res in results.get("results", [])]
    except Exception as e:
        print(f"Error during web search: {e}")
        return []




