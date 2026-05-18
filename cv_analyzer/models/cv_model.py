from pydantic import BaseModel, Field

class AnalisisCV(BaseModel):
    """MOdelo de datos para analisi de un CV."""
    nombre_candidato : str = Field(description="Nombre completo del candidato extraido del CV.")
    experiencia_años : int = Field(description="Años totales de experiencia laboral relevante.")
    habilidades_clave : list[str] = Field(description="Lista de las 5-7 habilidades del candidato mas relevantes para el puesto")
    educacion: str = Field(description="Nivel educativo mas alto y especializacion principal.")
    experiencia_relevante : str = Field(description="Resumen especifico de la experiencia mas relevante para el puesto.")
    fortalezas : list[str]= Field(description="3- 5 principales fortalezas del candidato basada en el puesto")
    areas_mejora : list[str] = Field(description="2-4 areas donde el candidato podria mejorar")
    porcentaje_ajuste : int = Field(description="Porcentaje de ajuste al puesto (0-100) basado en experiencia, habilidades y formacion", ge= 0, le=100)



