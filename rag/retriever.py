"""
Chunks loaded documents, stores them (with embeddings) in a persistent Chroma
collection, and answers similarity-search queries for the research agent.
"""
from __future__ import annotations

import hashlib
from dataclasses import dataclass
from typing import List

import chromadb

from config.settings import settings
from rag.embeddings import embed_texts, embed_query
from rag.loader import LoadedPage, load_directory


@dataclass
class Chunk:
    text: str
    source: str
    page: int | None


@dataclass
class RetrievedChunk:
    text: str
    source: str
    page: int | None
    score: float


def _chunk_text(text: str, size: int, overlap: int) -> List[str]:
    words = text.split()
    if not words:
        return []
    chunks, start = [], 0
    step = max(size - overlap, 1)
    while start < len(words):
        chunk_words = words[start : start + size]
        chunks.append(" ".join(chunk_words))
        start += step
    return chunks


def chunk_pages(pages: List[LoadedPage]) -> List[Chunk]:
    chunks: List[Chunk] = []
    for page in pages:
        for piece in _chunk_text(page.text, settings.CHUNK_SIZE, settings.CHUNK_OVERLAP):
            chunks.append(Chunk(text=piece, source=page.source, page=page.page))
    return chunks


class DocumentRetriever:
    """Thin wrapper around a persistent Chroma collection."""

    def __init__(self, collection_name: str = "research_documents"):
        self.client = chromadb.PersistentClient(path=settings.CHROMA_DIR)
        self.collection = self.client.get_or_create_collection(collection_name)

    def ingest_directory(self, directory: str = settings.DOCS_DIR) -> int:
        pages = load_directory(directory)
        chunks = chunk_pages(pages)
        if chunks:
            self.add_chunks(chunks)
        return len(chunks)

    def add_chunks(self, chunks: List[Chunk]) -> None:
        texts = [c.text for c in chunks]
        embeddings = embed_texts(texts)
        ids = [
            hashlib.sha1(f"{c.source}-{c.page}-{i}-{c.text[:50]}".encode()).hexdigest()
            for i, c in enumerate(chunks)
        ]
        metadatas = [{"source": c.source, "page": c.page or -1} for c in chunks]
        self.collection.upsert(ids=ids, documents=texts, embeddings=embeddings, metadatas=metadatas)

    def query(self, question: str, top_k: int = settings.TOP_K) -> List[RetrievedChunk]:
        if self.collection.count() == 0:
            return []
        result = self.collection.query(
            query_embeddings=[embed_query(question)],
            n_results=min(top_k, self.collection.count()),
        )
        out: List[RetrievedChunk] = []
        docs = result.get("documents", [[]])[0]
        metas = result.get("metadatas", [[]])[0]
        dists = result.get("distances", [[]])[0]
        for doc, meta, dist in zip(docs, metas, dists):
            out.append(
                RetrievedChunk(
                    text=doc,
                    source=meta.get("source", "unknown"),
                    page=None if meta.get("page", -1) == -1 else meta.get("page"),
                    score=1 - dist,  # cosine distance -> similarity
                )
            )
        return out
