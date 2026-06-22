from pathlib import Path
from langchain_community.document_loaders import (TextLoader,PyPDFLoader)

def load_documents(folder):
    documents = []

    for file in Path(folder).rglob("*"):
        if not file.is_file():
            continue

        suffix = file.suffix.lower()

        try:
            if suffix in (".md", ".txt", ".markdown"):
                loader = TextLoader(str(file), encoding="utf-8")
                docs = loader.load()

            elif suffix == ".pdf":
                loader = PyPDFLoader(str(file))
                docs = loader.load()

            else:
                continue

            for doc in docs:
                if doc.page_content:
                    doc.page_content = (str(doc.page_content).replace("\x00", ""))

                doc.metadata["arquivo"] = file.name
                doc.metadata["categoria"] = file.parent.name

            documents.extend(docs)
            print(f"Carregado: {file.name} ({len(docs)} páginas/chunks)")

        except Exception as e:
            print( f"Erro ao carregar {file.name}: {e}")

    print(f"Total de documentos carregados: {len(documents)}")
    return documents