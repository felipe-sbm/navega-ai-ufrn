import streamlit as st
from ui.chat import clear_chat_history

def render_sidebar():
    with st.sidebar:
        st.markdown(
            """
            **Assistente Virtual da UFRN**
            
            Tire dúvidas sobre:
            - o IMDtec
            - a PPGCTI
            - Módulo Integrador
            - Processos de pós graduação como material didático e resoluções
            """
        )

        st.markdown("---")

        if st.button("Limpar conversa", use_container_width=True):
            clear_chat_history()
            st.rerun()

        if st.button("Atualizar documentos", use_container_width=True):
            st.session_state.force_rebuild = True
            st.rerun()

        st.markdown("---")
        st.caption("Desenvolvido no IMDtec")