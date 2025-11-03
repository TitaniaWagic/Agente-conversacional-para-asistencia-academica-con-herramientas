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
- **Calculadora Académica**: Extrae notas de texto natural y calcula el promedio.
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

## 🖥️ Uso Interactivo

Ejecuta el agente académico en la terminal:
```bash
python -m src.main
```

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

## 🏆 Referencias y Marco Teórico

Consulta sobre el estado del arte, orquestación de herramientas y justificación académica en los apartados teóricos y referencias del repositorio.[2][3][1]

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
