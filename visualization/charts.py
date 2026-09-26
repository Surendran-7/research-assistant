"""
Renders simple charts (bar / line / pie) from data the research or
visualization agent has extracted, and saves them as PNG files.
"""
from __future__ import annotations

import os
from typing import List

import matplotlib

matplotlib.use("Agg")  # headless rendering
import matplotlib.pyplot as plt

from config.settings import settings


def _out_path(name: str) -> str:
    os.makedirs(settings.OUTPUT_DIR, exist_ok=True)
    return os.path.join(settings.OUTPUT_DIR, name)


def _clean_values(values: List) -> List[float]:
    cleaned = []
    for v in values:
        if isinstance(v, (int, float)):
            cleaned.append(float(v))
        elif isinstance(v, str):
            s = v.strip().replace("$", "").replace(",", "").replace("%", "")
            try:
                cleaned.append(float(s))
            except ValueError:
                cleaned.append(0.0)
        else:
            cleaned.append(0.0)
    return cleaned


def bar_chart(labels: List[str], values: List, title: str, filename: str = "bar_chart.png") -> str:
    fig, ax = plt.subplots(figsize=(7, 4.5))
    clean_vals = _clean_values(values)
    ax.bar(labels, clean_vals, color="#3B82F6")
    ax.set_title(title)
    ax.tick_params(axis="x", rotation=30)
    fig.tight_layout()
    path = _out_path(filename)
    fig.savefig(path, dpi=150)
    plt.close(fig)
    return path


def line_chart(labels: List[str], values: List, title: str, filename: str = "line_chart.png") -> str:
    fig, ax = plt.subplots(figsize=(7, 4.5))
    clean_vals = _clean_values(values)
    ax.plot(labels, clean_vals, marker="o", color="#10B981")
    ax.set_title(title)
    ax.tick_params(axis="x", rotation=30)
    fig.tight_layout()
    path = _out_path(filename)
    fig.savefig(path, dpi=150)
    plt.close(fig)
    return path


def pie_chart(labels: List[str], values: List, title: str, filename: str = "pie_chart.png") -> str:
    fig, ax = plt.subplots(figsize=(6, 6))
    clean_vals = _clean_values(values)
    ax.pie(clean_vals, labels=labels, autopct="%1.1f%%")
    ax.set_title(title)
    fig.tight_layout()
    path = _out_path(filename)
    fig.savefig(path, dpi=150)
    plt.close(fig)
    return path
