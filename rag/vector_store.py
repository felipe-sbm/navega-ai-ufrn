from langchain_chroma import Chroma
from config.settings import COLLECTION_NAME, CHROMA_DIR
import uuid
import re

def clean_text(text):
    """Remove caracteres problemáticos do texto"""
    if not isinstance(text, str):
        return ""
    text = re.sub(r'[\x00-\x1f\x7f-\x9f]', '', text)
    text = text.replace('\uf02d', '')
    text = text.replace('\u200b', '')
    text = text.replace('\u200c', '')
    text = text.replace('\u200d', '')
    text = text.replace('\ufeff', '')
    return text.strip()

def create_vector_store(documents, embeddings):
    print(f"Total de documentos: {len(documents)}")
    
    textos_validos = []
    metadados_validos = []
    
    for i, doc in enumerate(documents):
        if not hasattr(doc, 'page_content'):
            continue
            
        content = doc.page_content
        
        if content is None:
            continue
            
        if not isinstance(content, str):
            try:
                content = str(content)
            except:
                continue
        
        content = clean_text(content)
        
        if not content:
            continue
            
        textos_validos.append(content)
        metadados_validos.append(doc.metadata)
    
    print(f"Total de documentos válidos: {len(textos_validos)}")
    
    if not textos_validos:
        raise ValueError("Nenhum documento com conteúdo válido.")
    
    vector_store = Chroma(
        collection_name=COLLECTION_NAME,
        embedding_function=embeddings,
        persist_directory=str(CHROMA_DIR)
    )
    
    BATCH_SIZE = 50
    total_adicionados = 0
    
    for i in range(0, len(textos_validos), BATCH_SIZE):
        batch_texts = textos_validos[i:i + BATCH_SIZE]
        batch_metadatas = metadados_validos[i:i + BATCH_SIZE] if metadados_validos else None
        batch_ids = [str(uuid.uuid4()) for _ in range(len(batch_texts))]
        
        try:
            vector_store.add_texts(
                texts=batch_texts,
                metadatas=batch_metadatas,
                ids=batch_ids
            )
            total_adicionados += len(batch_texts)
            
        except Exception as e:
            for j, (text, metadata, doc_id) in enumerate(zip(batch_texts, batch_metadatas, batch_ids)):
                try:
                    text = clean_text(text)
                    if text:
                        vector_store.add_texts(
                            texts=[text],
                            metadatas=[metadata] if metadata else None,
                            ids=[doc_id]
                        )
                        total_adicionados += 1
                except Exception as e2:
                    print(f"Documento {i+j} com falha: {e2}")
    
    print(f"Total de adicionados: {total_adicionados}")
    
    return vector_store