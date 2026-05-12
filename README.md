# 🦜 LangChain Practice

Proyectos prácticos con **LangChain + Google Gemini** mientras aprendo a construir aplicaciones con LLMs.

## 🚀 Proyectos incluidos

### 🤖 Chatbot Conversacional con Streaming

Chatbot tipo ChatGPT construido con LangChain, Google Gemini 2.5 Flash y Streamlit.

**Features:**
- 💬 Memoria conversacional persistente
- ⚡ Streaming de respuestas en tiempo real (token a token)
- 🎛️ Sidebar interactiva con control de temperatura y selección de modelo
- 🎨 Tema oscuro personalizado
- 🔄 Botón para reiniciar conversación
- 🛡️ Manejo robusto de errores

**Stack:** Python 3.13 · LangChain · Google Gemini 2.5 · Streamlit · LCEL

📁 [`curso_langchain/streamlit_chatbot.py`](curso_langchain/streamlit_chatbot.py)

---

### 📝 Ice Breaker — Resumen de Personas con LLM

Script que toma información de una persona y genera un resumen + datos curiosos usando Gemini.

**Conceptos demostrados:**
- PromptTemplate con variables
- LCEL (LangChain Expression Language) con operador pipe `|`
- Gestión segura de API keys con `.env`

📁 [`main.py`](main.py)

---

## 🛠️ Stack Tecnológico

| Categoría | Tecnologías |
|---|---|
| **Lenguaje** | Python 3.13 |
| **LLM** | Google Gemini 2.5 Flash |
| **Framework IA** | LangChain · LangChain Core |
| **Frontend** | Streamlit |
| **Gestión de dependencias** | uv |
| **Control de versiones** | Git · GitHub |

## 📦 Setup

```bash
# 1. Clonar el repositorio
git clone https://github.com/jazbedoya/langchain-practice.git
cd langchain-practice

# 2. Instalar dependencias con uv
uv sync

# 3. Configurar API key (crea archivo .env)
echo "GOOGLE_API_KEY=tu_key_aqui" > .env

# 4. Ejecutar el chatbot
uv run streamlit run curso_langchain/streamlit_chatbot.py
```

> 🔑 Consigue tu API key gratis en [Google AI Studio](https://aistudio.google.com/)

## 🎯 Conceptos aprendidos

- ✅ Integración de LLMs (Gemini) en aplicaciones Python
- ✅ Prompt engineering con PromptTemplates
- ✅ Composición de cadenas con LCEL (`prompt | llm`)
- ✅ Streaming de respuestas en tiempo real
- ✅ Gestión de estado conversacional con `session_state`
- ✅ Despliegue de apps web interactivas con Streamlit
- ✅ Buenas prácticas: variables de entorno, manejo de errores

## 👤 Autora

**Jazmín Bedoya** — Backend Python Engineer  
📍 Málaga, España

🔗 [GitHub](https://github.com/jazbedoya)
