import os
from dotenv import load_dotenv
from langchain.agents import AgentExecutor, create_react_agent
from langchain_core.tools import tool, Tool
from langchain.prompts import PromptTemplate
from langchain_huggingface import HuggingFaceEndpoint, ChatHuggingFace
from langchain_google_genai import ChatGoogleGenerativeAI
from .tools.calculadora import calcular_promedio_de_notas
from .tools.buscador import buscar_en_faq, buscador_de_reglamentos

load_dotenv()

def filtro_de_seguridad(consulta: str) -> bool:
    consultas_prohibidas = ["examen", "respuestas", "dame la prueba", "hackear"]
    for palabra in consultas_prohibidas:
        if palabra in consulta.lower():
            return False
    return True

@tool
def calculadora_academica(consulta: str) -> str:
    """Útil para cuando el usuario pide calcular el promedio de varias notas."""
    return calcular_promedio_de_notas(consulta)

@tool
def buscador_faq(consulta: str) -> str:
    """Útil para responder preguntas frecuentes sobre temas generales como horarios o correos."""
    return buscar_en_faq(consulta)


def crear_agente():
    herramienta_buscador_reglamentos = Tool(
        name="buscador_reglamentos",
        func=buscador_de_reglamentos.buscar,
        description="Útil para responder preguntas específicas sobre el reglamento académico, como reglas de asistencia, calificaciones, o condiciones de examen."
    )
    tools = [calculadora_academica, buscador_faq, herramienta_buscador_reglamentos]

    #Selector LLM
    # Opciones válidas: "GOOGLE", "HUGGINGFACE"
    LLM_PROVIDER = "GOOGLE"  #Elige tu proveedor aquí

    print(f"--- Usando el proveedor de LLM: {LLM_PROVIDER} ---")

    if LLM_PROVIDER == "GOOGLE":
        llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.1)
        
    elif LLM_PROVIDER == "HUGGINGFACE":
        llm_endpoint = HuggingFaceEndpoint(
            repo_id="mistralai/Mistral-7B-Instruct-v0.2",
            task="text-generation",
            max_new_tokens=256,
            temperature=0.1,
            stop_sequences=["\nObservation:", "\nThought:"]
        )
        llm = ChatHuggingFace(llm=llm_endpoint)
        
    else:
        raise ValueError(f"Proveedor de LLM '{LLM_PROVIDER}' no reconocido. Opciones válidas: GOOGLE, HUGGINGFACE")

    # Plantilla de prompt personalizada
    template = """
    Eres un asistente que responde preguntas usando herramientas. Sigue estas reglas ESTRICTAMENTE.
    Para ayudarte, tienes acceso a las siguientes herramientas:
    {tools}
    REGLAS DE FORMATO:
    1.  Tu primer paso DEBE seguir este formato:
        Question: La pregunta que debes responder.
        Thought: Tu análisis de la pregunta y qué herramienta usar.
        Action: La herramienta a usar, debe ser una de [{tool_names}].
        Action Input: La entrada para la herramienta.
    2.  Después de `Action Input`, DETENTE. No escribas nada más. El sistema te dará la `Observation`.
    3.  Después de recibir una `Observation`, si ya tienes la respuesta, DEBES usar este formato:
        Thought: Ya tengo la respuesta final.
        Final Answer: Tu respuesta final a la pregunta del usuario.
    4.  REGLA CRÍTICA: Si la `Observation` indica que no se encontró la información, tu respuesta final DEBE ser que no pudiste encontrar la información. No inventes respuestas.
    --- EJEMPLO DE USO ---
    Question: ¿cuál es el promedio de 5 y 4?
    Thought: El usuario quiere calcular un promedio. Debo usar la herramienta 'calculadora_academica'.
    Action: calculadora_academica
    Action Input: 5, 4
    --- FIN DEL EJEMPLO ---
    Ahora, empieza.
    Question: {input}
    {agent_scratchpad}
    """

    prompt = PromptTemplate.from_template(template)
    agent = create_react_agent(llm, tools, prompt)
    
    agent_executor = AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True,
        handle_parsing_errors=True,
        max_iterations=5,
    )
    return agent_executor