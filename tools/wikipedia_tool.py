"""
Tool: Wikipedia lookup, useful for background/definitional context on a topic
before or alongside document-grounded research.
"""
import wikipedia

TOOL_SCHEMA = {
    "type": "function",
    "function": {
        "name": "wikipedia_search",
        "description": (
            "Look up background or definitional information on a topic from Wikipedia. "
            "Good for grounding terms, historical context, or general concepts."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "topic": {"type": "string", "description": "The topic to look up."}
            },
            "required": ["topic"],
        },
    },
}


def wikipedia_search(topic: str) -> str:
    try:
        results = wikipedia.search(topic, results=3)
        if not results:
            return "No Wikipedia article found."
        page = wikipedia.page(results[0], auto_suggest=False)
        summary = wikipedia.summary(results[0], sentences=6, auto_suggest=False)
        return f"[{page.title}] {page.url}\n{summary}"
    except wikipedia.DisambiguationError as e:
        return f"Topic is ambiguous. Options: {', '.join(e.options[:5])}"
    except Exception as e:
        return f"Wikipedia lookup failed: {e}"
