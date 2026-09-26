"""
Loads raw text out of files in data/documents/ (or a single given path).
Supports .pdf, .docx, .txt, .md. Each record keeps enough metadata to cite later.
"""
from __future__ import annotations

import os
from dataclasses import dataclass, field
from typing import List

from pypdf import PdfReader
from docx import Document as DocxDocument


@dataclass
class LoadedPage:
    text: str
    source: str          # file name
    page: int | None = None  # page number if applicable


def _load_pdf(path: str) -> List[LoadedPage]:
    reader = PdfReader(path)
    pages = []
    for i, page in enumerate(reader.pages, start=1):
        text = (page.extract_text() or "").strip()
        if text:
            pages.append(LoadedPage(text=text, source=os.path.basename(path), page=i))
    return pages


def _load_docx(path: str) -> List[LoadedPage]:
    doc = DocxDocument(path)
    text = "\n".join(p.text for p in doc.paragraphs if p.text.strip())
    return [LoadedPage(text=text, source=os.path.basename(path), page=None)] if text else []


def _load_text(path: str) -> List[LoadedPage]:
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        text = f.read().strip()
    return [LoadedPage(text=text, source=os.path.basename(path), page=None)] if text else []


LOADERS = {
    ".pdf": _load_pdf,
    ".docx": _load_docx,
    ".txt": _load_text,
    ".md": _load_text,
}


def load_file(path: str) -> List[LoadedPage]:
    ext = os.path.splitext(path)[1].lower()
    loader = LOADERS.get(ext)
    if not loader:
        raise ValueError(f"Unsupported file type: {ext}")
    return loader(path)


def load_directory(directory: str) -> List[LoadedPage]:
    """Load every supported file in a directory."""
    pages: List[LoadedPage] = []
    if not os.path.isdir(directory):
        return pages
    for name in sorted(os.listdir(directory)):
        path = os.path.join(directory, name)
        ext = os.path.splitext(name)[1].lower()
        if os.path.isfile(path) and ext in LOADERS:
            pages.extend(load_file(path))
    return pages
