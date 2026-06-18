from transformers import AutoTokenizer, pipeline
from langchain_huggingface import HuggingFacePipeline
from langchain_core.prompts import ChatPromptTemplate
from config.settings import LLM_MODEL, TOP_K
from rag.prompt import SYSTEM_PROMPT

def create_chain(vector_store):
    tokenizer = AutoTokenizer.from_pretrained(LLM_MODEL)
    pipe = pipeline(
        "text-generation",
        model=LLM_MODEL,
        tokenizer=tokenizer,
        max_new_tokens=400,
        temperature=0.2,
        return_full_text=False
    )

    llm = HuggingFacePipeline(pipeline=pipe)
    retriever = vector_store.as_retriever(search_kwargs={"k": TOP_K})
    prompt = ChatPromptTemplate.from_template(
        """
        Sistema:
        {system}

        Contexto:
        {context}

        Pergunta:
        {question}
        """
    )

    return (retriever, prompt, llm)