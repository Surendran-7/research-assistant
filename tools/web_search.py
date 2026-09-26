"""
Tool: general web search, used when the answer isn't in the uploaded documents
or the user asks about something current. Uses DuckDuckGo (no API key needed).
"""
from duckduckgo_search import DDGS

TOOL_SCHEMA = {
    "type": "function",
    "function": {
        "name": "web_search",
        "description": (
            "Search the public web for current or general information not found "
            "in the uploaded documents. Use for facts, news, or topics outside the file."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "The search query."},
                "max_results": {
                    "type": "integer",
                    "description": "How many results to return (default 5).",
                },
            },
            "required": ["query"],
        },
    },
}


def web_search(query: str, max_results: int = 5) -> str:
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=max_results))
    except Exception as e:
        return f"Web search failed: {e}"

    if not results:
        return "No web results found."

    formatted = [
        f"[{r.get('title')}] {r.get('href')}\n{r.get('body')}" for r in results
    ]
    return "\n\n---\n\n".join(formatted)
