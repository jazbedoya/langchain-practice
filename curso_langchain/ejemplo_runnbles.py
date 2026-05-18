from langchain_core.runnables import RunnableLambda

paso1= RunnableLambda(lambda x : F"NUmero{x}")

def duplicar_texto(texto):
    return[texto]*2


paso2= RunnableLambda(duplicar_texto)


cadena = paso1 | paso2


resultado = cadena.invoke(45)
print(resultado)