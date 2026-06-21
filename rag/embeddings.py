from langchain_huggingface import HuggingFaceEmbeddings
from config.settings import EMBEDDING_MODEL


def load_embeddings():
    return HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL,
        model_kwargs={
            "device": "cpu",
        },
        encode_kwargs={
            "normalize_embeddings": True
        }
    )
