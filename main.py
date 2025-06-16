# main.py
from langchain_ollama import OllamaLLM
from langchain.prompts import ChatPromptTemplate
from info import info

template = """
Answer the question below in Spanish.

Here is the constext of the conversation: 
{info}

{context}

Question: {question}

Answer:

""" 

model = OllamaLLM(model = "llama3")
prompt = ChatPromptTemplate.from_template(template)
chain = prompt | model


def chat():
    print("Bienvenido al chat! Escribe 'stop' para salir.")
    context = ""
    while True:
        question = input("Tú: ")
        if question == "stop":
            break

        result = chain.invoke({"info":info, "context": context, "question": question})
        print("Bot:", result)
        context += f"Bot: {result}\nTú: {question}\n"


if __name__ == "__main__":
    chat()