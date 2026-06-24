# Configuración de modelos

EMBEDDING_MODEL = "models/gemini-embedding-001"

QUERY_MODEL = "gemini-2.5-flash"

GENERATION_MODEL = "gemini-2.5-flash"

# Base vectorial
CHROMA_DB_PATH = "./chroma_db"


#Confi del REtriver
SEARCH_TYPE= "mmr"
MMR_DIVERSITY_LAMBDA= 0.7
MMR_FETCH_K =20
SEARCH_K=2