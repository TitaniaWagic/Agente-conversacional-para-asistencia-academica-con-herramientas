import os
from dotenv import load_dotenv
from langchain.agents import AgentExecutor, create_react_agent
from langchain_core.tools import tool, Tool
from langchain.prompts import PromptTemplate
from langchain_huggingface import HuggingFaceEndpoint, ChatHuggingFace
from langchain_google_genai import ChatGoogleGenerativeAI
from .tools.calculadora import (
    calcular_promedio_de_notas,
    calcular_nota_para_aprobar,
    calcular_nota_para_exonerar,
    verificar_riesgo_cancelacion_matricula,
    verificar_estado_asignatura,
    convertir_porcentaje_a_nota
)
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

@tool
def conversor_porcentaje_nota(consulta: str) -> str:
    """Útil para convertir un porcentaje a una nota según el sistema de calificaciones (Art. 90).
    El usuario pregunta qué nota tiene con un porcentaje específico.
    Ejemplos: '¿qué nota tengo si tengo 75%?', 'tengo 85%, qué nota es?', 'con 60% qué nota saco?'
    """
    import re
    try:
        # Buscar el porcentaje en la consulta
        porcentaje_match = re.search(r'(\d+\.?\d*)\s*%', consulta, re.IGNORECASE)
        if not porcentaje_match:
            # Intentar buscar solo el número
            porcentaje_match = re.search(r'(\d+\.?\d*)', consulta)
        
        if porcentaje_match:
            porcentaje = float(porcentaje_match.group(1))
            return convertir_porcentaje_a_nota(porcentaje)
        else:
            return "No pude encontrar un porcentaje en tu consulta. Por favor, indica el porcentaje, por ejemplo: '¿qué nota tengo con 75%?'"
    except (AttributeError, ValueError):
        return "Error al procesar el porcentaje. Por favor, escribe algo como: '¿qué nota tengo con 75%?'"

@tool
def calculadora_nota_aprobar(consulta: str) -> str:
    """Útil para calcular qué nota necesita un estudiante en el examen final para aprobar.
    El usuario debe proporcionar: primera parcial, segunda parcial, trabajo práctico, 
    trabajo laboratorio (si aplica), y la opción (A, B, o C).
    Ejemplo: 'primera parcial 80, segunda parcial 75, trabajo practico 90, trabajo laboratorio 0, opcion A'
    """
    import re
    # Extraer los valores de la consulta
    try:
        pp1 = float(re.search(r'primera\s+parcial[:\s]+(\d+\.?\d*)', consulta, re.IGNORECASE).group(1))
        pp2 = float(re.search(r'segunda\s+parcial[:\s]+(\d+\.?\d*)', consulta, re.IGNORECASE).group(1))
        tp = float(re.search(r'trabajo\s+pr[aá]ctico[:\s]+(\d+\.?\d*)', consulta, re.IGNORECASE).group(1))
        tl_match = re.search(r'trabajo\s+laboratorio[:\s]+(\d+\.?\d*)', consulta, re.IGNORECASE)
        tl = float(tl_match.group(1)) if tl_match else 0
        opcion_match = re.search(r'opci[oó]n[:\s]+([ABC])', consulta, re.IGNORECASE)
        opcion = opcion_match.group(1).upper() if opcion_match else "A"
        
        return calcular_nota_para_aprobar(pp1, pp2, tp, tl, opcion)
    except (AttributeError, ValueError) as e:
        return """Para calcular la nota necesaria, proporciona la información en este formato:
        'primera parcial X, segunda parcial Y, trabajo practico Z, trabajo laboratorio W, opcion A/B/C'
        Por ejemplo: 'primera parcial 80, segunda parcial 75, trabajo practico 90, trabajo laboratorio 0, opcion A'
        """

@tool
def calculadora_exoneracion(consulta: str) -> str:
    """Útil para calcular si un estudiante puede exonerar el examen final o qué le falta.
    El usuario debe proporcionar: primera parcial, segunda parcial, trabajo práctico, 
    trabajo laboratorio (si aplica), y la opción (A, B, o C).
    """
    import re
    try:
        pp1 = float(re.search(r'primera\s+parcial[:\s]+(\d+\.?\d*)', consulta, re.IGNORECASE).group(1))
        pp2 = float(re.search(r'segunda\s+parcial[:\s]+(\d+\.?\d*)', consulta, re.IGNORECASE).group(1))
        tp = float(re.search(r'trabajo\s+pr[aá]ctico[:\s]+(\d+\.?\d*)', consulta, re.IGNORECASE).group(1))
        tl_match = re.search(r'trabajo\s+laboratorio[:\s]+(\d+\.?\d*)', consulta, re.IGNORECASE)
        tl = float(tl_match.group(1)) if tl_match else 0
        opcion_match = re.search(r'opci[oó]n[:\s]+([ABC])', consulta, re.IGNORECASE)
        opcion = opcion_match.group(1).upper() if opcion_match else "A"
        
        return calcular_nota_para_exonerar(pp1, pp2, tp, tl, opcion)
    except (AttributeError, ValueError):
        return """Para calcular la exoneración, proporciona la información en este formato:
        'primera parcial X, segunda parcial Y, trabajo practico Z, trabajo laboratorio W, opcion A/B/C'
        """

@tool
def verificador_cancelacion_matricula(consulta: str) -> str:
    """Útil para verificar si un estudiante está en riesgo de cancelación de matrícula por exceso de aplazos.
    El usuario debe proporcionar: número de aplazos acumulados y total de materias en el plan de estudios.
    Ejemplo: 'tengo 15 aplazos de 50 materias'
    """
    import re
    try:
        aplazos = int(re.search(r'(\d+)\s+aplazos?', consulta, re.IGNORECASE).group(1))
        total = int(re.search(r'de\s+(\d+)\s+materias?', consulta, re.IGNORECASE).group(1))
        
        return verificar_riesgo_cancelacion_matricula(aplazos, total)
    except (AttributeError, ValueError):
        return """Para verificar el riesgo de cancelación, proporciona:
        'tengo X aplazos de Y materias totales'
        Por ejemplo: 'tengo 10 aplazos de 40 materias'
        """

@tool
def verificador_estado_materia(consulta: str) -> str:
    """Útil para verificar el estado de un estudiante en una materia específica según número de aplazos.
    El usuario debe proporcionar cuántas veces ha sido aplazado en esa materia.
    Ejemplo: 'he sido aplazado 2 veces en esta materia'
    """
    import re
    try:
        aplazos = int(re.search(r'(\d+)\s+veces?', consulta, re.IGNORECASE).group(1))
        return verificar_estado_asignatura(aplazos)
    except (AttributeError, ValueError):
        try:
            aplazos = int(re.search(r'(\d+)\s+aplazos?', consulta, re.IGNORECASE).group(1))
            return verificar_estado_asignatura(aplazos)
        except (AttributeError, ValueError):
            return """Para verificar el estado en una materia, indica:
            'he sido aplazado X veces en esta materia'
            Por ejemplo: 'he sido aplazado 2 veces en esta materia'
            """


def crear_agente():
    herramienta_buscador_reglamentos = Tool(
        name="buscador_reglamentos",
        func=buscador_de_reglamentos.buscar,
        description="Útil para responder preguntas específicas sobre el reglamento académico, como reglas de asistencia, calificaciones, o condiciones de examen."
    )
    tools = [
        calculadora_academica, 
        buscador_faq, 
        conversor_porcentaje_nota,
        herramienta_buscador_reglamentos,
        calculadora_nota_aprobar,
        calculadora_exoneracion,
        verificador_cancelacion_matricula,
        verificador_estado_materia
    ]

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