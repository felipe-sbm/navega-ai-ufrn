from pathlib import Path
from dotenv import load_dotenv
import os

load_dotenv()

# Modo offline para Hugging Face (modelos já em cache no disco)
os.environ["TRANSFORMERS_OFFLINE"] = "1"
os.environ["HF_HUB_OFFLINE"] = "1"
os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"

BASE_DIR = Path(__file__).parent.parent

PDF_DIR = BASE_DIR / "data" / "pdfs"
CHROMA_DIR = BASE_DIR / "data" / "chroma"

COLLECTION_NAME = "navega_ai_ufrn"

HF_TOKEN = os.getenv("HF_TOKEN", None)

LLM_MODEL = "Qwen/Qwen2.5-1.5B-Instruct"

EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

CHUNK_SIZE = 700
CHUNK_OVERLAP = 100
TOP_K = 6
FETCH_K = 20
