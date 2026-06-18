from langchain_chroma import Chroma
from config.settings import COLLECTION_NAME, CHROMA_DIR

def create_vector_store(documents, embeddings):
    return Chroma.from_documents(
        documents=documents,
        embedding=embeddings,
        collection_name=COLLECTION_NAME,
        persist_directory=str(CHROMA_DIR)
    )