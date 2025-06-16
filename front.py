import streamlit as st
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from info import info

#COnfiguación general de la página
st.set_page_config(
    page_title="ALPAX Productos Naturales Chatbot",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)

#------Sidebar------
st.sidebar.image("logo.png", width=200)
st.sidebar.title("ALPAX Productos Naturales")
st.sidebar.markdown("---")
st.sidebar.markdown("Productos Naturales de alta calidad para el bienestar.")
st.sidebar.markdown("- 🧪 Suplementos Alimenticios\n- 💧 Líquidos Orales\n- 💊 Sólidos Orales\n- 🌿 Nutracéuticos\n- 🧴 Cosméticos\n- 🧒 Línea Especial\n- 🏋️ Línea Deportiva")
st.sidebar.markdown("---")
st.sidebar.markdown("### Información de la Empresa")
st.sidebar.markdown("**Contacto:**\n- 📞 33 1122 3366\n- ✉️ contacto@alpaxnatural.com\n- 🌐 [Sitio web](https://alpaxnatural.com)")

#-------Estilo de la página-------
st.markdown("""
    <style>
    .main {
        background-color: #f0f4f8;
    }
    .stChatMessage {
        background-color: #b4e08c;
        border-radius: 10px;
        padding: 10px;
        margin-bottom: 10px;
    }
    .stButton>button {
        color:white;
        background: #4CAF50;
    }
    </style>
""", unsafe_allow_html=True)

#-----------Encabezado-----------
col1, col2 = st.columns([1, 5])
with col1:
    st.image("logo.png", width=120)
with col2:
    st.title("ALPAX Chatbot")
    st.write("¡Hola! Soy el asistente virtual de ALPAX Productos Naturales. Estoy aquí para responder tus preguntas sobre nuestros productos y servicios. ")
st.markdown("---")

#-----------Estado de la sesión-----------
if "messages" not in st.session_state:
    st.session_state.messages = []
if "first_message" not in st.session_state:
    st.session_state.first_message = True

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

# --- Mostrar historial del chat ---
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- Primer mensaje automático ---
if st.session_state.first_message:
    bienvenida = "Hola 👋 Soy el asistente de ALPAX Productos Naturales. ¿En qué puedo ayudarte hoy?"
    with st.chat_message("assistant"):
        st.markdown(bienvenida)
    st.session_state.messages.append({"role": "assistant", "content": bienvenida})
    st.session_state.first_message = False

#----------Entrada del usuario----------
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

