from langchain_google_community import GoogleDriveLoader

credentials_path = "credenciales.json"
token_path = "token.json"

loader = GoogleDriveLoader(
    folder_id="root",
    credentials_path=credentials_path,
    token_path=token_path,
    recursive=False,
    file_types=["document"]    # ← solo Google Docs, ignora Sheets y PDFs
)

docs = loader.load()
print(f"Total documentos cargados: {len(docs)}")

for doc in docs:
    print(f"\nArchivo: {doc.metadata}")
    print(f"Contenido: {doc.page_content[:200]}")