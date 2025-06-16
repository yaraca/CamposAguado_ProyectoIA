import streamlit as st
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from info import info

st.title("ALPAX Productos Naturales - Chatbot")
st.write("Bienvenido al chatbot de ALPAX Productos Naturales. Puedes hacer preguntas sobre nuestros productos y servicios.")

if "messages" not in st.session_state:
    st.session_state.messages = []
if "first_message" not in st.session_state:
    st.session_state.first_message = True

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if st.session_state.first_message:
    with st.chat_message("assistant"):
        st.markdown("Hola! Soy el asistente de ALPAX Productos Naturales. ¿En qué puedo ayudarte hoy?")
    
    st.session_state.messages.append({
        "role": "assistant",
        "content": "Hola! Soy el asistente de ALPAX Productos Naturales. ¿En qué puedo ayudarte hoy?"
    })
    st.session_state.first_message = False

if "ollama" not in st.session_state:
    template = """
    Answer the question below in Spanish.

    Here is the context of the conversation: 
    {info}

    {context}

    Question: {question}

    Answer:
    """ 

    model = OllamaLLM(model="llama3")
    prompt = ChatPromptTemplate.from_template(template)
    chain = prompt | model

    context = ""

if prompt := st.chat_input("Escribe tu pregunta aquí..."):

    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    result = chain.invoke({"info": info, "context": context, "question": prompt})

    with st.chat_message("assistant"):
        st.markdown(result)
    st.session_state.messages.append({
        "role": "assistant",
        "content": result
    })

    context += f"Bot: {result}\nTú: {prompt}\n"
