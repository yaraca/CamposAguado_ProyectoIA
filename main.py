#-----Librerías necesarias---------
from langchain_ollama import OllamaLLM #sirve para conectar con el modelo de Ollama
from langchain.prompts import ChatPromptTemplate #sirve para crear el prompt del modelo
from info import info #importa la información del negocio desde el archivo info.py

#-----Plantilla del prompt----------
#Esta plantilla define cómo se formateará la pregunta y el contexto para el modelo de lenguaje.
#El modelo responderá en español, utilizando el contexto de la conversación y la información del negocio.
#El contexto se irá acumulando a medida que se realicen más preguntas.
#La plantilla incluye un espacio para la pregunta del usuario y el contexto de la conversación.
#El modelo generará una respuesta en español basada en esta información.
template = """
Answer the question below in Spanish. 

Here is the constext of the conversation: 
{info}

{context}

Question: {question}

Answer:

""" 


model = OllamaLLM(model = "llama3") #Crea una instancia del modelo de lenguaje de Ollama, especificando el modelo a utilizar (en este caso, "llama3").
#Crea un prompt de chat a partir de la plantilla definida anteriormente.
prompt = ChatPromptTemplate.from_template(template)
chain = prompt | model #Crea una cadena de procesamiento que combina el prompt y el modelo, permitiendo enviar preguntas y recibir respuestas.


#-------Función para iniciar el chat---------
def chat():
    print("Bienvenido al chat! Escribe 'stop' para salir.")
    context = "" #Inicializa el contexto vacío, donde se acumularán las preguntas y respuestas del chat.
    while True: #Mientras el usuario no escriba 'stop', el chat continuará.
        question = input("Tú: ") #Solicita al usuario que ingrese una pregunta.
        if question == "stop": #Si el usuario escribe 'stop', se termina el chat.
            break

        #Imprime la pregunta del usuario en la consola.
        result = chain.invoke({"info":info, "context": context, "question": question}) #Invoca la cadena de procesamiento con la información del negocio, el contexto acumulado y la pregunta del usuario.
        print("Bot:", result) #Imprime la respuesta del modelo en la consola.
        context += f"Bot: {result}\nTú: {question}\n" #Actualiza el contexto acumulado con la pregunta del usuario y la respuesta del modelo, para que se utilice en la siguiente iteración del chat.

#-------Punto de entrada del programa---------
if __name__ == "__main__":
    chat() #Llama a la función chat() para iniciar el chat cuando se ejecuta el script directamente. 