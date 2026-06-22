from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_core.runnables import RunnableParallel
from config.settings import AVAILABLE_MODELS
from config.settings import TOP_K
from rag.prompt import SYSTEM_PROMPT
import os

def get_model_config(model_key):
    if model_key in AVAILABLE_MODELS:
        return AVAILABLE_MODELS[model_key]

    return list(AVAILABLE_MODELS.values())[0]

def format_docs(docs):
    formatted = []

    for i, doc in enumerate(docs, 1):
        print(f"\nDOC {i}")
        print(doc.metadata)

        print(doc.page_content)

        source = doc.metadata.get("arquivo", "Desconhecido")
        category = doc.metadata.get("categoria", "Geral")

        formatted.append(
            f"[Documento {i} - Fonte: {source} "
            f"(Categoria: {category})]\n"
            f"{doc.page_content}\n"
        )

    return "\n\n".join(formatted)


def create_chain(
    vector_store,
    model_key=None,
    debug_retriever=False,
):

    model_config = get_model_config(model_key)

    llm = ChatGroq(
        model=model_config["model_id"],
        api_key=os.getenv("GROQ_API_KEY"),
        temperature=model_config["temperature"],
    )

    retriever = vector_store.as_retriever(
        search_type="similarity",
        search_kwargs={
            "k": TOP_K,
        },
    )

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", SYSTEM_PROMPT,),
            ("human", "Contexto:\n{context}\n\n" "Pergunta:\n{question}" ),
        ]
    )

    chain = (
        RunnableParallel(
            {"context": retriever | format_docs, "question": RunnablePassthrough()}
        )
        | prompt
        | llm
        | StrOutputParser()
    )

    return chain