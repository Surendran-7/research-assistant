"""
Tool: search the user's uploaded documents (RAG over data/documents/).
This is the tool definition the agent hands to Groq's function-calling API,
plus the Python function Groq's tool_calls resolve to.
"""
from rag.retriever import DocumentRetriever

_retriever = DocumentRetriever()

TOOL_SCHEMA = {
    "type": "function",
    "function": {
        "name": "search_documents",
        "description": (
            "Search the user's uploaded research documents for passages relevant "
            "to a question. Always try this tool first before web search when the "
            "user references 'the document', 'the file', or 'the paper'."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The question or topic to search for in the documents.",
                }
            },
            "required": ["query"],
        },
    },
}


def search_documents(query: str) -> str:
    results = _retriever.query(query)
    if not results:
        return "No relevant passages found in the uploaded documents."

    formatted = []
    for r in results:
        loc = f"{r.source}" + (f", p.{r.page}" if r.page else "")
        formatted.append(f"[{loc}] (score {r.score:.2f})\n{r.text}")
    return "\n\n---\n\n".join(formatted)
