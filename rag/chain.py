from transformers import AutoTokenizer, pipeline
from langchain_huggingface import HuggingFacePipeline
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableParallel
from config.settings import AVAILABLE_MODELS, TOP_K, FETCH_K
from rag.prompt import SYSTEM_PROMPT


def get_model_config(model_key):
    if model_key in AVAILABLE_MODELS:
        return AVAILABLE_MODELS[model_key]
    return list(AVAILABLE_MODELS.values())[0]


def create_chain(vector_store, model_key=None, debug_retriever: bool = False):
    model_config = get_model_config(model_key)
    model_id = model_config["model_id"]
    max_tokens = model_config["max_tokens"]
    temperature = model_config["temperature"]

    tokenizer = AutoTokenizer.from_pretrained(model_id)

    # Evita carregamento via pipeline que dá fragementos.
    from transformers import AutoModelForCausalLM

    model = AutoModelForCausalLM.from_pretrained(
        model_id,
        device_map="auto",
        torch_dtype="auto",
    )

    pipe = pipeline(
        "text-generation",
        model=model,
        tokenizer=tokenizer,
        max_new_tokens=max_tokens,
        temperature=temperature,
        repetition_penalty=1.1,
        do_sample=True,
        return_full_text=False,
    )


    llm = HuggingFacePipeline(pipeline=pipe)
    retriever = vector_store.as_retriever(
        search_type="similarity",
        search_kwargs={
            "k": TOP_K,
        },
    )

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", SYSTEM_PROMPT),
            (
                "human",
                "Contexto (trechos recuperados):\\n{context}\\n\\n"
                "Pergunta: {question}\\n\\n"
                "Instruções estritas:\\n"
                "1) Use **somente** informações que apareçam explicitamente no contexto.\\n"
                "2) Para perguntas de **carga horária / créditos / horas mínimas**, devolva uma **tabela** com valores.\\n"
                "3) Se a resposta não estiver no contexto, diga exatamente: 'Não encontrei a resposta nos documentos disponíveis.'\\n"
                "4) Não invente números nem interpretações.\\n",
            ),
        ]
    )

    def maybe_format_docs(docs):
        if debug_retriever:
            try:
                print("\n===== DOCUMENTOS RECUPERADOS =====")
                for i, doc in enumerate(docs, 1):
                    print(f"\nDOC {i}")
                    print("ARQUIVO:", doc.metadata.get("arquivo"))
                    print("CATEGORIA:", doc.metadata.get("categoria"))
                    print("PAGE:", doc.metadata.get("page"))

                    snippet = (doc.page_content or "").strip().replace("\n", " ")
                    snippet = snippet[:500] + ("..." if len(snippet) > 500 else "")
                    print("SNIPPET:", snippet)
            except Exception as e:
                print(f"[DEBUG retriever] falha ao logar docs: {e}")

        return format_docs(docs)

    chain = (
        RunnableParallel(
            {
                "context": retriever | maybe_format_docs,
                "question": RunnablePassthrough(),
            }
        )
        | prompt
        | llm
        | StrOutputParser()
    )

    return chain


def format_docs(docs):
    formatted = []
    for i, doc in enumerate(docs, 1):
        source = doc.metadata.get("arquivo", "Desconhecido")
        category = doc.metadata.get("categoria", "Geral")
        formatted.append(
            f"[Documento {i} - Fonte: {source} (Categoria: {category})]\\n"
            f"{doc.page_content}\\n"
        )
    return "\\n\\n".join(formatted)

