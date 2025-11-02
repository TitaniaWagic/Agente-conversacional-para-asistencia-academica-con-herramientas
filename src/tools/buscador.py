import json
from pathlib import Path  # Importamos la clase Path
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

def buscar_en_faq(consulta: str) -> str:
    """
    Busca una respuesta en el archivo faq.json basado en palabras clave.
    """
    # ruta absoluta al archivo JSON 
    ruta_faq = Path(__file__).resolve().parent.parent.parent / "data" / "faq.json"
    
    with open(ruta_faq, 'r', encoding='utf-8') as f:
        faqs = json.load(f)
    
    palabras_consulta = set(consulta.lower().split())
    
    for item in faqs:
        palabras_pregunta = set(item["pregunta"].lower().split())
        if len(palabras_consulta.intersection(palabras_pregunta)) >= 2:
            return item["respuesta"]
            
    return "No encontré una respuesta directa en las preguntas frecuentes."

class BuscadorLocal:
    """
    Una clase para manejar la búsqueda semántica en documentos locales.
    """
    def __init__(self, file_path: Path): #  Aceptamos un objeto Path
        loader = TextLoader(str(file_path), encoding='utf-8') # Convertimos Path a string para el loader
        documents = loader.load()
        
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        docs = text_splitter.split_documents(documents)
        
        embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        
        self.db = FAISS.from_documents(docs, embeddings)

    def buscar(self, query: str) -> str:
        """
        Realiza una búsqueda de similitud en la base de datos vectorial.
        """
        resultados = self.db.similarity_search(query, k=1)
        if resultados:
            return resultados[0].page_content
        return "No encontré información sobre eso en los reglamentos."

# ruta absoluta al archivo de reglamentos
# Path(__file__) -> el archivo actual (buscador.py)
# .resolve()     -> convierte a ruta completa (C:\Users\...)
# .parent        -> sube a la carpeta /tools
# .parent        -> sube a la carpeta /src
# .parent        -> sube a la carpeta raíz del proyecto
# / "data" / "reglamentos.txt" -> añade el resto de la ruta
ruta_reglamentos = Path(__file__).resolve().parent.parent.parent / "data" / "reglamentos.txt"

# instancia con la ruta correcta
buscador_de_reglamentos = BuscadorLocal(ruta_reglamentos)