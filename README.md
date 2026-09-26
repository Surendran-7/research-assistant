# Research Assistant

A multi-agent research assistant: retrieves from your own documents (RAG),
supplements with live web + Wikipedia search when needed, optionally
visualizes findings, and writes a markdown report. Powered by Groq for
fast LLM inference.

## Setup

```bash
pip install -e .
# or: pip install groq chromadb sentence-transformers pypdf python-docx \
#     python-dotenv duckduckgo-search wikipedia matplotlib networkx rich
```

Add your key to `.env` (get one free at https://console.groq.com/keys):

```
GROQ_API_KEY=gsk_...
```

Drop PDFs/DOCX/TXT/MD files into `data/documents/`.

## Usage

### Web Frontend (Streamlit)
```bash
streamlit run web_app.py
```
*Allows uploading documents directly in the UI, automatic vector store indexing, asking questions, displaying charts, and downloading research reports.*

### Command Line Interface (CLI)
```bash
python app.py ingest                 # index your documents into the vector store
python app.py ask "your question"    # research, visualize, and generate a report
```

Output charts and the final `report.md` land in `data/outputs/`.

## How it works

1. **rag/loader.py** — extracts text from PDF/DOCX/TXT files.
2. **rag/embeddings.py** — encodes chunks locally with `sentence-transformers`
   (Groq doesn't serve an embeddings endpoint, so this runs offline/free).
3. **rag/retriever.py** — chunks text, stores it in a persistent Chroma
   collection, and does similarity search at query time.
4. **agents/research_agent.py** — a Groq tool-calling loop. The model decides
   when to call `search_documents`, `web_search`, or `wikipedia_search`, and
   produces a cited answer.
5. **agents/visualization_agent.py** — asks Groq whether the answer contains
   chartable data, then renders a bar/line/pie chart or relationship graph.
6. **agents/report_agent.py** — compiles the answer + chart into `report.md`.

## Extending

- Swap `EMBEDDING_MODEL` in `.env` for a different `sentence-transformers` model.
- Add a new tool by writing a `TOOL_SCHEMA` + function in `tools/`, then
  registering it in `agents/research_agent.py`'s `TOOLS` / `TOOL_FUNCTIONS`.
- Swap the CLI in `app.py` for a Streamlit/FastAPI front end — the agents are
  plain Python classes, so nothing else needs to change.
