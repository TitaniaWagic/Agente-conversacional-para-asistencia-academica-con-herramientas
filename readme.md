# 🤖 Agente Conversacional Académico con Herramientas (LangChain)

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)

[![LangChain](https://img.shields.io/badge/LangChain-0.2.5-green.svg)](https://www.langchain.com/)

[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Este proyecto implementa un agente conversacional inteligente con orquestación de herramientas para asistencia académica, desarrollado como trabajo final de **Inteligencia Artificial I** (2025). Proporciona soporte 24/7 a estudiantes para consultas sobre reglamentos, cálculos de notas y preguntas frecuentes, utilizando IA moderna, reglas de seguridad y búsqueda semántica.

***

## 💡 Justificación y Objetivos

- **Problema Solucionado:** Facilita el acceso inmediato a información relevante, reduce la carga administrativa y responde consultas recurrentes de manera personalizada, superando las limitaciones de sistemas FAQ estáticos.
- **Objetivos SMART:**
  - *Específico*: Implementa tres herramientas integradas (calculadora, buscador de reglamentos y FAQ), más filtro de seguridad.
  - *Medible*: ≥80% de exactitud en FAQ y 100% precisión matemática.
  - *Alcanzable*: Usando frameworks adecuados (LangChain, Python).
  - *Relevante*: Mejora la experiencia estudiantil y reduce trabajo administrativo.
  - *Temporal*: Entrega y validación antes del 31/10/2025.
- **Estado del Arte:** Aprovecha agentes reactivos y modularidad de herramientas, como recomiendan revisiones recientes en educación con IA.[1][2][3]

***

## ✨ Características Principales

- **Orquestación de Herramientas**: Toma decisiones dinámicas sobre qué módulo invocar.
- **Calculadora Académica Avanzada**: 
  - Calcula promedios de notas
  - **🆕 Convierte porcentajes a notas** (según escala del Art. 90)
  - Determina nota necesaria en el examen final para aprobar
  - Calcula posibilidad de exoneración (94% en evaluaciones parciales)
  - Verifica riesgo de cancelación de matrícula por aplazos (Art. 71)
  - Analiza estado en asignaturas específicas (Art. 70)
  - Soporta 3 opciones de distribución de porcentajes de evaluación
- **Buscador de FAQ**: Consulta en una base JSON con respuestas predefinidas; búsqueda por similitud textual.
- **Buscador Semántico RAG**: Recupera información de reglamentos académicos usando embeddings y FAISS.
- **Filtro de Seguridad**: Bloquea solicitudes inapropiadas según reglas académicas.
- **Selector Multi-LLM**: Permite elegir y comparar entre Google Gemini y Hugging Face (Mistral-7B).

***

## 📐 Arquitectura del Sistema

```
Usuario → Filtro Seguridad → Agente ReAct (LangChain, Multi-LLM) → Herramientas (Calculadora, FAQ, Reglamentos) → Respuesta Final
```
Patrón principal: **Percepción → Decisión → Acción**

***

## 📦 Estructura del Proyecto

```
TP final IA/
├── src/
│   ├── agent.py         # Configura y orquesta el agente
│   ├── main.py          # Entrada interactiva
│   └── tools/
│       ├── calculadora.py
│       └── buscador.py
├── data/
│   ├── faq.json
│   └── reglamentos.txt
├── notebooks/
├── .env                 # Claves de API (IGNORADO EN GIT)
├── .gitignore
├── requirements.txt
└── README.md
```

***

## 🛠️ Tecnologías Utilizadas

- Python 3.10+
- LangChain (Orquestación de agentes)
- Hugging Face (Mistral-7B-Instruct-v0.2)
- Google Gemini (gemini-2.5-flash)
- Sentence-Transformers + FAISS (embeddings y búsqueda semántica)
- dotenv (configuración segura de API keys)

***

### APIs Necesarias

Para usar el selector de LLM, necesitarás al menos una de estas claves:

1. **Google Gemini API** (Recomendado - Gratis)
   - Registro: [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Modelo usado: `gemini-2.5-flash`

2. **Hugging Face API** (Alternativa)
   - Registro: [Hugging Face](https://huggingface.co/settings/tokens)
   - Modelo usado: `mistralai/Mistral-7B-Instruct-v0.2`

***

## 🚀 Instalación Rápida

1. Clonar el repositorio:
    ```bash
    git clone https://github.com/TitaniaWagic/Agente-conversacional-para-asistencia-academica-con-herramientas.git
    cd "TP final IA"
    ```
2. Crear entorno virtual y activarlo:
    - Windows: `python -m venv venv && .\venv\Scripts\Activate.ps1`
    - Linux/Mac: `python3 -m venv venv && source venv/bin/activate`
3. Instalar dependencias:
    ```bash
    pip install -r requirements.txt
    ```
4. Añadir tu archivo `.env` con los tokens de API (Ver ejemplos en Configuración).

***

## ⚙️ Configuración de Datos y Proveedores

- **.env (Ejemplo):**
    ```
    GOOGLE_API_KEY=tu_clave_de_google
    HUGGINGFACEHUB_API_TOKEN=tu_token_de_huggingface
    ```
- **FAQ (`data/faq.json`):**
    ```json
    [
      {"pregunta": "¿Cuál es el correo de soporte técnico?", "respuesta": "El correo es soporte.ti@une.edu.py"}
    ]
    ```
- **Reglamento (`data/reglamentos.txt`):** Añade tu texto completo.

- **Configuración de Proveedor de LLM:** En `src/agent.py`, cambia la línea:
    ```python
    LLM_PROVIDER = "GOOGLE"  # O "HUGGINGFACE"
    ```

***

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

***

## 🖥️ Uso Interactivo

Ejecuta el agente académico en la terminal:
```bash
python -m src.main
```

### 💡 Ejemplos de Consultas

#### 1. Convertir Porcentaje a Nota 🆕
```
Usuario: ¿Qué nota tengo si tengo un 75%?

Agente:
📊 CONVERSIÓN DE PORCENTAJE A NOTA (Art. 90)
==================================================

Porcentaje obtenido: 75.0%
Nota correspondiente: 3 (70% - 80%)
Estado: ✅ APROBADO

📋 Sistema de Calificaciones:
   • Nota 1: 0% - 59% (Reprobado)
   • Nota 2: 60% - 69% (Aprobado - mínimo)
   • Nota 3: 70% - 80% (Aprobado)
   • Nota 4: 81% - 93% (Muy bueno)
   • Nota 5: 94% - 100% (Excelente)
```

#### 2. Calcular Promedio de Notas
```
Usuario: ¿Cuál es el promedio de 85, 90 y 78?
Agente: El promedio de las notas [85.0, 90.0, 78.0] es: 84.33
```

#### 3. Calcular Nota para Aprobar
```
Usuario: Tengo primera parcial 80, segunda parcial 75, trabajo practico 90, trabajo laboratorio 0, opcion A. ¿Qué necesito en el final para aprobar?

Agente: 
📊 CÁLCULO DE NOTAS - Opción A
==================================================

📝 Evaluaciones Parciales (40% del total):
   • Primera Parcial (15%): 80% = 12.00 puntos
   • Segunda Parcial (20%): 75% = 15.00 puntos
   • Trabajo Práctico (5%): 90% = 4.50 puntos
   • Trabajo Laboratorio (0%): 0% = 0.00 puntos
   
   Total Parciales: 31.50/40 puntos (78.75%)

🎓 Estado de Exoneración:
   ❌ No exonerado. Necesitas 15.25% más para exonerar.

📋 Examen Final (60% del total):
   Para APROBAR (nota 2 = 60% del total):
   Necesitas: 47.50% en el examen final
   
   Para nota 3 (70% del total):
   Necesitas: 64.17% en el examen final
```

#### 4. Verificar Exoneración
```
Usuario: Primera parcial 95, segunda parcial 98, trabajo practico 100, trabajo laboratorio 0, opcion A. ¿Puedo exonerar?

Agente: 
✅ ¡FELICITACIONES! Ya has exonerado el examen final.
   
   Puntos obtenidos: 37.65/40 (94.13%)
   Puntos necesarios para exonerar: 37.60/40 (94%)
   
   No necesitas rendir el examen final. ¡Bien hecho! 🎉
```

#### 5. Verificar Riesgo de Cancelación de Matrícula
```
Usuario: Tengo 15 aplazos de 50 materias. ¿Estoy en riesgo?

Agente:
✅ Estado Normal
==================================================

Tienes 15 aplazos de 50 materias (30.0%).
Límite permitido: 15 aplazos (30% del plan).

Aplazos disponibles: 0

⚠️ ¡ATENCIÓN! Has alcanzado exactamente el límite.
No puedes acumular más aplazos sin consecuencias.
```

#### 6. Verificar Estado en una Materia
```
Usuario: He sido aplazado 2 veces en esta materia. ¿Qué pasa si repruebo de nuevo?

Agente:
⚠️ ADVERTENCIA - Última Oportunidad
==================================================

Has sido aplazado 2 veces en esta asignatura.

⚠️ Este es tu ÚLTIMO intento antes de tener que recursar.

Si vuelves a reprobar:
- Deberás cursar la materia nuevamente
- Tendrás que cumplir todos los requisitos otra vez

¡Prepárate bien para este examen!
```

#### 7. Consultar Reglamentos
```
Usuario: ¿Cómo funciona el sistema de calificaciones?

Agente: Según el Art. 90, las calificaciones van del 1 al 5:
- 1 (0-59%)
- 2 (60-69%) - Nota mínima para aprobar
- 3 (70-80%)
- 4 (81-93%)
- 5 (94-100%)
```

### 📚 Opciones de Evaluación

El sistema soporta tres opciones de distribución de porcentajes:

**Opción A:**
- Primera Parcial: 15%
- Segunda Parcial: 20%
- Trabajo Práctico: 5%
- Trabajo en Laboratorio: 0%
- Examen Final: 60%

**Opción B:**
- Primera Parcial: 10%
- Segunda Parcial: 20%
- Trabajo Práctico: 5%
- Trabajo en Laboratorio: 5%
- Examen Final: 60%

**Opción C:**
- Primera Parcial: 10%
- Segunda Parcial: 20%
- Trabajo Práctico: 0%
- Trabajo en Laboratorio: 10%
- Examen Final: 60%

### 📋 Artículos Implementados

- **Art. 70**: Restricción por 3 aplazos en la misma asignatura
- **Art. 71**: Cancelación automática de matrícula por 30% de aplazos
- **Art. 90**: Sistema de calificaciones (1-5)

Prueba también los notebooks en la carpeta `/notebooks` para ver ejemplos, casos de prueba y validar exactitud y cobertura de las herramientas.

***

## 📝 Pruebas y Evaluación

El proyecto incluye notebooks de pruebas funcionales para:
- Calculadora académica
- Buscador de FAQ
- Buscador semántico de reglamentos
- Simulación de preguntas bloqueadas y manejo de errores

**Métricas propuestas:**
- Exactitud de respuesta ≥80% en sets de prueba.
- Cobertura de FAQ ≥85%.
- Satisfacción simulada (Likert ≥4/5).

***

## 🔍 Troubleshooting

- Si hay problemas con dependencias, verifica que tienes las versiones correctas en `requirements.txt` y que el `.env` está bien ubicado.
- Si tienes errores de API, verifica y renueva claves y tokens.
- La búsqueda semántica depende de la calidad y estructura de los reglamentos.

***

## 🤝 Contribuir

Ideas para mejorar el proyecto:
- Nuevas herramientas (clima, registros).
- Soporte de multiidioma y dashboard visual.
- Más tests unitarios.
- Mejor documentación y ejemplos de uso.

***

## Referencias y Recursos

- [Documentación de LangChain](https://python.langchain.com/)
- [Google Gemini API Docs](https://ai.google.dev/)
- [Hugging Face Inference API](https://huggingface.co/docs/api-inference/)
- [FAISS Documentation](https://github.com/facebookresearch/faiss)
- [Sentence-Transformers](https://www.sbert.net/)

***

## 📜 Licencia

MIT License.

***

## 🚩 Autor y Créditos

Desarrollado para la cátedra **Inteligencia Artificial I**.  
Agradecimientos a LangChain, Hugging Face, Google Gemini y colaboraciones abiertas.  
Contribuciones y sugerencias siempre son bienvenidas.

***

<div align="center">

⭐ **Si te fue útil, dale estrella en GitHub!** ⭐  
Made with ❤️ and 🤖

</div>

[1](https://educacion.bilateria.org/como-evaluar-proyectos-en-grupo-con-inteligencia-artificial)
[2](https://edtk.co/rbk/337881)
[3](https://educa.fme.cl/wp-content/uploads/2025/07/Proyectos-Educativos-con-IA.pdf)
[4](https://www.python.org)
