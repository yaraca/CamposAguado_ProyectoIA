from langchain.llms import Ollama

llm = Ollama(model="llama3")
respuesta = llm("¿Cuál es la capital de México?")
print(respuesta)
