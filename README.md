# 🔬 Multi-Agent AI Research Assistant

A multi-agent research automation tool that combines **Retrieval-Augmented Generation (RAG)**, **live web search**, and **automatic data visualization** into a single pipeline. Upload documents, ask a research question, and get back a structured summary, sourced findings, and auto-generated charts — all through a simple Streamlit interface.

---

## ✨ Features

- **Document ingestion (RAG):** Upload PDF, DOCX, TXT, or MD files. Documents are chunked, embedded, and stored in a vector database for retrieval.
- **Live web search:** Agents can pull in up-to-date information from the web to supplement document-based knowledge.
- **Multi-agent workflow:** Separate agents handle research/retrieval, validation & visualization, and final synthesis — rather than relying on a single prompt to do everything.
- **Automatic data visualization:** The system detects when a chart would help (e.g. financial metrics) and generates one automatically.
- **Structured + narrative outputs:** Produces both a sectioned summary table (with source page references) and a polished narrative summary.
- **Simple web UI:** Built with Streamlit — no command-line usage required to run a research query.

---

## 🖼️ Demo

> _Add a screenshot or GIF of the app here, e.g._
> `![App Screenshot](docs/screenshot.png)`

Example: uploading a company's annual report and asking the assistant to "summarize" produces an executive summary table with page citations, a bar chart of key financial metrics, and a narrative summary — in under a minute.

---

## 🏗️ Architecture

```
research-assistant/
├── agents/            # Agent definitions (research, validation, synthesis, etc.)
├── config/            # Configuration files
├── data/              # Uploaded documents & vector store (gitignored)
├── prompts/           # Prompt templates used by agents
├── rag/               # Retrieval-Augmented Generation pipeline
├── tools/             # Tools available to agents (search, file parsing, etc.)
├── visualization/      # Chart, diagram, and graph generation logic
├── app.py             # Core application logic
├── web_app.py         # Streamlit web interface entry point
├── pyproject.toml     # Project dependencies & metadata
└── README.md
```

**Workflow:**
1. **Ingestion** — Uploaded documents are parsed, chunked, and embedded into a vector store.
2. **Research** — Given a query, the agent retrieves relevant document chunks and/or performs live web search.
3. **Validation & Visualization** — Results are checked, and relevant charts are generated automatically.
4. **Synthesis** — A final structured summary and narrative report are produced.

---

## 🚀 Getting Started

### Prerequisites
- Python 3.10+
- An API key for your LLM provider (e.g. OpenAI, Anthropic) — set in a `.env` file

### Installation

```bash
git clone https://github.com/Surendran-7/research-assistant.git
cd research-assistant

python -m venv .venv
.venv\Scripts\activate        # on Windows
# source .venv/bin/activate   # on macOS/Linux

pip install -r requirements.txt
# or, if using pyproject.toml:
pip install .
```

### Configuration

Create a `.env` file in the project root with your API key(s):

```
OPENAI_API_KEY=your_key_here
# or
ANTHROPIC_API_KEY=your_key_here
```

### Running the app

```bash
streamlit run web_app.py
```

Then open the local URL shown in your terminal (typically `http://localhost:8501`).

---

## 🧰 Tech Stack

- **Python** — core application logic
- **Streamlit** — web interface
- **Vector database** (e.g. ChromaDB) — document embeddings for RAG
- **LLM API** — reasoning, synthesis, and summarization
- **Web search integration** — live information retrieval

---

## 📌 Roadmap / Ideas

- [ ] Support for additional file types
- [ ] Export reports as PDF/Word
- [ ] Multi-document comparison mode
- [ ] Deployment guide (Streamlit Cloud / Docker)

---

## 📄 License

Specify your license here (e.g. MIT).

---

## 🙋 About

Built as a project exploring agentic RAG systems — orchestrating multiple AI agents across distinct stages of a research workflow (ingestion, retrieval, reasoning, and presentation) instead of relying on a single prompt.
