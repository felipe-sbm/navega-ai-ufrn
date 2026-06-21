from transformers import AutoTokenizer, pipeline
from langchain_huggingface import HuggingFacePipeline
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableParallel
from config.settings import LLM_MODEL, TOP_K, FETCH_K
from rag.prompt import SYSTEM_PROMPT

def format_docs(docs):
    formatted = []
    for i, doc in enumerate(docs, 1):
        source = doc.metadata.get("arquivo", "Desconhecido")
        category = doc.metadata.get("categoria", "Geral")
        formatted.append(
            f"[Documento {i} - Fonte: {source} (Categoria: {category})]\n"
            f"{doc.page_content}\n"
        )
    return "\n\n".join(formatted)

def create_chain(vector_store):
    tokenizer = AutoTokenizer.from_pretrained(LLM_MODEL)

    pipe = pipeline(
        "text-generation",
        model=LLM_MODEL,
        tokenizer=tokenizer,
        max_new_tokens=600,
        temperature=0.1,
        top_p=0.9,
        repetition_penalty=1.1,
        do_sample=True,
        return_full_text=False,
        device_map="auto",
    )

    llm = HuggingFacePipeline(pipeline=pipe)
    retriever = vector_store.as_retriever(
        search_type="mmr",
        search_kwargs={
            "k": TOP_K,
            "fetch_k": FETCH_K
        }
    )

    prompt = ChatPromptTemplate.from_messages([
        ("system", SYSTEM_PROMPT),
        ("human",
         "Contexto:\n{context}\n\n"
         "Pergunta: {question}\n\n"
         "Com base APENAS no contexto acima, responda à pergunta de forma clara e objetiva. "
         "Se a informação não estiver no contexto, informe que não encontrou a resposta nos documentos disponíveis."
         )
    ])

    chain = (
        RunnableParallel(
            {
                "context": retriever | format_docs,
                "question": RunnablePassthrough()
            }
        )
        | prompt
        | llm
        | StrOutputParser()
    )

    return chain