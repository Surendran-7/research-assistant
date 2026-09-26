"""
Renders a node/relationship graph (e.g. entities and how they relate) using
networkx + matplotlib. Input is a list of (source, relation, target) triples.
"""
from __future__ import annotations

import os
from typing import List, Tuple

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import networkx as nx

from config.settings import settings


def relationship_graph(
    triples: List[Tuple],
    title: str = "",
    filename: str = "graph.png",
) -> str:
    g = nx.DiGraph()
    for item in triples:
        if len(item) >= 3:
            src, relation, dst = item[0], item[1], item[2]
        elif len(item) == 2:
            src, dst = item[0], item[1]
            relation = ""
        else:
            continue
        g.add_edge(str(src), str(dst), label=str(relation))

    fig, ax = plt.subplots(figsize=(7, 6))
    pos = nx.spring_layout(g, seed=42, k=0.9)
    nx.draw_networkx_nodes(g, pos, ax=ax, node_color="#DBEAFE", node_size=1800, edgecolors="#3B82F6")
    nx.draw_networkx_labels(g, pos, ax=ax, font_size=9)
    nx.draw_networkx_edges(g, pos, ax=ax, arrows=True, edge_color="#94A3B8")
    edge_labels = nx.get_edge_attributes(g, "label")
    if any(edge_labels.values()):
        nx.draw_networkx_edge_labels(g, pos, edge_labels=edge_labels, ax=ax, font_size=8)
    ax.axis("off")
    if title:
        ax.set_title(title)
    fig.tight_layout()
    os.makedirs(settings.OUTPUT_DIR, exist_ok=True)
    path = os.path.join(settings.OUTPUT_DIR, filename)
    fig.savefig(path, dpi=150)
    plt.close(fig)
    return path
