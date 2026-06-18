import streamlit as st
from config.settings import PDF_DIR
from rag.loader import load_documents
from rag.splitter import split_documents
from rag.embeddings import load_embeddings
from rag.vector_store import create_vector_store
from ui.sidebar import render_sidebar

st.set_page_config(page_title="Navega Aí | UFRN")

render_sidebar()

documents = load_documents(PDF_DIR)
chunks = split_documents(documents)
embeddings = load_embeddings()
vector_store = create_vector_store(chunks, embeddings)

st.title("Navega Aí | UFRN")

question = st.chat_input("Me faça uma pergunta! :)")

if question:
    retriever = vector_store.as_retriever()
    docs = retriever.invoke(question)
    context = "\n".join(
        doc.page_content
        for doc in docs
    )

    st.write(context[:2000])