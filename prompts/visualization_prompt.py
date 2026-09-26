VISUALIZATION_PLANNER_PROMPT = """You turn research findings into a visualization plan.

User Question: {question}

Research Answer:
---
{research_answer}
---

Decide whether a visualization would help, and if so, which type:
- "bar": for numerical comparisons across categories (e.g. Revenue, Profits, Expenses, Sales by Product/Year, Department counts).
- "line": for trends over time (e.g. Annual/Quarterly growth, historical performance metrics).
- "pie": for proportions, market share, budget allocation, or percentage breakdowns.
- "graph": for entity/relationship networks, company structures, key stakeholder linkages, organization models, or entity interactions (e.g. Company -> Division, Executive -> Role, Company -> Partner).
- "flow": for step-by-step processes or sequence of events.

Guidance:
- If the question or answer relates to company records, company performance, metrics, financial numbers, organizational structure, or structured document insights, ALWAYS create a relevant visualization ("bar", "line", "pie", "graph", or "flow").
- For relationship graphs ("graph"), `labels_or_nodes` can be node names, and `values_or_edges` MUST be a list of 2 or 3-element lists: `[["Source", "Relation", "Target"], ...]` or `[["Source", "Target"], ...]`.
- For bar/line/pie charts, `labels_or_nodes` is a list of strings, and `values_or_edges` is a list of numbers (or numeric strings).
- For flow diagrams ("flow"), `labels_or_nodes` is a list of step descriptions in sequence, and `values_or_edges` can be an empty list `[]`.

Respond ONLY with a JSON object in this exact shape (no markdown fences, no extra prose):
{{
  "should_visualize": true/false,
  "chart_type": "bar" | "line" | "pie" | "graph" | "flow" | null,
  "title": "short chart title",
  "data": {{
    "labels_or_nodes": [...],
    "values_or_edges": [...]
  }},
  "reason": "one sentence on why this visualization fits"
}}
"""
