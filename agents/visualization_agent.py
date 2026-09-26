"""
Looks at a research answer and, if it contains comparable data, decides on and
renders an appropriate visualization (bar/line/pie chart, relationship graph, or flow diagram).
"""
from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Optional

from groq import Groq

from config.settings import settings
from prompts.visualization_prompt import VISUALIZATION_PLANNER_PROMPT
from visualization.charts import bar_chart, line_chart, pie_chart
from visualization.graph import relationship_graph
from visualization.diagrams import flow_diagram


@dataclass
class VisualizationResult:
    created: bool
    path: Optional[str] = None
    reason: str = ""
    chart_type: Optional[str] = None


class VisualizationAgent:
    def __init__(self, model: str = settings.GROQ_MODEL):
        self.client = Groq(api_key=settings.GROQ_API_KEY)
        self.model = model

    def _plan(self, research_answer: str, question: str = "") -> dict:
        prompt = VISUALIZATION_PLANNER_PROMPT.format(question=question, research_answer=research_answer)
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0,
        )
        raw = response.choices[0].message.content.strip()
        raw = raw.removeprefix("```json").removeprefix("```").removesuffix("```").strip()
        try:
            return json.loads(raw)
        except json.JSONDecodeError:
            return {"should_visualize": False, "reason": "planner returned invalid JSON"}

    def run(self, research_answer: str, question: str = "") -> VisualizationResult:
        plan = self._plan(research_answer, question)
        if not plan.get("should_visualize"):
            return VisualizationResult(created=False, reason=plan.get("reason", "no visualizable data"))

        chart_type = plan.get("chart_type")
        title = plan.get("title", "Research findings")
        data = plan.get("data", {})

        try:
            if chart_type == "bar":
                path = bar_chart(data.get("labels_or_nodes", []), data.get("values_or_edges", []), title)
            elif chart_type == "line":
                path = line_chart(data.get("labels_or_nodes", []), data.get("values_or_edges", []), title)
            elif chart_type == "pie":
                path = pie_chart(data.get("labels_or_nodes", []), data.get("values_or_edges", []), title)
            elif chart_type == "graph":
                raw_edges = data.get("values_or_edges", [])
                triples = [tuple(edge) for edge in raw_edges if isinstance(edge, (list, tuple))]
                path = relationship_graph(triples, title)
            elif chart_type == "flow":
                path = flow_diagram(data.get("labels_or_nodes", []), title)
            else:
                return VisualizationResult(created=False, reason="unsupported chart type")
        except Exception as e:
            return VisualizationResult(created=False, reason=f"data didn't fit chart type: {e}")

        return VisualizationResult(
            created=True,
            path=path,
            reason=plan.get("reason", ""),
            chart_type=chart_type
        )
