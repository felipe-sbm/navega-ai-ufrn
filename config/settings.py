from pathlib import Path

BASE_DIR = Path(__file__).parent.parent

PDF_DIR = BASE_DIR / "data/pdfs"
CHROMA_DIR = BASE_DIR / "data/chroma"

OLLAMA_MODEL = "gemma3:4b"
EMBEDDING_MODEL = "nomic-embed-text"

TOP_K = 4