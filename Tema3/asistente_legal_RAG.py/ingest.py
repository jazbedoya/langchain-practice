"""
Script de ingesta para el Asistente Legal RAG.

Carga los PDFs de la carpeta ./documentos, los divide en chunks y
construye la base vectorial Chroma en ./chroma_db usando el mismo
modelo de embeddings que la app (config.EMBEDDING_MODEL).

Uso:
    1. Copia tu(s) PDF del contrato dentro de la carpeta ./documentos
    2. Ejecuta:  uv run python ingest.py
"""

import os

from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_community.vectorstores import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

from config import CHROMA_DB_PATH, EMBEDDING_MODEL

load_dotenv()

DOCS_DIR = "./documentos"


def main():
    if not os.path.isdir(DOCS_DIR):
        os.makedirs(DOCS_DIR)
        print(f"Se creó la carpeta '{DOCS_DIR}'. Copia ahí tus PDFs y vuelve a ejecutar.")
        return

    # 1. Cargar PDFs
    loader = PyPDFDirectoryLoader(DOCS_DIR)
    documentos = loader.load()
    print(f"Se cargaron {len(documentos)} páginas desde '{DOCS_DIR}'")

    if not documentos:
        print("No se encontraron PDFs. Copia tus archivos en ./documentos y reintenta.")
        return

    # 2. Dividir en chunks
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
    )
    docs_split = text_splitter.split_documents(documentos)
    print(f"Se crearon {len(docs_split)} chunks de texto")

    # 3. Embeddings + base vectorial persistente
    vectorstore = Chroma.from_documents(
        docs_split,
        embedding=GoogleGenerativeAIEmbeddings(model=EMBEDDING_MODEL),
        persist_directory=CHROMA_DB_PATH,
    )
    print(f"Base vectorial creada en '{CHROMA_DB_PATH}' con {len(docs_split)} vectores.")


if __name__ == "__main__":
    main()
