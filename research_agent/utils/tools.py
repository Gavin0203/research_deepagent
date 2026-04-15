import os
from typing import Annotated, Literal

import dotenv
import httpx
from langchain.tools import InjectedToolArg, tool
from markdownify import markdownify as md
from tavily import TavilyClient

dotenv.load_dotenv()

tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

def get_web_content(url: str, timeout: float = 30.0) -> str:
    """
    Get content from a web page and convert it to markdown format.
    Args:
        url (str): The URL of the web page to fetch.
        timeout (float, optional): The maximum time to wait for a response. Defaults to 30.0 seconds.
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    try:
        response = httpx.get(url, headers=headers,timeout=timeout)
        response.raise_for_status()
        return md(response.text)
    except httpx.RequestError as exc:
        return f"An error occurred while requesting {exc.request.url!r}."
    except Exception as e:
        return f"Error fetching {url}:{str(e)}"
    
@tool(parse_docstring=True)
def tavily_search(
    query: str,
    max_results: Annotated[int, InjectedToolArg]=1,
    topic: Annotated[Literal["general","news","finance"], InjectedToolArg] = "general",
) -> str:
    """Search the web for information for a query.
    
    Uses Tavily to discover relevant urls, then fetches and returns full webpage content as markdown.

    Args:
        query (str): The search query.
        max_results (int, optional): The maximum number of search results to return. Defaults to 1.
        topic (Literal["general","news","finance"], optional): The topic to search within. Defaults to "general".
    
    Returns:
        Formatted serarch results with full webpage content
    """
    search_results = tavily_client.search(query=query, 
                                          max_results=max_results,
                                          topic=topic
                                          )
    result_texts = []
    for result in search_results.get("results",[]):
        url = result.get("url")
        title = result.get("title")
        content = get_web_content(url)
        result_texts.append(f"## {title} \n URL: {url} \n\n {content}")
    return f"Found {len(result_texts)} for {query} : \n\n {result_texts}"
