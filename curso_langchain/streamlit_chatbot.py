import streamlit as st
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

# Configuracion de la pagina
st.set_page_config(page_title="Chatbot Basico", page_icon="🤖")
st.title("🤖 Chatbot Basico con LangChain")
st.markdown(
    "Este es un *ChatBot de ejemplo* construido con **LangChain + Streamlit**. "
    "Escribe tu mensaje abajo para comenzar!"
)

# Sidebar con configuracion 
with st.sidebar:
    st.header("Configuracion")
    
    # Control de temperatura del modelo
    temperature = st.slider("Temperatura", 0.0, 1.0, 0.5, 0.1)
    
    # Selector de modelo
    model_name = st.selectbox("Modelo", ["gemini-2.5-flash"])

    # Personalidad configurable
    personalidad = st.selectbox(
        "Personalidad del asistente",
        [
            "Util y amigable",
            "Profesional y formal", 
            "Casual y relajado",
            "Experto tecnico",
            "Creativo y divertido"
        ]
    )

# Configuracion del modelo
chat_model = ChatGoogleGenerativeAI(model=model_name, temperature=temperature)

# Template dinamico basado en personalidad
system_personalidad = {
    "Util y amigable": "Eres un asistente util y amigable llamado ChatBot Pro. Responde de manera clara y concisa.",
    "Profesional y formal": "Eres un asistente profesional y formal. Proporciona respuestas precisas y bien estructuradas.",
    "Casual y relajado": "Eres un asistente casual y relajado. Habla de forma natural y amigable, como un buen amigo.",
    "Experto tecnico": "Eres un asistente experto tecnico. Proporciona respuestas detalladas con precision tecnica.",
    "Creativo y divertido": "Eres un asistente creativo y divertido. Usa analogias, ejemplos creativos y manten un tono alegre."
}

# Prompt template con historial y mensaje actual
chat_prompt = ChatPromptTemplate.from_messages([
    ("system", system_personalidad[personalidad]),
    ("human", "{historial}Usuario: {mensaje}\nAsistente:")
])

# Cadena: prompt + modelo
cadena = chat_prompt | chat_model

# Inicializar historial de mensajes en session_state
if "mensajes" not in st.session_state:
    st.session_state.mensajes = []

# Renderizar historial existente
for msg in st.session_state.mensajes:
    if isinstance(msg, SystemMessage):
        continue
    role = "assistant" if isinstance(msg, AIMessage) else "user"
    with st.chat_message(role):
        st.markdown(msg.content)

# Boton para nueva conversacion
if st.button("Nueva conversacion"):
    st.session_state.mensajes = []
    st.rerun()

# Cuadro de entrada del usuario
pregunta = st.chat_input("Escribe tu mensaje:")

if pregunta:
    # Mostrar inmediatamente el mensaje del usuario
    with st.chat_message("user"):
        st.markdown(pregunta)

    # Formatear historial como string legible para el LLM
    # Se construye ANTES de guardar la pregunta actual
    historial_str = ""
    for msg in st.session_state.mensajes:
        if isinstance(msg, HumanMessage):
            historial_str += f"Usuario: {msg.content}\n"
        elif isinstance(msg, AIMessage):
            historial_str += f"Asistente: {msg.content}\n"

    # Guardar mensaje del usuario en el historial
    st.session_state.mensajes.append(HumanMessage(content=pregunta))

    # Generar respuesta con streaming
    try:
        with st.chat_message("assistant"):
            response_placeholder = st.empty()
            full_response = ""

            # Streaming token a token estilo ChatGPT
            for chunk in cadena.stream({
                "mensaje": pregunta,
                "historial": historial_str
            }):
                full_response += chunk.content
                response_placeholder.markdown(full_response + "▌")

            # Al terminar quitar el cursor
            response_placeholder.markdown(full_response)

        # Guardar respuesta del asistente en el historial
        st.session_state.mensajes.append(AIMessage(content=full_response))

    except Exception as e:
        st.error(f"Error al generar respuesta: {str(e)}")
        st.info("Verifica que tu API Key de Google este configurada correctamente en el archivo .env")
        st.stop()