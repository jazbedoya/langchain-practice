# Al ejecutar esto podemos acceder a las variables de entorno,
# la clave API key de OpenAI o Gemini, la que hemos utilizado.

from dotenv import load_dotenv  # cuando lo llamemos irá a buscar un archivo .env
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()


def main():
    print("Hello from langchain-course!\n")

    information = """Elon Reeve Musk (/ˈiːlɒn mʌsk/ Pretoria, 28 de junio de 1971) es un empresario,
    inversor, activista político conservador y magnate estadounidense de origen anglosudafricano.
    Es el fundador, consejero delegado e «ingeniero» en jefe de la empresa SpaceX; inversor ángel,
    director general y arquitecto de productos de Tesla, Inc.; fundador de The Boring Company;
    y cofundador de Neuralink y OpenAI. Con un patrimonio neto estimado en más de 450 mil millones
    de dólares en octubre de 2025, es la persona más rica del mundo según Forbes.

    Musk nació y se crio en una rica familia de Pretoria (Sudáfrica). Estudió brevemente en la
    Universidad de Pretoria antes de trasladarse a Canadá a los 17 años. Se graduó en Economía
    y Física en la Universidad de Pensilvania. En 2002 fundó SpaceX. En 2003 se unió a Tesla
    Motors. En 2015 cofundó OpenAI. En 2022 compró Twitter por 44 000 millones de dólares.

    Ha sido criticado por hacer declaraciones controvertidas y por difundir información errónea
    sobre la pandemia de COVID-19 y teorías de conspiración."""

    summary_template = """
    Toma esta información {information} sobre una persona y crea:
    1. Un resumen corto
    2. 2 datos interesantes sobre esta persona

    Responde en español.
    """

    summary_prompt_template = PromptTemplate(
        input_variables=["information"],
        template=summary_template,
    )

    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)

    chain = summary_prompt_template | llm
    response = chain.invoke(input={"information": information})

    print("=" * 60)
    print("RESPUESTA DE GEMINI:")
    print("=" * 60)
    print(response.content)


if __name__ == "__main__":
    main()
