import streamlit as st
from ui.chat import clear_chat_history
from config.settings import AVAILABLE_MODELS


def render_sidebar():
    with st.sidebar:
        st.markdown(
            """
            **Assistente Virtual do IMDtec**
            
            Tire dúvidas sobre:
            - o IMDtec
            - Módulo Integrador
            - Grades Curriculares
            - Processos Burocráticos
            """
        )

        st.markdown("---")

        st.markdown("### Modelo de IA")
        model_keys = list(AVAILABLE_MODELS.keys())
        default_idx = 0  # Qwen é o padrão

        selected_model = st.selectbox(
            "Escolha o modelo:",
            options=model_keys,
            index=default_idx,
            format_func=lambda k: k.split(" (")[0],  # Mostra só o nome (ex: "Qwen2.5-1.5B")
            help="Selecione o modelo de linguagem para responder às perguntas."
        )
        
        st.caption(AVAILABLE_MODELS[selected_model]["description"])

        if "selected_model" not in st.session_state:
            st.session_state.selected_model = selected_model
        elif st.session_state.selected_model != selected_model:
            st.session_state.selected_model = selected_model
            st.session_state.model_changed = True
            st.rerun()

        st.markdown("---")

        if st.button("Limpar conversa", use_container_width=True):
            clear_chat_history()
            st.rerun()

        if st.button("Atualizar documentos", use_container_width=True):
            st.session_state.force_rebuild = True
            st.rerun()

        st.markdown("---")

        st.caption("Desenvolvido no IMDtec")