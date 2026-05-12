import streamlit as st
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_core.prompts import PromptTemplate

load_dotenv()

st.set_page_config(page_title="Chatbot Básico", page_icon="🤖")
st.title("🤖 Chatbot Básico con LangChain")
st.markdown(
    "Este es un *ChatBot de ejemplo* construido con **LangChain + Streamlit**. "
    "¡Escribe tu mensaje abajo para comenzar!"
)

with st.sidebar:
    st.header("Configuración")
    temperature = st.slider("Temperatura", 0.0, 1.0, 0.5, 0.1)
    model_name = st.selectbox("Modelo", ["gemini-2.5-flash"])

# FIX 1: usar temperature del slider
chat_model = ChatGoogleGenerativeAI(model=model_name, temperature=temperature)

if "mensajes" not in st.session_state:
    st.session_state.mensajes = []

prompt_template = PromptTemplate(
    input_variables=["mensaje", "historial"],
    template="""Eres un asistente útil y amigable llamado ChatBot Pro.

Historial de conversación:
{historial}

Responde de manera clara y concisa a la siguiente pregunta: {mensaje}
"""
)

cadena = prompt_template | chat_model

# Mostrar historial
for msg in st.session_state.mensajes:
    if isinstance(msg, SystemMessage):
        continue
    role = "assistant" if isinstance(msg, AIMessage) else "user"
    with st.chat_message(role):
        st.markdown(msg.content)

if st.button("Nueva conversación"):
    # FIX 2: nombre correcto "mensajes" con s
    st.session_state.mensajes = []
    st.rerun()

pregunta = st.chat_input("Escribe tu mensaje:")

if pregunta:
    with st.chat_message("user"):
        st.markdown(pregunta)

    # FIX 3: formatear historial como string legible
    historial_str = ""
    for msg in st.session_state.mensajes:
        if isinstance(msg, HumanMessage):
            historial_str += f"Usuario: {msg.content}\n"
        elif isinstance(msg, AIMessage):
            historial_str += f"Asistente: {msg.content}\n"

    # FIX 4: guardar mensaje del usuario ANTES de la respuesta
    st.session_state.mensajes.append(HumanMessage(content=pregunta))

    try:
        with st.chat_message("assistant"):
            response_placeholder = st.empty()
            full_response = ""

            # FIX 5: usar .stream() con .invoke() correctamente
            for chunk in cadena.stream({
                "mensaje": pregunta,
                "historial": historial_str  # FIX 6: pasar string, no objeto
            }):
                full_response += chunk.content
                response_placeholder.markdown(full_response + "▌")

            response_placeholder.markdown(full_response)

        # FIX 7: guardar respuesta del asistente con nombre correcto
        st.session_state.mensajes.append(AIMessage(content=full_response))

    except Exception as e:  # FIX 8: except dentro del bloque correcto
        st.error(f"Error al generar respuesta: {str(e)}")
        st.info("Verifica que tu API Key de Google esté configurada correctamente en el archivo .env")