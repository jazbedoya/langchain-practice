from langchain_community.vectorstores import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
import os
from dotenv import load_dotenv


#Cargar variables de entorno
load_dotenv()



#Cargar PDFS
loader = PyPDFDirectoryLoader("")
documentos= loader.load()

print(f"Se cargaron {len(documentos)} documentos desde el directorio")



#Dividir Documentos
text_splitter= RecursiveCharacterTextSplitter(
    chunk_size= 1000,
    chunk_overlap=200
)    

docs_split = text_splitter.split_documents(documentos)

print(F"Se crearon {len(docs_split)} chunks de texto")


#Embediing y crear base vectorial
vectorstore= Chroma.from_documents(
    docs_split,
    embedding= GoogleGenerativeAIEmbeddings (model="models/embedding-001"),
    persist_directory=""
)



#Consulta
consulta ="¿Cual es el inmuble que forma parte del contrato en la que particpa ...."

resultados= vectorstore.similarity_search(consulta, k=3 )

print("Top 3 docuemntos mas similares a la consulta:")

for i, doc in enumerate(resultados, start=1):
    print(f"Contenido:{doc.page_content}")
    print(f"Metadatos: {doc.metadata}")
