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
    "Qwen2.5-1.5B (Padrão, leve)": {
        "model_id": "Qwen/Qwen2.5-1.5B-Instruct",
        "max_tokens": 600,
        "temperature": 0.4,
        "description": "Modelo leve e rápido da família Qwen (1.5B parâmetros)"
    },
    "Phi-3-mini (Mais capaz)": {
        "model_id": "microsoft/Phi-3-mini-4k-instruct",
        "max_tokens": 800,
        "temperature": 0.2,
        "description": "Modelo mais potente da Microsoft (3.8B parâmetros)"
    },
    "SmolLM2-1.7B (Balanceado)": {
        "model_id": "HuggingFaceTB/SmolLM2-1.7B-Instruct",
        "max_tokens": 700,
        "temperature": 0.15,
        "description": "Modelo intermediário da HuggingFace (1.7B parâmetros)"
    },
}

EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

CHUNK_SIZE = 700
CHUNK_OVERLAP = 100
TOP_K = 6
FETCH_K = 20