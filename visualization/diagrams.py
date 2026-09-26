"""
Renders simple linear process/flow diagrams (step-by-step boxes with arrows),
useful for summarizing a process the research described.
"""
from __future__ import annotations

import os
from typing import List

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from config.settings import settings


def flow_diagram(steps: List[str], title: str = "", filename: str = "flow_diagram.png") -> str:
    fig, ax = plt.subplots(figsize=(max(6, 2.2 * len(steps)), 2.5))
    ax.axis("off")
    n = len(steps)
    box_w, gap = 1.0, 0.4
    for i, step in enumerate(steps):
        x = i * (box_w + gap)
        ax.add_patch(plt.Rectangle((x, 0), box_w, 1, fill=True, facecolor="#EFF6FF", edgecolor="#3B82F6"))
        ax.text(x + box_w / 2, 0.5, step, ha="center", va="center", fontsize=9, wrap=True)
        if i < n - 1:
            ax.annotate(
                "", xy=(x + box_w + gap, 0.5), xytext=(x + box_w, 0.5),
                arrowprops=dict(arrowstyle="->", color="#3B82F6"),
            )
    ax.set_xlim(-0.2, n * (box_w + gap))
    ax.set_ylim(-0.3, 1.3)
    if title:
        ax.set_title(title)
    fig.tight_layout()
    os.makedirs(settings.OUTPUT_DIR, exist_ok=True)
    path = os.path.join(settings.OUTPUT_DIR, filename)
    fig.savefig(path, dpi=150)
    plt.close(fig)
    return path
