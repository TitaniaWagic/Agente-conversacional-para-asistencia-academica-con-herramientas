# En src/tools/calculadora.py
import re

def calcular_promedio_de_notas(texto_con_notas: str) -> str:
    """
    Extrae todos los números de un string, los convierte a flotantes
    y calcula su promedio.
    Devuelve un string con el resultado o un mensaje de error.
    """
    # Usamos expresiones regulares para encontrar todos los números (enteros o decimales)
    numeros_encontrados = re.findall(r'\d+\.?\d*', texto_con_notas)
    
    if not numeros_encontrados:
        return "No encontré números en tu pregunta para calcular el promedio."

    try:
        # Convertimos los strings encontrados a números flotantes
        notas = [float(num) for num in numeros_encontrados]
        
        # Calculamos el promedio
        promedio = sum(notas) / len(notas)
        
        return f"El promedio de las notas {notas} es: {promedio:.2f}"
    except ValueError:
        return "Hubo un error al procesar los números."