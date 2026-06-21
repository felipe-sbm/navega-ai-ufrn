from pathlib import Path
from langchain_community.document_loaders import TextLoader

def load_documents(folder):
    documents = []
    
    for file in Path(folder).rglob("*"):
        if not file.is_file():
            continue

        elif file.suffix.lower() in (".md", ".txt", ".markdown"):
            loader = TextLoader(str(file), encoding="utf-8")
            docs = loader.load()
            
            for doc in docs:
                if doc.page_content:
                    doc.page_content = str(doc.page_content)
                    doc.page_content = doc.page_content.replace('\x00', '')
                
                doc.metadata["arquivo"] = file.name
                doc.metadata["categoria"] = file.parent.name

            documents.extend(docs)

    return documents