"""
Central configuration for the research assistant.
Everything else in the app imports from here instead of reading os.environ directly.
"""
import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    # --- Groq (LLM inference) ---
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
    GROQ_MODEL: str = os.getenv("GROQ_MODEL", "openai/gpt-oss-120b")

    # --- Embeddings (local, since Groq has no embeddings endpoint) ---
    EMBEDDING_MODEL: str = os.getenv("EMBEDDING_MODEL", "BAAI/bge-small-en-v1.5")

    # --- RAG / vector store ---
    CHROMA_DIR: str = os.getenv("CHROMA_DIR", "data/chroma_db")
    DOCS_DIR: str = os.getenv("DOCS_DIR", "data/documents")
    CHUNK_SIZE: int = int(os.getenv("CHUNK_SIZE", 800))
    CHUNK_OVERLAP: int = int(os.getenv("CHUNK_OVERLAP", 120))
    TOP_K: int = int(os.getenv("TOP_K", 6))

    # --- Output ---
    OUTPUT_DIR: str = os.getenv("OUTPUT_DIR", "data/outputs")

    @classmethod
    def validate(cls) -> None:
        if not cls.GROQ_API_KEY or cls.GROQ_API_KEY == "your_groq_api_key_here":
            raise ValueError(
                "GROQ_API_KEY is missing. Add your key to the .env file "
                "(get one free at https://console.groq.com/keys)."
            )


settings = Settings()
