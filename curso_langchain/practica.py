from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate


# Cargar la API del archivo .env
load_dotenv()

# Crear el cliente de Gemini
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.7)

# Definir plantilla
plantilla = PromptTemplate(
    input_variables=["nombre"],
    template="Saluda al usuario con su nombre.\nNombre del usuario: {nombre}\nAsistente:",
)

# Encadenar prompt + modelo (sintaxis moderna LCEL)
chain = plantilla | llm

# Ejecutar la cadena
resultado = chain.invoke({"nombre": "Jazmin"})

# Imprimir solo el texto de la respuesta
print(resultado.content)





