"""
CLI entry point.

Usage:
    python app.py ingest                  # index everything in data/documents/
    python app.py ask "your question"     # run research -> visualize -> report
"""
from __future__ import annotations

import sys

from rich.console import Console
from rich.markdown import Markdown

from config.settings import settings
from rag.retriever import DocumentRetriever
from agents.research_agent import ResearchAgent
from agents.visualization_agent import VisualizationAgent
from agents.report_agent import ReportAgent

console = Console()


def ingest() -> None:
    retriever = DocumentRetriever()
    n = retriever.ingest_directory(settings.DOCS_DIR)
    console.print(f"[green]Indexed {n} chunks from {settings.DOCS_DIR}[/green]")


def ask(question: str) -> None:
    console.print(f"[bold]Question:[/bold] {question}\n")

    with console.status("[cyan]Researching..."):
        research = ResearchAgent().run(question)
    console.print(Markdown(research.answer))

    with console.status("[cyan]Checking for a useful visualization..."):
        viz = VisualizationAgent().run(research.answer, question)
    if viz.created:
        console.print(f"\n[green]Visualization saved:[/green] {viz.path}")
    else:
        console.print(f"\n[dim]No visualization generated ({viz.reason})[/dim]")

    report_path = ReportAgent().build(question, research, viz)
    console.print(f"[green]Report saved:[/green] {report_path}")


def main() -> None:
    if len(sys.argv) < 2:
        console.print("Usage: python app.py [ingest | ask \"question\"]")
        return

    command = sys.argv[1]
    if command == "ingest":
        ingest()
    elif command == "ask":
        if len(sys.argv) < 3:
            console.print("Usage: python app.py ask \"your question\"")
            return
        ask(" ".join(sys.argv[2:]))
    else:
        console.print(f"Unknown command: {command}")


if __name__ == "__main__":
    main()
