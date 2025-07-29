import streamlit as st
from orchestrator import build_orchestrator_agent

# Page design
st.set_page_config(page_title="IoT Threat Detection Chat", page_icon="🦥", layout="centered")

st.title("🦥 IoT Security Threat Detection Chat")
st.write("Envía un log y el asistente lo analizará para detectar amenazas.")

# Initialize the agent once per session
@st.cache_resource(show_spinner="Cargando modelo y agente, espera unos segundos...")
def load_agent():
    return build_orchestrator_agent()

agent = load_agent()

# Session state to save the chat history 
if "history" not in st.session_state:
    st.session_state.history = []

# User form 
with st.form("log_form", clear_on_submit=True):
    user_input = st.text_area("Introduce aquí tu log para analizar:", height=120)
    submitted = st.form_submit_button("Enviar")

if submitted and user_input.strip():
    st.session_state.history.append(("user", user_input))

    response = agent.run(user_input)
    st.session_state.history.append(("bot", response))

# Show conversation
for speaker, msg in reversed(st.session_state.history):
    if speaker == "bot":
        st.chat_message("assistant").write(msg)
    else:
        st.chat_message("user").write(msg)
