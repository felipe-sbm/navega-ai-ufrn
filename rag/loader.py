from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader

def load_documents(folder):
    documents = []
    
    for file in Path(folder).rglob("*"):
        if not file.is_file():
            continue

        if file.suffix.lower() == ".pdf":
            loader = PyPDFLoader(str(file))
            docs = loader.load()
            
            for doc in docs:
                if doc.page_content:
                    if isinstance(doc.page_content, bytes):
                        try:
                            doc.page_content = doc.page_content.decode('utf-8')
                        except:
                            doc.page_content = doc.page_content.decode('latin-1')
                    
                    doc.page_content = str(doc.page_content)
                    doc.page_content = doc.page_content.replace('\x00', '')
                
                doc.metadata["arquivo"] = file.name
                doc.metadata["categoria"] = file.parent.name

            documents.extend(docs)

        elif file.suffix.lower() == ".docx":
            loader = Docx2txtLoader(str(file))
            docs = loader.load()

            for doc in docs:
                if doc.page_content:
                    if isinstance(doc.page_content, bytes):
                        try:
                            doc.page_content = doc.page_content.decode('utf-8')
                        except:
                            doc.page_content = doc.page_content.decode('latin-1')
                    
                    doc.page_content = str(doc.page_content)
                    doc.page_content = doc.page_content.replace('\x00', '')
                
                doc.metadata["arquivo"] = file.name
                doc.metadata["categoria"] = file.parent.name

            documents.extend(docs)
            
    return documents