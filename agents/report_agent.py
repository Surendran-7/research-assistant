"""
Combines the research agent's answer and the visualization agent's chart (if any)
into a single markdown report file the user can keep.
"""
from __future__ import annotations

import os
from datetime import datetime

from config.settings import settings
from agents.research_agent import ResearchResult
from agents.visualization_agent import VisualizationResult


class ReportAgent:
    def build(
        self,
        question: str,
        research: ResearchResult,
        visualization: VisualizationResult,
        filename: str = "report.md",
    ) -> str:
        os.makedirs(settings.OUTPUT_DIR, exist_ok=True)
        path = os.path.join(settings.OUTPUT_DIR, filename)

        lines = [
            f"# Research report",
            f"*Generated {datetime.now().strftime('%Y-%m-%d %H:%M')}*",
            "",
            f"## Question",
            question,
            "",
            f"## Findings",
            research.answer,
        ]

        if visualization.created and visualization.path:
            rel_path = os.path.relpath(visualization.path, settings.OUTPUT_DIR)
            lines += ["", "## Visualization", f"![chart]({rel_path})"]

        if research.tool_calls_made:
            lines += ["", "## Tools used", *[f"- `{c}`" for c in research.tool_calls_made]]

        with open(path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))

        return path
