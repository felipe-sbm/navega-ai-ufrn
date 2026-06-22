import streamlit as st
from config.settings import DOCS_DIR, AVAILABLE_MODELS
from rag.loader import load_documents
from rag.splitter import split_documents
from rag.embeddings import load_embeddings
from rag.vector_store import create_vector_store, get_existing_vector_store
from rag.chain import create_chain
from ui.sidebar import render_sidebar
from ui.chat import init_chat_history, display_chat_history, add_message
import time

st.set_page_config(
    page_title="Navega Aí!",
    page_icon="🚢",
    layout="centered"
)

init_chat_history()
render_sidebar()

if "debug_retriever" not in st.session_state:
    st.session_state.debug_retriever = False

if "selected_model" not in st.session_state:
    st.session_state.selected_model = list(AVAILABLE_MODELS.keys())[0]

current_model = st.session_state.selected_model
model_changed = st.session_state.pop("model_changed", False)

if "vector_store" not in st.session_state or st.session_state.get("force_rebuild"):
    with st.spinner("Carregando documentos e criando vector store..."):
        embeddings = load_embeddings()
        vector_store = get_existing_vector_store(embeddings)

        if vector_store is None or st.session_state.get("force_rebuild"):
            documents = load_documents(DOCS_DIR)
            chunks = split_documents(documents)
            vector_store = create_vector_store(
                chunks,
                embeddings,
                force_rebuild=st.session_state.get("force_rebuild", False)
            )

        st.session_state.vector_store = vector_store
        st.session_state.vector_store_ready = True
        st.session_state.force_rebuild = False

if "chain" not in st.session_state or model_changed or "chain_model" not in st.session_state or st.session_state.chain_model != current_model:
    model_name_display = current_model.split(" (")[0]
    with st.spinner(
        f"Carregando modelo **{model_name_display}**... "
        "Isso pode levar alguns minutos na primeira execução de cada modelo."
    ):
        
        if "chain" in st.session_state:
            del st.session_state.chain
            import gc
            gc.collect()

        chain = create_chain(
            st.session_state.vector_store,
            model_key=current_model,
            debug_retriever=st.session_state.get("debug_retriever", False),
        )
        st.session_state.chain = chain
        st.session_state.chain_ready = True
        st.session_state.chain_model = current_model

st.title("🚢 Navega Aí!")

display_chat_history()
question = st.chat_input("Digite sua pergunta sobre a UFRN...")

if question:
    add_message("user", question)
    with st.chat_message("assistant"):
        with st.spinner("Consultando documentos e gerando resposta..."):
            try:
                start = time.time()
                response = st.session_state.chain.invoke(question)
                elapsed = time.time() - start
                print(f"Tempo da consulta: {elapsed:.2f}s")
                st.markdown(response)
                add_message("assistant", response)
            except Exception as e:
                error_msg = f" **Erro ao gerar resposta:** {str(e)}"
                st.error(error_msg)
                add_message("assistant", error_msg)

    st.rerun()