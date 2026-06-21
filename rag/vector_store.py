from langchain_chroma import Chroma
from config.settings import COLLECTION_NAME, CHROMA_DIR
import uuid
import re
import shutil

def clean_text(text):
    if not isinstance(text, str):
        return ""
    text = re.sub(r'[\x00-\x1f\x7f-\x9f]', '', text)
    text = text.replace('\uf02d', '')
    text = text.replace('\u200b', '')
    text = text.replace('\u200c', '')
    text = text.replace('\u200d', '')
    text = text.replace('\ufeff', '')
    return text.strip()


def get_existing_vector_store(embeddings):
    chroma_dir = CHROMA_DIR
    chroma_db_file = chroma_dir / "chroma.sqlite3"

    if chroma_db_file.exists():
        print(f"Carregando vector store existente em: {chroma_dir}")
        return Chroma(
            collection_name=COLLECTION_NAME,
            embedding_function=embeddings,
            persist_directory=str(chroma_dir)
        )
    return None


def create_vector_store(documents, embeddings, force_rebuild=False):
    chroma_dir = CHROMA_DIR
    chroma_db_file = chroma_dir / "chroma.sqlite3"

    if not force_rebuild and chroma_db_file.exists():
        print("Vector store existente encontrado. Carregando...")
        return Chroma(
            collection_name=COLLECTION_NAME,
            embedding_function=embeddings,
            persist_directory=str(chroma_dir)
        )

    if force_rebuild and chroma_dir.exists():
        print("Forçando rebuild. Apagando vector store existente...")
        shutil.rmtree(chroma_dir)

    print(f"Total de documentos recebidos: {len(documents)}")

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
        raise ValueError("Nenhum documento com conteúdo válido para indexar.")

    vector_store = Chroma(
        collection_name=COLLECTION_NAME,
        embedding_function=embeddings,
        persist_directory=str(chroma_dir)
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
            print(f"Erro no batch {i}: {e}. Tentando documento por documento...")
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

    print(f"Total adicionado ao vector store: {total_adicionados}")

    return vector_store