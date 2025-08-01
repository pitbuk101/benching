from src.utils.logs import get_custom_logger
from duckduckgo_search import DDGS
logger = get_custom_logger(__name__)
def search_duckduckgo(query):
    logger.info(f"Searching DuckDuckGo for query: {query}")
    with DDGS() as ddgs:
        results = ddgs.text(query, timelimit="m", safesearch="off", max_results=20)
        if results:
            return [f"{res['title']} - {res['href']}" for res in results]
        else:
            return "No relevant results found."

internet_search_function = [
        {
            "name": "search_duckduckgo",
            "description": "Searches the internet for information.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The query string to search on the internet"
                    }
                },
                "required": ["query"]
            }
        }
    ]