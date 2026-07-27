"""
Tavily Real-Time Web Search Tool Integration.
Provides search functionality and OpenAI/Groq compatible tool schemas.
"""
import logging
from typing import Any, Dict, List

from app.core.config import settings

logger = logging.getLogger(__name__)

# Lazy Tavily client initialization
_tavily_client = None


def get_tavily_client():
    global _tavily_client
    if _tavily_client is None:
        if not settings.tavily_api_key:
            return None
        try:
            from tavily import TavilyClient
            _tavily_client = TavilyClient(api_key=settings.tavily_api_key)
        except Exception as e:
            logger.error(f"Failed to initialize TavilyClient: {e}")
            return None
    return _tavily_client


def search_trending_keywords(query: str) -> str:
    """
    Search Tavily for real-time trending keywords, search topics, and social buzz related to the query.
    """
    client = get_tavily_client()
    if not client:
        return "Tavily API key not configured or unavailable."

    try:
        response = client.search(
            query=f"trending search keywords topics market trends {query}",
            search_depth="basic",
            max_results=5
        )
        results = response.get("results", [])
        snippets = []
        for r in results:
            snippets.append(f"Title: {r.get('title')}\nSnippet: {r.get('content')}\nURL: {r.get('url')}")
        return "\n\n".join(snippets) if snippets else "No trending keyword results found."
    except Exception as e:
        logger.error(f"Tavily trending keyword search failed for query '{query}': {e}")
        return f"Error executing search: {e}"


def search_competitors(query: str) -> str:
    """
    Search Tavily for market competitors, positioning, and alternative products related to the query.
    """
    client = get_tavily_client()
    if not client:
        return "Tavily API key not configured or unavailable."

    try:
        response = client.search(
            query=f"top competitors market alternatives positioning market share {query}",
            search_depth="basic",
            max_results=5
        )
        results = response.get("results", [])
        snippets = []
        for r in results:
            snippets.append(f"Title: {r.get('title')}\nSnippet: {r.get('content')}\nURL: {r.get('url')}")
        return "\n\n".join(snippets) if snippets else "No competitor results found."
    except Exception as e:
        logger.error(f"Tavily competitor search failed for query '{query}': {e}")
        return f"Error executing search: {e}"


# Groq / OpenAI compatible tool definitions
TAVILY_TOOLS_SCHEMA: List[Dict[str, Any]] = [
    {
        "type": "function",
        "function": {
            "name": "search_trending_keywords",
            "description": "Search real-time web trends, emerging keywords, and industry news for a product or domain.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Search query for discovering trending keywords and market buzz."
                    }
                },
                "required": ["query"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "search_competitors",
            "description": "Search real-time web for market competitors, competing brands, and product positioning.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Search query for finding competitors and positioning."
                    }
                },
                "required": ["query"]
            }
        }
    }
]

# Dispatch map from function name to python callable
TOOL_DISPATCH_MAP = {
    "search_trending_keywords": search_trending_keywords,
    "search_competitors": search_competitors,
}
