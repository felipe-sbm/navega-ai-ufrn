from pathlib import Path
from dotenv import load_dotenv
import os

load_dotenv()

# Modo offline para Hugging Face
# No deploy, preferimos permitir download online (melhora a inicialização).
os.environ.pop("TRANSFORMERS_OFFLINE", None)
os.environ.pop("HF_HUB_OFFLINE", None)
os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"

BASE_DIR = Path(__file__).parent.parent

DOCS_DIR = BASE_DIR / "data" / "docs"
CHROMA_DIR = BASE_DIR / "data" / "chroma"
COLLECTION_NAME = "navega_ai_ufrn"
HF_TOKEN = os.getenv("HF_TOKEN", None)
LLM_MODEL = "Qwen/Qwen2.5-1.5B-Instruct"

AVAILABLE_MODELS = {
    "Llama 3.3 70B": {
        "model_id": "llama-3.3-70b-versatile",
        "temperature": 0.2,
        "description": "Modelo principal da Meta hospedado pela Groq. Melhor qualidade."
    },

    "Llama 3.1 8B": {
        "model_id": "llama-3.1-8b-instant",
        "temperature": 0.2,
        "description": "Modelo menor e extremamente rápido."
    },
}

TOP_K = 8
FETCH_K = 10

CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200

EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"