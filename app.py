import streamlit as st
from config.settings import PDF_DIR
from rag.loader import load_documents
from rag.splitter import split_documents
from rag.embeddings import load_embeddings
from rag.vector_store import create_vector_store, get_existing_vector_store
from rag.chain import create_chain
from ui.sidebar import render_sidebar
from ui.chat import init_chat_history, display_chat_history, add_message

st.set_page_config(
    page_title="Navega Aí!",
    page_icon="🚢",
    layout="centered"
)

init_chat_history()
render_sidebar()

if "vector_store" not in st.session_state or st.session_state.get("force_rebuild"):
    with st.spinner("Carregando documentos e criando vector store..."):
        embeddings = load_embeddings()
        vector_store = get_existing_vector_store(embeddings)

        if vector_store is None or st.session_state.get("force_rebuild"):
            documents = load_documents(PDF_DIR)
            chunks = split_documents(documents)
            vector_store = create_vector_store(
                chunks,
                embeddings,
                force_rebuild=st.session_state.get("force_rebuild", False)
            )

        st.session_state.vector_store = vector_store
        st.session_state.vector_store_ready = True
        st.session_state.force_rebuild = False

if "chain" not in st.session_state:
    with st.spinner(
        "Carregando modelo de linguagem (Qwen2.5-1.5B)... "
        "Isso pode levar alguns minutos na primeira execução."
    ):
        chain = create_chain(st.session_state.vector_store)
        st.session_state.chain = chain
        st.session_state.chain_ready = True
        
st.title("Navega Aí!")
st.markdown(
    "Olá, como posso lhe ajudar hoje! 😊"
)

display_chat_history()
question = st.chat_input("Digite sua pergunta sobre a UFRN...")

if question:
    add_message("user", question)
    with st.chat_message("assistant"):
        with st.spinner("Consultando documentos e gerando resposta..."):
            try:
                response = st.session_state.chain.invoke(question)
                st.markdown(response)
                add_message("assistant", response)
            except Exception as e:
                error_msg = f" **Erro ao gerar resposta:** {str(e)}"
                st.error(error_msg)
                add_message("assistant", error_msg)
                
    st.rerun()