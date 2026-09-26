"""
Wraps a local sentence-transformers model so the rest of the app never
touches the embedding library directly. Groq does not serve an embeddings
endpoint, so embeddings are generated locally/offline and are free to run.
"""
from __future__ import annotations

from functools import lru_cache
from typing import List

from sentence_transformers import SentenceTransformer

from config.settings import settings


@lru_cache(maxsize=1)
def _get_model() -> SentenceTransformer:
    return SentenceTransformer(settings.EMBEDDING_MODEL)


def embed_texts(texts: List[str]) -> List[List[float]]:
    model = _get_model()
    vectors = model.encode(texts, normalize_embeddings=True, show_progress_bar=False)
    return vectors.tolist()


def embed_query(text: str) -> List[float]:
    return embed_texts([text])[0]
