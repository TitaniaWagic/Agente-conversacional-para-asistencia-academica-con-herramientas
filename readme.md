# 🤖 Agente Conversacional Académico con LangChain# En el archivo: README.md



[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)# Agente Conversacional para Asistencia Académica

[![LangChain](https://img.shields.io/badge/LangChain-0.2.5-green.svg)](https://www.langchain.com/)

[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)Este proyecto es un agente conversacional inteligente desarrollado para la materia de Inteligencia Artificial I. Su objetivo es proporcionar asistencia 24/7 a los estudiantes, respondiendo preguntas sobre reglamentos, calculando promedios y consultando FAQs.



> **Sistema inteligente de asistencia académica 24/7** desarrollado con LangChain y múltiples proveedores LLM. El agente puede calcular promedios, buscar información en FAQs y consultar reglamentos académicos usando búsqueda semántica.## Características



---*   **Orquestación de Herramientas**: El agente puede decidir qué herramienta usar para cada tarea específica.

*   **Calculadora Académica**: Calcula promedios de notas a partir del lenguaje natural.

## Tabla de Contenidos*   **Buscador de FAQ**: Responde preguntas frecuentes almacenadas en una base de conocimientos.

*   **Buscador Semántico Local**: Busca en documentos de texto (como reglamentos) para encontrar respuestas precisas.

- [Características](#-características)*   **Filtro de Seguridad**: Bloquea consultas inapropiadas para un comportamiento ético y seguro.

- [Arquitectura del Sistema](#-arquitectura-del-sistema)

- [Requisitos Previos](#-requisitos-previos)## Tecnologías Utilizadas

- [Instalación](#-instalación)

- [Configuración](#-configuración)*   **Python 3.10+**

- [Uso](#-uso)*   **LangChain**: Framework principal para la orquestación del agente.

- [Estructura del Proyecto](#-estructura-del-proyecto)*   **Hugging Face**: Para el acceso a modelos de lenguaje de código abierto (Mistral-7B).

- [Herramientas Disponibles](#-herramientas-disponibles)*   **Sentence-Transformers**: Para la creación de embeddings vectoriales.

- [Selector de Proveedores LLM](#-selector-de-proveedores-llm)*   **FAISS (Facebook AI Similarity Search)**: Para la base de datos vectorial y búsqueda semántica.

- [Notebooks de Demostración](#-notebooks-de-demostración)

- [Troubleshooting](#-troubleshooting)## Instalación y Configuración

- [Contribuir](#-contribuir)

Sigue estos pasos para ejecutar el proyecto en tu máquina local.

---

### 1. Clonar el Repositorio

## ✨ Características```bash

git clone https://github.com/TitaniaWagic/Agente-conversacional-para-asistencia-academica-con-herramientas.git

### Funcionalidades Principalescd proyecto-agente-academico

- **Calculadora Académica**: Extrae y calcula promedios de notas desde lenguaje natural
  - Ejemplo: *"¿Cuál es el promedio de 8, 9 y 7?"* → `8.0`
  
- **Búsqueda en FAQ**: Consulta rápida de preguntas frecuentes
  - Base de conocimientos en JSON con respuestas predefinidas
  - Búsqueda por similitud de texto
  
- **Búsqueda Semántica en Reglamentos**: RAG (Retrieval-Augmented Generation)
  - Embeddings vectoriales con `sentence-transformers`
  - Base de datos vectorial FAISS para búsqueda eficiente
  - Responde preguntas sobre reglamentos académicos complejos

- **Filtro de Seguridad**: Bloquea consultas inapropiadas
  - Previene consultas sobre respuestas de exámenes
  - Control de comportamiento ético del agente

- **Selector Multi-LLM**: Cambia fácilmente entre proveedores
  - **Google Gemini** (gemini-2.5-flash) - Por defecto
  - **Hugging Face** (Mistral-7B-Instruct-v0.2)
  - Extensible a otros proveedores (OpenAI, Anthropic, etc.)

### Patrón de Agente ReAct

El agente utiliza el patrón **ReAct** (Reasoning + Acting):
1. **Question**: Recibe la pregunta del usuario
2. **Thought**: Analiza qué herramienta usar
3. **Action**: Selecciona la herramienta apropiada
4. **Action Input**: Proporciona los parámetros
5. **Observation**: Recibe el resultado de la herramienta
6. **Final Answer**: Genera la respuesta final

---

## 🏗️ Arquitectura del Sistema

```
┌─────────────────────────────────────────────────────────────┐
│                     Usuario Final                            │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│                  Filtro de Seguridad                         │
│          (Bloquea consultas inapropiadas)                    │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│              Agente ReAct (LangChain)                        │
│                                                               │
│  ┌─────────────────────────────────────────────┐            │
│  │   Selector de LLM                           │            │
│  │   • Google Gemini (por defecto)             │            │
│  │   • Hugging Face (Mistral-7B)               │            │
│  └─────────────────────────────────────────────┘            │
│                                                               │
│  ┌─────────────────────────────────────────────┐            │
│  │   Prompt ReAct Mejorado                     │            │
│  │   • Instrucciones estrictas                 │            │
│  │   • Ejemplos de uso                         │            │
│  │   • Control de iteraciones (max 5)          │            │
│  └─────────────────────────────────────────────┘            │
└────────────────┬────────────────────────────────────────────┘
                 │
                 ├──────────────┬──────────────┬──────────────┐
                 ▼              ▼              ▼              ▼
         ┌───────────┐  ┌──────────┐  ┌────────────┐  ┌──────────┐
         │Calculadora│  │Buscador  │  │  Buscador  │  │ Futura   │
         │ Académica │  │   FAQ    │  │Reglamentos │  │  Tool    │
         └─────┬─────┘  └────┬─────┘  └─────┬──────┘  └──────────┘
               │             │               │
               │             │               ▼
               │             │        ┌──────────────┐
               │             │        │Vector Store  │
               │             │        │   (FAISS)    │
               │             │        └──────────────┘
               │             │
               ▼             ▼
         ┌─────────────────────────────────┐
         │      Respuesta Final            │
         └─────────────────────────────────┘
```

---

## Requisitos Previos

### Software Requerido

- **Python**: 3.10 o superior
- **pip**: Gestor de paquetes de Python
- **git**: Para clonar el repositorio (opcional)

### APIs Necesarias

Para usar el selector de LLM, necesitarás al menos una de estas claves:

1. **Google Gemini API** (Recomendado - Gratis)
   - Registro: [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Modelo usado: `gemini-2.5-flash`

2. **Hugging Face API** (Alternativa)
   - Registro: [Hugging Face](https://huggingface.co/settings/tokens)
   - Modelo usado: `mistralai/Mistral-7B-Instruct-v0.2`

---

## Instalación

### 1. Clonar el Repositorio

```bash
git clone https://github.com/TitaniaWagic/Agente-conversacional-para-asistencia-academica-con-herramientas.git
cd "TP final IA"
```

### 2. Crear Entorno Virtual (Recomendado)

**Windows (PowerShell):**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar Dependencias

```bash
pip install -r requirements.txt
```

**Dependencias principales instaladas:**
- `langchain==0.2.5` - Framework principal
- `langchain-google-genai` - Cliente de Google Gemini
- `langchain-huggingface==0.0.3` - Cliente de Hugging Face
- `sentence-transformers>=2.7.0` - Para embeddings
- `faiss-cpu>=1.8.0` - Base de datos vectorial
- `python-dotenv>=1.0.0` - Manejo de variables de entorno

---

## Configuración

### 1. Crear Archivo `.env`

Crea un archivo `.env` en la raíz del proyecto:

```bash
# Para usar Google Gemini (Recomendado)
GOOGLE_API_KEY=tu_clave_de_google_aquí

# Para usar Hugging Face (Opcional)
HUGGINGFACEHUB_API_TOKEN=tu_token_de_huggingface_aquí
```

### 2. Seleccionar Proveedor LLM

En `src/agent.py`, línea 41:

```python
LLM_PROVIDER = "GOOGLE"  # Opciones: "GOOGLE" o "HUGGINGFACE"
```

### 3. Personalizar Datos (Opcional)

#### **FAQs** (`data/faq.json`):
```json
[
  {
    "pregunta": "¿Cuál es el correo de soporte técnico?",
    "respuesta": "El correo de soporte técnico es soporte.ti@une.edu.py."
  }
]
```

#### **Reglamentos** (`data/reglamentos.txt`):
Añade el texto completo de tus reglamentos académicos. El sistema creará automáticamente los embeddings.

---

## Uso

### Modo Interactivo (CLI)

Ejecuta el asistente desde la terminal:

```bash
python -m src.main
```

**Ejemplo de conversación:**

```
¡Hola! Soy tu asistente académico. ¿En qué puedo ayudarte?
Escribe 'salir' para terminar la conversación.

Tú: ¿Cuál es el promedio de 8, 9 y 7?

--- Usando el proveedor de LLM: GOOGLE ---

> Entering new AgentExecutor chain...
Question: ¿Cuál es el promedio de 8, 9 y 7?
Thought: El usuario quiere calcular un promedio. Debo usar la herramienta 'calculadora_academica'.
Action: calculadora_academica
Action Input: 8, 9 y 7
Observation: La media de 8.0, 9.0 y 7.0 es: 8.0
Thought: Ya tengo la respuesta final.
Final Answer: El promedio de 8, 9 y 7 es 8.0.

> Finished chain.

Asistente: El promedio de 8, 9 y 7 es 8.0.
```

### Notebooks de Jupyter

Abre los notebooks para pruebas interactivas:

```bash
jupyter lab
```

Luego navega a:
- `notebooks/01_prueba_calculadora.ipynb` - Pruebas de la calculadora y agente básico
- `notebooks/02_prueba_buscador.ipynb` - Pruebas de búsqueda en FAQ y reglamentos

---

## Estructura del Proyecto

```
TP final IA/
│
├── src/                          # Código fuente principal
│   ├── agent.py                  # Configuración del agente y selector LLM
│   ├── main.py                   # Punto de entrada (CLI interactivo)
│   └── tools/                    # Herramientas del agente
│       ├── calculadora.py        # Calculadora de promedios
│       └── buscador.py           # Búsqueda en FAQ y reglamentos (RAG)
│
├── data/                         # Base de conocimientos
│   ├── faq.json                  # Preguntas frecuentes
│   └── reglamentos.txt           # Documento de reglamentos académicos
│
├── notebooks/                    # Jupyter notebooks de demostración
│   ├── 01_prueba_calculadora.ipynb
│   └── 02_prueba_buscador.ipynb
│
├── .env                          # Variables de entorno (API keys)
├── .gitignore                    # Archivos ignorados por git
├── requirements.txt              # Dependencias del proyecto
└── README.md                     # Este archivo
```

---

## Herramientas Disponibles

### 1. Calculadora Académica

**Archivo**: `src/tools/calculadora.py`

**Función**: Extrae números de texto y calcula promedios.

**Tecnologías**:
- Expresiones regulares para extracción de números
- Soporte para formatos: `8`, `8.5`, `8,5`

**Ejemplo de uso**:
```python
from src.tools.calculadora import calcular_promedio_de_notas

resultado = calcular_promedio_de_notas("¿Cuál es el promedio de 7, 8 y 9?")
# Output: "La media de 7.0, 8.0 y 9.0 es: 8.0"
```

### 2. Buscador de FAQ

**Archivo**: `src/tools/buscador.py` → función `buscar_en_faq()`

**Función**: Busca coincidencias en preguntas frecuentes.

**Tecnologías**:
- Carga de JSON con respuestas predefinidas
- Búsqueda por similitud de texto simple

**Ejemplo de uso**:
```python
from src.tools.buscador import buscar_en_faq

respuesta = buscar_en_faq("¿Cuál es el correo de soporte?")
# Output: "El correo de soporte técnico es soporte.ti@une.edu.py."
```

### 3. Buscador Semántico de Reglamentos (RAG)

**Archivo**: `src/tools/buscador.py` → clase `BuscadorSemantico`

**Función**: Búsqueda semántica en documentos largos usando embeddings vectoriales.

**Tecnologías**:
- **Sentence-Transformers**: `paraphrase-multilingual-MiniLM-L12-v2`
- **FAISS**: Base de datos vectorial para búsqueda rápida
- **LangChain**: `RecursiveCharacterTextSplitter` para chunking

**Flujo**:
1. Divide el documento en chunks de 300 caracteres
2. Crea embeddings vectoriales para cada chunk
3. Almacena en FAISS para búsqueda eficiente
4. Recupera los 2 chunks más relevantes para cada consulta

**Ejemplo de uso**:
```python
from src.tools.buscador import buscador_de_reglamentos

respuesta = buscador_de_reglamentos.buscar("¿Cuál es la nota mínima para aprobar?")
# Output: "La nota mínima para aprobar una asignatura es 6.0..."
```

---

## Selector de Proveedores LLM

### Arquitectura del Selector

El sistema permite cambiar fácilmente entre proveedores de modelos de lenguaje editando **una sola línea** en `src/agent.py`:

```python
LLM_PROVIDER = "GOOGLE"  # Cambia a "HUGGINGFACE" para usar Mistral
```

### Proveedores Disponibles

#### 1. **Google Gemini** (Por defecto)

**Ventajas**:
- ✅ Rápido y eficiente
- ✅ API gratuita con límites generosos
- ✅ Excelente comprensión del español
- ✅ Baja latencia

**Configuración**:
```python
if LLM_PROVIDER == "GOOGLE":
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0.1  # Respuestas más determinísticas
    )
```

**Obtener API Key**:
1. Ve a [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Crea un nuevo proyecto
3. Genera una API key
4. Añádela al `.env`: `GOOGLE_API_KEY=tu_clave`

#### 2. **Hugging Face (Mistral-7B)**

**Ventajas**:
- ✅ Open source
- ✅ Control total sobre el modelo
- ✅ Sin límites de uso (dependiendo del plan)
- ✅ Puede ejecutarse localmente

**Configuración**:
```python
elif LLM_PROVIDER == "HUGGINGFACE":
    llm_endpoint = HuggingFaceEndpoint(
        repo_id="mistralai/Mistral-7B-Instruct-v0.2",
        task="text-generation",
        max_new_tokens=256,
        temperature=0.1,
        stop_sequences=["\nObservation:", "\nThought:"]
    )
    llm = ChatHuggingFace(llm=llm_endpoint)
```

**Obtener Token**:
1. Regístrate en [Hugging Face](https://huggingface.co/)
2. Ve a [Settings → Access Tokens](https://huggingface.co/settings/tokens)
3. Crea un token de tipo "Read"
4. Añádelo al `.env`: `HUGGINGFACEHUB_API_TOKEN=tu_token`

### Añadir Nuevos Proveedores

Para añadir un nuevo proveedor (ejemplo: OpenAI):

1. Instala el cliente:
```bash
pip install langchain-openai
```

2. Añade el import en `src/agent.py`:
```python
from langchain_openai import ChatOpenAI
```

3. Añade la condición en el selector:
```python
elif LLM_PROVIDER == "OPENAI":
    llm = ChatOpenAI(
        model="gpt-4",
        temperature=0.1,
        api_key=os.getenv("OPENAI_API_KEY")
    )
```

---

## 📓 Notebooks de Demostración

### Notebook 1: Prueba de Calculadora

**Archivo**: `notebooks/01_prueba_calculadora.ipynb`

**Contenido**:
1. Importación y configuración del agente
2. Pruebas unitarias de la calculadora
3. Pruebas del agente completo con selector LLM

**Ejecutar**:
```bash
jupyter lab notebooks/01_prueba_calculadora.ipynb
```

### Notebook 2: Prueba de Buscadores

**Archivo**: `notebooks/02_prueba_buscador.ipynb`

**Contenido**:
1. Pruebas del buscador de FAQ
2. Pruebas del buscador semántico de reglamentos
3. Pruebas del agente completo con todas las herramientas

**Ejecutar**:
```bash
jupyter lab notebooks/02_prueba_buscador.ipynb
```

---

## Troubleshooting

### Error: "Module not found: langchain_google_genai"

**Solución**:
```bash
pip install langchain-google-genai google-generativeai
```

### Error: "Invalid API key"

**Solución**:
1. Verifica que el archivo `.env` esté en la raíz del proyecto
2. Asegúrate de que la clave sea correcta y esté activa
3. Reinicia el kernel de Jupyter si estás usando notebooks

### Agente entra en bucle infinito

**Solución**:
El prompt tiene `max_iterations=5` para prevenir esto. Si ocurre:
1. Reduce `max_new_tokens` en el endpoint de Hugging Face
2. Asegúrate de que `stop_sequences` esté configurado correctamente
3. Cambia a Google Gemini, que es más estable

### Búsqueda semántica muy lenta

**Solución**:
1. Usa `faiss-cpu` en lugar de `faiss-gpu` para desarrollo local
2. Reduce el tamaño de los chunks en `buscador.py`:
```python
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=200,  # Reduce de 300 a 200
    chunk_overlap=30
)
```

---

## Contribuir

Las contribuciones son bienvenidas. Para contribuir:

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/NuevaCaracteristica`)
3. Commit tus cambios (`git commit -m 'Añadir nueva característica'`)
4. Push a la rama (`git push origin feature/NuevaCaracteristica`)
5. Abre un Pull Request

### Ideas para Contribuir

- Añadir más herramientas (clima, horarios de transporte, etc.)
- Mejorar el soporte multiidioma
- Añadir dashboard con Streamlit
- Mejorar la interfaz CLI con `rich` o `typer`
- Añadir tests unitarios con `pytest`
- Mejorar la documentación

---

## Licencia

Este proyecto está bajo la licencia MIT.

---

## Autor

Desarrollado como proyecto final para la materia **Inteligencia Artificial I**.

---

## Agradecimientos

- **LangChain** - Framework de orquestación de agentes
- **Google** - API de Gemini
- **Hugging Face** - Modelos open source
- **FAISS** - Búsqueda vectorial eficiente
- **Sentence-Transformers** - Embeddings multiidioma

---

## Referencias y Recursos

- [Documentación de LangChain](https://python.langchain.com/)
- [Google Gemini API Docs](https://ai.google.dev/)
- [Hugging Face Inference API](https://huggingface.co/docs/api-inference/)
- [FAISS Documentation](https://github.com/facebookresearch/faiss)
- [Sentence-Transformers](https://www.sbert.net/)

---

<div align="center">

**⭐ Si te gustó el proyecto, dale una estrella en GitHub ⭐**

Made with ❤️ and 🤖

</div>
