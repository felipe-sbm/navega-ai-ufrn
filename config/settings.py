# Achei que poderia usar o Ollama, mas devemos usar somente o hugging faces

from pathlib import Path

BASE_DIR = Path(__file__).parent.parent

PDF_DIR = BASE_DIR / "data" / "pdfs"
CHROMA_DIR = BASE_DIR / "data" / "chroma"

COLLECTION_NAME = "navega_ai_ufrn"

LLM_MODEL = "Qwen/Qwen2.5-1.5B-Instruct"

EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200
TOP_K = 4