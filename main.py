# al ejecutar esto podemos acceder a las variables de entorno , la clave api key de openAI o gemini la que hemos utilizado


import os  # para acceder a la variables de entornos

from dotenv import \
    load_dotenv  # cuando lo llamemos ira a busacr una archivo dot env.

load_dotenv()


def main():
    print("Hello from langchain-course!")
    print(os.environ.get("GOOGLE_API_KEY"))


if __name__ == "__main__":
    main()
