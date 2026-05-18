from langchain_core.runnables import RunnableLambda, RunnableParallel
from langchain_google_genai import ChatGoogleGenerativeAI
import json
from dotenv import load_dotenv

load_dotenv()

#Configuracion del modelo

llm = ChatGoogleGenerativeAI(model = "gemini-2.5-flash", temperature =0)

#Procesador: limpia espacios y limita a 500 caracteres
def preprocess_text(text):
    """LImpia el tesxto eliminando espacio extras y limitando longitud"""
    return text.strip()[:500]


procesador = RunnableLambda(preprocess_text)

#Genrador de resumen 
def generate_summary(text):
    prompt= f"Resume en una sola oracion:{text}"
    response= llm.invoke(prompt)
    return response.content

resumen = RunnableLambda(generate_summary)

#Analisi de sentimientos con formato Json
def analyze_sentiment(text):
    prompt= f"""Analiza el sentimiento del siguinete texto.
    Responde UNICAMENTE en formato JSON valido:
    {{"sentimiento": "positivo|negativo|neutro", "razon": "justificacion breve"}}
     
    Texto: {text}"""

    response = llm.invoke(prompt)
    try:
        return json.loads(response.content)
    except json.JSONDecodeError:
        return {"sentimiento": "neutro", "razon":"Error en el analisi"}
    
sentimiento = RunnableLambda(analyze_sentiment)
    
#Combinacion de resultados 
def merge_results(data):
    #combina los resultados de ambas ramas en un formato unificado
    return {
        "resumen": data["resumen"],
        "sentimiento": data["sentimiento_data"]["sentimiento"],
        "razon":data["sentimiento_data"]["razon"]

    }

juntar_resultado = RunnableLambda(merge_results)



parallel_analysis = RunnableParallel({
    "resumen": resumen,
    "sentimiento_data": sentimiento
})

#Cadena completa
chain = procesador|parallel_analysis|juntar_resultado


reviews_batch=[
    "Buen producto; satisfecho",
    "terrible producto, no recomiendo",
    "esta bien , funcion basica"
]

resultado_batch= chain.batch(reviews_batch)

print(resultado_batch)