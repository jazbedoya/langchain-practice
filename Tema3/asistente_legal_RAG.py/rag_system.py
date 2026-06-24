from langchain_community.vectorstores import Chroma
from langchain_google_genai import (
    ChatGoogleGenerativeAI,
    GoogleGenerativeAIEmbeddings
)
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_classic.retrievers.multi_query import MultiQueryRetriever

import streamlit as st
from dotenv import load_dotenv

from config import *
from prompt import *

# Cargar variables de entorno
load_dotenv()


@st.cache_resource
def initialize_rag_system():

    # =========================
    # Vector Store
    # =========================
    vectorstore = Chroma(
        embedding_function=GoogleGenerativeAIEmbeddings(
            model=EMBEDDING_MODEL
        ),
        persist_directory=CHROMA_DB_PATH
    )

    # =========================
    # Modelo para MultiQuery
    # =========================
    llm_queries = ChatGoogleGenerativeAI(
        model=QUERY_MODEL,
        temperature=0
    )

    # =========================
    # Modelo para generación final
    # =========================
    llm_generation = ChatGoogleGenerativeAI(
        model=GENERATION_MODEL,
        temperature=0.2
    )

    # =========================
    # Retriever Base
    # =========================
    base_retriever = vectorstore.as_retriever(
        search_type=SEARCH_TYPE,
        search_kwargs={
            "k": SEARCH_K,
            "fetch_k": MMR_FETCH_K,
            "lambda_mult": MMR_DIVERSITY_LAMBDA
        }
    )

    # =========================
    # Prompt MultiQuery
    # =========================
    multi_query_prompt = PromptTemplate.from_template(
        MULTI_QUERY_PROMPT
    )

    # =========================
    # MultiQuery Retriever
    # =========================
    mmr_multi_retriever = MultiQueryRetriever.from_llm(
        retriever=base_retriever,
        llm=llm_queries,
        prompt=multi_query_prompt
    )

    # =========================
    # Prompt principal RAG
    # =========================
    rag_prompt = PromptTemplate.from_template(
        RAG_TEMPLATE
    )

    # =========================
    # Formatear documentos
    # =========================
    def format_docs(docs):

        formatted = []

        for i, doc in enumerate(docs, 1):

            header = f"[Fragmento {i}]"

            if doc.metadata:

                if "source" in doc.metadata:

                    source = doc.metadata["source"]

                    source = (
                        source.split("\\")[-1]
                        if "\\" in source
                        else source
                    )

                    header += f" - Fuente: {source}"

                if "page" in doc.metadata:

                    header += (
                        f" - Página: {doc.metadata['page']}"
                    )

            content = doc.page_content.strip()

            formatted.append(
                f"{header}\n{content}"
            )

        return "\n\n".join(formatted)

    # =========================
    # Cadena RAG
    # =========================
    rag_chain = (
        {
            "context": mmr_multi_retriever | format_docs,
            "question": RunnablePassthrough()
        }
        | rag_prompt
        | llm_generation
        | StrOutputParser()
    )

    return rag_chain, mmr_multi_retriever


def query_rag(question):

    try:

        rag_chain, retriever = initialize_rag_system()

        # Respuesta
        response = rag_chain.invoke(question)

        # Documentos recuperados
        docs = retriever.invoke(question)

        docs_info = []

        for i, doc in enumerate(docs[:SEARCH_K], 1):

            source = doc.metadata.get(
                "source",
                "No especificado"
            )

            source = (
                source.split("\\")[-1]
                if "\\" in source
                else source
            )

            content = doc.page_content

            if len(content) > 1000:
                content = content[:1000] + "..."

            pagina = doc.metadata.get("page", "N/A")

            doc_info = {
                "fragmento": i,
                "contenido": content,
                "fuente": source,
                "pagina": pagina
            }

            docs_info.append(doc_info)

        return response, docs_info

    except Exception as e:

        error_message = f"Error al consultar el sistema RAG: {str(e)}"

        return error_message, []
    

def get_retriever_info():
    """Obtiene informacion sobre la configuracion del Retriever"""

    return{
        "tipo": f"{SEARCH_TYPE.upper()}",
        "documentos": SEARCH_K,
        "diversidad": MMR_DIVERSITY_LAMBDA,
        "candidatos":MMR_FETCH_K, 
        "umbral": None
    }