from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader

def load_documents(folder):
    documents = []

    for file in Path(folder).iterdir():
        if file.suffix.lower() == ".pdf":
            loader = PyPDFLoader(str(file))
            documents.extend(loader.load())

        elif file.suffix.lower() == ".docx":
            loader = Docx2txtLoader(str(file))
            documents.extend(loader.load())

    return documents