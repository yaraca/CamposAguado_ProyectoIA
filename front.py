#Librerias necesarias
#-----Librerías necesarias---------
import streamlit as st  #Librería para crear aplicaciones web interactivas
from langchain_ollama import OllamaLLM #Librería para conectar con el modelo de lenguaje de Ollama
from langchain_core.prompts import ChatPromptTemplate #Librería para crear el prompt del modelo
from info import info #Importa la información del negocio desde el archivo info.py

#----COnfiguación general de la página----
#Configura el título, icono y diseño de la página de Streamlit
st.set_page_config(
    page_title="ALPAX Productos Naturales Chatbot",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)

#------Sidebar------
st.sidebar.image("logo.png", width=200) #muestra el logo de la empresa en la barra lateral
st.sidebar.title("ALPAX Productos Naturales") #título de la barra lateral
st.sidebar.markdown("---") 
st.sidebar.markdown("Productos Naturales de alta calidad para el bienestar.") #mensaje de bienvenida
st.sidebar.markdown("- 🧪 Suplementos Alimenticios\n- 💧 Líquidos Orales\n- 💊 Sólidos Orales\n- 🌿 Nutracéuticos\n- 🧴 Cosméticos\n- 🧒 Línea Especial\n- 🏋️ Línea Deportiva")
st.sidebar.markdown("---")
st.sidebar.markdown("### Información de la Empresa")
st.sidebar.markdown("**Contacto:**\n- 📞 33 1122 3366\n- ✉️ contacto@alpaxnatural.com\n- 🌐 [Sitio web](https://alpaxnatural.com)")

#-------Estilo de la página-------
#Aplica estilos personalizados a la página de Streamlit
# Esto cambia el color de fondo, el estilo de los mensajes del chat y los botones.
st.markdown("""
    <style>
    .main {
        background-color: #f0f4f8;
    }
    .stChatMessage {
        background-color: #b4e08c;
        border-radius: 10px;
        padding: 10px; #Espacio interno para los mensajes del chat
        margin-bottom: 10px;
    }
    .stButton>button {
        color:white;
        background: #4CAF50;
    }
    </style>
""", unsafe_allow_html=True) #unsafe_allow_html=True permite usar HTML y CSS personalizados
# Esto es necesario para aplicar estilos personalizados a la página de Streamlit.

#-----------Encabezado-----------
col1, col2 = st.columns([1, 5]) #Crea dos columnas para el encabezado, una para el logo y otra para el título y descripción
with col1: #Columna para el logo
    st.image("logo.png", width=120)
with col2: #Columna para el título y descripción
    st.title("ALPAX Chatbot")
    st.write("¡Hola! Soy el asistente virtual de ALPAX Productos Naturales. Estoy aquí para responder tus preguntas sobre nuestros productos y servicios. ")
st.markdown("---")

#-----------Estado de la sesión-----------
if "messages" not in st.session_state: # Verifica si la variable de estado de sesión "messages" existe, si no, la inicializa como una lista vacía
    st.session_state.messages = [] #Lista para almacenar los mensajes del chat
if "first_message" not in st.session_state: # Verifica si la variable de estado de sesión "first_message" existe, si no, la inicializa como True
    # Esta variable se usa para mostrar un mensaje de bienvenida solo una vez al inicio del chat
    # y evitar que se repita en cada interacción.
    st.session_state.first_message = True 

if "ollama" not in st.session_state: # Verifica si la variable de estado de sesión "ollama" existe, si no, la inicializa como una instancia del modelo de lenguaje
    # Esta variable se usa para almacenar el modelo de lenguaje de Ollama y evitar que se cree una nueva instancia en cada interacción.
    # Esto mejora el rendimiento al reutilizar el modelo ya cargado.
    #Se carga la plantilla del prompt y el modelo de lenguaje de Ollama solo una vez al inicio del chat.
    template = """
    Answer the question below in Spanish.

    Here is the context of the conversation: 
    {info}

    {context}

    Question: {question}

    Answer:
    """ 

    model = OllamaLLM(model="llama3") # Crea una instancia del modelo de lenguaje de Ollama, especificando el modelo a utilizar (en este caso, "llama3").
    prompt = ChatPromptTemplate.from_template(template) # Crea un prompt de chat a partir de la plantilla definida anteriormente.
    chain = prompt | model # Crea una cadena de procesamiento que combina el prompt y el modelo, permitiendo enviar preguntas y recibir respuestas.

    context = "" # Inicializa el contexto vacío, donde se acumularán las preguntas y respuestas del chat.

# --- Mostrar historial del chat ---
for message in st.session_state.messages: #iterar sobre los mensajes almacenados en el estado de la sesión
    # Muestra cada mensaje en el chat según su rol (usuario o asistente)
    with st.chat_message(message["role"]): 
        st.markdown(message["content"])

# --- Primer mensaje automático ---
if st.session_state.first_message: #Si es el primer mensaje del chat, muestra un mensaje de bienvenida
    # Este mensaje se muestra solo una vez al inicio del chat para dar la bienvenida al usuario.
    bienvenida = "Hola 👋 Soy el asistente de ALPAX Productos Naturales. ¿En qué puedo ayudarte hoy?"
    # Muestra el mensaje de bienvenida en el chat y lo agrega al historial de mensajes
    with st.chat_message("assistant"): # Muestra el mensaje de bienvenida como un mensaje del asistente
        st.markdown(bienvenida) 
    st.session_state.messages.append({"role": "assistant", "content": bienvenida}) #Los mensajes se almacenan en el estado de la sesión para mantener el historial del chat.
    # Marca que ya se ha mostrado el primer mensaje para no repetirlo en futuras interacciones
    st.session_state.first_message = False # Esto evita que el mensaje de bienvenida se muestre nuevamente en cada interacción.

#----------Entrada del usuario----------
if prompt := st.chat_input("Escribe tu pregunta aquí..."): # Solicita al usuario que ingrese su pregunta en el chat

    with st.chat_message("user"): #Muestra la pregunta del usuario como un mensaje del usuario
        st.markdown(prompt) 
    # Agrega el mensaje del usuario al historial de mensajes
    # Esto permite que el asistente recuerde la pregunta del usuario y la use para generar una respuesta.
    st.session_state.messages.append({
        "role": "user", # El rol del mensaje es "user" para indicar que es una pregunta del usuario
        "content": prompt # El contenido del mensaje es la pregunta ingresada por el usuario
    })

    # Invoca la cadena de procesamiento con la información del negocio, el contexto acumulado y la pregunta del usuario.
    # Esto genera una respuesta del modelo de lenguaje basada en el contexto y la pregunta.
    result = chain.invoke({"info": info, "context": context, "question": prompt}) 

    with st.chat_message("assistant"): # Muestra la respuesta del modelo como un mensaje del asistente
        st.markdown(result) # El contenido de la respuesta es el resultado generado por el modelo de lenguaje
    # Agrega la respuesta del asistente al historial de mensajes
    st.session_state.messages.append({
        "role": "assistant",
        "content": result
    })

    # Actualiza el contexto acumulado con la pregunta del usuario y la respuesta del modelo, 
    # para que se utilice en la siguiente iteración del chat.
    context += f"Bot: {result}\nTú: {prompt}\n" 

