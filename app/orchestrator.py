import os
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"

from dotenv import load_dotenv
load_dotenv() 

from langchain.agents import initialize_agent, AgentType
from langchain.memory import ConversationBufferMemory
from langchain.schema import SystemMessage
from langchain_mistralai.chat_models import ChatMistralAI
from tools.is_attack import is_attack_tool
from tools.attack_type import attack_type_tool

def build_orchestrator_agent():
    mistral_api_key = os.getenv("MISTRAL_API_KEY")
    mistral_model_name = os.getenv("MISTRAL_MODEL_NAME")

    if not mistral_api_key:
        raise RuntimeError("Debes establecer tu MISTRAL_API_KEY en el entorno.")
    if not mistral_model_name:
        raise RuntimeError("Debes establecer tu MISRTAL_MODEL_NAME en el entorno.")

    llm = ChatMistralAI(
        model=mistral_model_name,  
        temperature=0.7,
        max_tokens=512,
        api_key=mistral_api_key
    )

    system_prompt = """
    Eres un asistente experto en ciberseguridad. Hablas en el mismo idioma que el usuario (por ejemplo, español o inglés).

    Tu objetivo es ayudar a analizar registros (logs) de red. Debes actuar de forma cercana y profesional, guiando al usuario en todo momento. Usa las herramientas disponibles solo cuando sea necesario.

    Instrucciones de comportamiento:

    1. Si el usuario te envía un posible log de red:
        - Usa la herramienta 'Detect Attack' para determinar si se trata de un ataque o tráfico normal.

    2. Si el resultado es tráfico normal:
        - Responde con claridad y amabilidad, por ejemplo: "No threats were detected in this log. Would you like to analyze another one?"

    3. Si el resultado es un ataque:
        - Informa al usuario de forma clara y proactiva: "A potential attack has been detected in the log. Would you like me to classify the specific attack type?"
        - Si el usuario acepta o pide más información, entonces puedes usar la herramienta 'Classify Attack Type'.

    4. Si el texto no parece un log válido:
        - Responde educadamente, por ejemplo: "This doesn't appear to be a valid network log. Please ensure it's properly formatted and try again."

    5. Mantén siempre un tono empático, profesional y claro. No tomes decisiones por adelantado: pregunta antes de usar herramientas adicionales.
    """

    agent = initialize_agent(
        tools=[is_attack_tool, attack_type_tool],
        llm=llm,
        agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION,
        verbose=True,
        memory=ConversationBufferMemory(memory_key="chat_history", return_messages=True),
        system_message=SystemMessage(content=system_prompt)
    )

    return agent
