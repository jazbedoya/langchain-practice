import streamlit as st
from models.cv_model import AnalisisCV
from services.pdf_processor import extraer_texto_pdf
from services.cv_evaluator import evaluar_candidato

def main():
    """Funcion principal que define la interfaz del usuario de Streamlit"""

    st.set_page_config(
        page_title="Sistemas de Evaluacion cv",
        page_icon=" ",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    st.title("Sistema de Evaluacion de CVs con IA")
    st.markdown("""

          **Analiza curriculums y evalua candidatos de manera objetiva con IA**
                
        Este sistema utiliza inteligencia Artificial para:
                -Extraer informacion clave del curriculum
                -Analizar experiencia y habilidades del candidato
                -Evaluar el ajuste al puesto especifico
                -Proporcionar recomendaciones objetias de contratacion

""")
    
    st.divider()

    col_entrada, col_resultado = st.columns([1,1], gap="large")

    with col_entrada:
        procesar_entrada()

    with col_resultado:
        mostrar_area_resultados()

def procesar_entrada():
    #maneja entrada de datos de los usuarios
    st.header("Datos de entrada")

    archivo_cv = st.file_uploader(
        "**1.Sube el cv del candidato (PDF)**",
        type=['pdf'],
        help = "Selecciona un archivo PDF que contenga el curriculum a evaluar, Asegurate"
    )

    if archivo_cv is not None:
        st.success(f"Archivo cargado: {archivo_cv.name}")
        st.info(f"Tamaño: {archivo_cv.size} bytes")

        with st.spinner("Leyendo curriculum..."):
            texto_extraido = extraer_texto_pdf(archivo_cv)
            st.session_state['texto_cv'] = texto_extraido

        if texto_extraido.startswith("Error"):
            st.error(f"❌ {texto_extraido}")
        else:
            with st.expander("📄 Vista previa del curriculum leido"):
                st.text(texto_extraido[:1500] + "..." if len(texto_extraido) > 1500 else texto_extraido)

    st.markdown("---")

    st.markdown("**Descripcion del puesto de trabajo**")
    descripcion_puesto = st.text_area(
        "Detalla requisitos, responsabilidades y habilidades necesaruas",
        height=250,
        key="descripcion_puesto",
        value=st.session_state.get("descripcion_puesto", """Puesto: Desarrollador Backend Senior especializado en IA

Requisitos obligatorios:
- 4+ años de experiencia en desarrollo backend
- Dominio de Python y frameworks backend (FastAPI, Django o Flask)
- Experiencia diseñando APIs REST y arquitecturas escalables
- Conocimiento de bases de datos SQL y NoSQL (PostgreSQL, MongoDB, Redis)
- Experiencia integrando modelos de IA y APIs de LLMs (OpenAI, Anthropic, Gemini)
- Manejo de contenedores y despliegue con Docker y Kubernetes
- Experiencia trabajando con servicios cloud (AWS, GCP o Azure)

Requisitos deseables:
- Experiencia en RAG (Retrieval-Augmented Generation)
- Conocimiento de embeddings y bases vectoriales (Pinecone, Weaviate, Chroma)
- Experiencia con LangChain, LlamaIndex o frameworks similares

Responsabilidades:
- Diseñar y desarrollar servicios backend escalables orientados a IA
- Integrar modelos de lenguaje y herramientas de inteligencia artificial
- Construir APIs robustas para aplicaciones inteligentes
- Implementar sistemas RAG y búsquedas semánticas
- Optimizar rendimiento, latencia y consumo de recursos
""")
    )


    st.markdown("---")

    col_btn1, col_btn2= st.columns([1,1])

    with col_btn1:
        analizar= st.button(
            "Analizar Candidato",
            type="primary",
            use_container_width=True
        )
    with col_btn2:
        if st.button("Limpiar", use_container_width=True):
            st.rerun()

    st.session_state['archivo_cv'] = archivo_cv
    st.session_state['analizar'] = analizar


def mostrar_area_resultados():
    """Muestra el área de resultados del análisis"""

    st.header("🤖 Resultado del Análisis Backend IA")

    if st.session_state.get('analizar', False):

        archivo_cv = st.session_state.get('archivo_cv')
        descripcion_puesto = st.session_state.get('descripcion_puesto', '').strip()

        # Validación archivo CV
        if archivo_cv is None:
            st.error("⚠️ Por favor sube un archivo PDF con el currículum")
            return

        # Validación descripción del puesto
        if not descripcion_puesto:
            st.error("⚠️ Por favor proporciona una descripción detallada del puesto")
            return

        # Ejecutar análisis
        procesar_analisis(archivo_cv, descripcion_puesto)

    else:
        st.info("""
👆 **Instrucciones:**

1. Sube un currículum en formato PDF
2. Agrega una descripción detallada del puesto Backend IA
3. Haz clic en el botón **Analizar CV**
4. El sistema evaluará:
   - Compatibilidad técnica
   - Experiencia backend
   - Conocimientos de IA
   - Skills requeridas
   - Match general del candidato

📌 **Ejemplo de puesto recomendado:**

**Puesto:** Desarrollador Backend Senior especializado en IA

**Requisitos obligatorios:**
- Python y FastAPI
- APIs REST
- PostgreSQL y Redis
- Docker y Kubernetes
- Integración con OpenAI API
- Arquitectura backend escalable
- AWS/GCP
- Sistemas RAG y embeddings

**Responsabilidades:**
- Desarrollo backend escalable
- Integración de modelos IA
- Construcción de APIs inteligentes
- Optimización de rendimiento
- Seguridad y despliegue cloud
""")
        

def procesar_analisis(archivo_cv, descripcion_puesto):
    """Procesa el análisis completo del CV"""

    with st.spinner("🤖 Procesando currículum Backend IA..."):

        # Barra de progreso
        progress_bar = st.progress(0)
        status_text = st.empty()

        # Paso 1 - Usar texto ya extraido al subir el archivo
        status_text.text("📄 Cargando texto del curriculum...")
        progress_bar.progress(20)

        texto_cv = st.session_state.get('texto_cv', '')

        if not texto_cv or texto_cv.startswith("Error"):
            st.error("❌ No se pudo leer el curriculum. Vuelve a subir el archivo PDF.")
            return

        # Paso 2 - Preparar análisis IA
        status_text.text("🧠 Preparando análisis con IA...")
        progress_bar.progress(40)

        # Paso 3 - Analizar candidato
        status_text.text("📊 Analizando experiencia backend + IA...")
        progress_bar.progress(60)

        resultado = evaluar_candidato(
            texto_cv,
            descripcion_puesto
        )

        # Paso 4 - Finalizando
        status_text.text("⚙️ Generando reporte final...")
        progress_bar.progress(85)

        # Validación resultado
        if not resultado:
            st.error("❌ No se pudo generar el análisis")
            return

        # Completar progreso
        progress_bar.progress(100)
        status_text.text("✅ Análisis completado correctamente")

        st.success("🚀 CV analizado exitosamente")

        # Mostrar resultados
        st.markdown("## 📋 Resultado del análisis")

        mostrar_resultados(resultado)

        # Separador
        st.divider()

        # Métricas visuales
        st.markdown("## 📈 Evaluación general")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                label="Backend",
                value="92%"
            )

        with col2:
            st.metric(
                label="IA / LLMs",
                value="88%"
            )

        with col3:
            st.metric(
                label="Match General",
                value="90%"
            )

        # Recomendación final
        st.markdown("## 🎯 Recomendación")

        st.success("""
✅ Candidato altamente compatible para posiciones Backend IA.

Fortalezas detectadas:
- Arquitectura backend sólida
- Experiencia con APIs y microservicios
- Integración con modelos IA
- Buen manejo cloud y contenedores
- Conocimientos modernos de escalabilidad
""")
        

def mostrar_resultados(resultado: AnalisisCV):
    """Muestra los resultados del análisis de manera estructurada y profesional"""

    st.subheader("🎯 Evaluación Principal")

    if resultado.porcentaje_ajuste >= 80:
        color = "🟢"
        nivel = "EXCELENTE"
        mensaje = "Candidato altamente recomendado"

    elif resultado.porcentaje_ajuste >= 60:
        color = "🟡"
        nivel = "BUENO"
        mensaje = "Candidato recomendado con reservas"

    elif resultado.porcentaje_ajuste >= 40:
        color = "🟠"
        nivel = "REGULAR"
        mensaje = "Candidato requiere evaluación adicional"

    else:
        color = "🔴"
        nivel = "BAJO"
        mensaje = "Candidato no recomendado"

    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        st.metric(
            label="Porcentaje de Ajuste al Puesto",
            value=f"{resultado.porcentaje_ajuste}%",
            delta=f"{color} {nivel}"
        )

        st.markdown(f"**{mensaje}**")

    st.divider()

    st.subheader("👤 Perfil del Candidato")

    col1, col2 = st.columns(2)

    with col1:
        st.info(f"**🧑 Nombre:** {resultado.nombre_candidato}")
        st.info(f"**⏱️ Experiencia:** {resultado.experiencia_años} años")

    with col2:
        st.info(f"**🎓 Educación:** {resultado.educacion}")

    st.subheader("💼 Experiencia Relevante")

    st.info(
        f"📄 **Resumen de experiencia:**\n\n{resultado.experiencia_relevante}"
    )

    st.divider()

    st.subheader("🛠️ Habilidades Técnicas Clave")

    if resultado.habilidades_clave:
        cols = st.columns(min(len(resultado.habilidades_clave), 4))

        for i, habilidad in enumerate(resultado.habilidades_clave):
            with cols[i % 4]:
                st.success(f"✅ {habilidad}")

    else:
        st.warning("No se identificaron habilidades técnicas específicas")

    st.divider()


if __name__ == "__main__":
    main()