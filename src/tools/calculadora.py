# En src/tools/calculadora.py
import re

def convertir_porcentaje_a_nota(porcentaje: float) -> str:
    """
    Convierte un porcentaje a una nota según el sistema de calificaciones del Art. 90.
    
    Args:
        porcentaje: Porcentaje obtenido (0-100)
    
    Returns:
        String con la nota correspondiente y su rango
    """
    if porcentaje < 0 or porcentaje > 100:
        return "Error: El porcentaje debe estar entre 0 y 100."
    
    if porcentaje < 60:
        nota = 1
        rango = "0% - 59%"
        estado = "❌ REPROBADO"
    elif porcentaje < 70:
        nota = 2
        rango = "60% - 69%"
        estado = "✅ APROBADO (mínimo)"
    elif porcentaje < 81:
        nota = 3
        rango = "70% - 80%"
        estado = "✅ APROBADO"
    elif porcentaje < 94:
        nota = 4
        rango = "81% - 93%"
        estado = "✅ APROBADO (muy bueno)"
    else:
        nota = 5
        rango = "94% - 100%"
        estado = "✅ EXCELENTE"
    
    return f"""
📊 CONVERSIÓN DE PORCENTAJE A NOTA (Art. 90)
{'='*50}

Porcentaje obtenido: {porcentaje}%
Nota correspondiente: {nota} ({rango})
Estado: {estado}

📋 Sistema de Calificaciones:
   • Nota 1: 0% - 59% (Reprobado)
   • Nota 2: 60% - 69% (Aprobado - mínimo)
   • Nota 3: 70% - 80% (Aprobado)
   • Nota 4: 81% - 93% (Muy bueno)
   • Nota 5: 94% - 100% (Excelente)
"""

def calcular_promedio_de_notas(texto_con_notas: str) -> str:
    """
    Extrae todos los números de un string, los convierte a flotantes
    y calcula su promedio.
    Devuelve un string con el resultado o un mensaje de error.
    """
    # expresiones regulares para encontrar todos los números (enteros o decimales)
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


def calcular_nota_para_aprobar(primera_parcial: float, segunda_parcial: float, 
                                trabajo_practico: float, trabajo_laboratorio: float, 
                                opcion: str = "A") -> str:
    """
    Calcula qué nota necesita un estudiante en el examen final para aprobar la materia.
    
    Args:
        primera_parcial: Nota de la primera parcial (0-100)
        segunda_parcial: Nota de la segunda parcial (0-100)
        trabajo_practico: Nota del trabajo práctico (0-100)
        trabajo_laboratorio: Nota del trabajo en laboratorio (0-100)
        opcion: Opción de distribución de porcentajes ("A", "B", o "C")
    
    Returns:
        String con el cálculo detallado
    """
    # Definir los porcentajes según la opción
    opciones = {
        "A": {"pp1": 15, "pp2": 20, "tp": 5, "tl": 0, "final": 60},
        "B": {"pp1": 10, "pp2": 20, "tp": 5, "tl": 5, "final": 60},
        "C": {"pp1": 10, "pp2": 20, "tp": 0, "tl": 10, "final": 60}
    }
    
    if opcion.upper() not in opciones:
        return "Opción inválida. Debe ser A, B o C."
    
    porcentajes = opciones[opcion.upper()]
    
    # Calcular puntos obtenidos en las evaluaciones parciales
    puntos_pp1 = (primera_parcial / 100) * porcentajes["pp1"]
    puntos_pp2 = (segunda_parcial / 100) * porcentajes["pp2"]
    puntos_tp = (trabajo_practico / 100) * porcentajes["tp"]
    puntos_tl = (trabajo_laboratorio / 100) * porcentajes["tl"]
    
    puntos_parciales = puntos_pp1 + puntos_pp2 + puntos_tp + puntos_tl
    porcentaje_parcial = (puntos_parciales / 40) * 100
    
    # Verificar si puede exonerar (94% o más en el 40%)
    puede_exonerar = porcentaje_parcial >= 94
    
    # Calcular nota necesaria en el final para aprobar (60% del total)
    # Para aprobar necesita 60% del total (nota 2)
    puntos_necesarios_aprobar = 60 - puntos_parciales
    porcentaje_final_aprobar = (puntos_necesarios_aprobar / 60) * 100
    
    resultado = f"""
📊 CÁLCULO DE NOTAS - Opción {opcion.upper()}
{'='*50}

📝 Evaluaciones Parciales (40% del total):
   • Primera Parcial ({porcentajes['pp1']}%): {primera_parcial}% = {puntos_pp1:.2f} puntos
   • Segunda Parcial ({porcentajes['pp2']}%): {segunda_parcial}% = {puntos_pp2:.2f} puntos
   • Trabajo Práctico ({porcentajes['tp']}%): {trabajo_practico}% = {puntos_tp:.2f} puntos
   • Trabajo Laboratorio ({porcentajes['tl']}%): {trabajo_laboratorio}% = {puntos_tl:.2f} puntos
   
   Total Parciales: {puntos_parciales:.2f}/40 puntos ({porcentaje_parcial:.2f}%)

🎓 Estado de Exoneración:
   {'✅ ¡EXONERADO! Has alcanzado el 94% o más en las parciales.' if puede_exonerar else f'❌ No exonerado. Necesitas {94 - porcentaje_parcial:.2f}% más para exonerar.'}

📋 Examen Final (60% del total):
   Para APROBAR (nota 2 = 60% del total):
   {'   Ya estás aprobado con las parciales.' if puntos_parciales >= 60 else f'   Necesitas: {max(0, porcentaje_final_aprobar):.2f}% en el examen final'}
   
   Para nota 3 (70% del total):
   Necesitas: {max(0, ((70 - puntos_parciales) / 60) * 100):.2f}% en el examen final
   
   Para nota 4 (81% del total):
   Necesitas: {max(0, ((81 - puntos_parciales) / 60) * 100):.2f}% en el examen final
   
   Para nota 5 (94% del total):
   Necesitas: {max(0, ((94 - puntos_parciales) / 60) * 100):.2f}% en el examen final

💡 Nota: Si el porcentaje necesario es mayor a 100%, no es posible alcanzar esa nota final.
"""
    
    return resultado


def calcular_nota_para_exonerar(primera_parcial: float, segunda_parcial: float, 
                                 trabajo_practico: float, trabajo_laboratorio: float, 
                                 opcion: str = "A") -> str:
    """
    Calcula qué nota necesita un estudiante para exonerar el examen final.
    
    Args:
        primera_parcial: Nota de la primera parcial (0-100)
        segunda_parcial: Nota de la segunda parcial (0-100)
        trabajo_practico: Nota del trabajo práctico (0-100)
        trabajo_laboratorio: Nota del trabajo en laboratorio (0-100)
        opcion: Opción de distribución de porcentajes ("A", "B", o "C")
    
    Returns:
        String con el cálculo detallado
    """
    opciones = {
        "A": {"pp1": 15, "pp2": 20, "tp": 5, "tl": 0},
        "B": {"pp1": 10, "pp2": 20, "tp": 5, "tl": 5},
        "C": {"pp1": 10, "pp2": 20, "tp": 0, "tl": 10}
    }
    
    if opcion.upper() not in opciones:
        return "Opción inválida. Debe ser A, B o C."
    
    porcentajes = opciones[opcion.upper()]
    
    # Calcular puntos obtenidos
    puntos_pp1 = (primera_parcial / 100) * porcentajes["pp1"]
    puntos_pp2 = (segunda_parcial / 100) * porcentajes["pp2"]
    puntos_tp = (trabajo_practico / 100) * porcentajes["tp"]
    puntos_tl = (trabajo_laboratorio / 100) * porcentajes["tl"]
    
    puntos_totales = puntos_pp1 + puntos_pp2 + puntos_tp + puntos_tl
    porcentaje_actual = (puntos_totales / 40) * 100
    
    # Para exonerar necesita 94% del 40%
    puntos_necesarios = 40 * 0.94
    
    if puntos_totales >= puntos_necesarios:
        return f"""
✅ ¡FELICITACIONES! Ya has exonerado el examen final.
   
   Puntos obtenidos: {puntos_totales:.2f}/40 ({porcentaje_actual:.2f}%)
   Puntos necesarios para exonerar: {puntos_necesarios:.2f}/40 (94%)
   
   No necesitas rendir el examen final. ¡Bien hecho! 🎉
"""
    else:
        puntos_faltantes = puntos_necesarios - puntos_totales
        return f"""
📊 CÁLCULO PARA EXONERAR - Opción {opcion.upper()}
{'='*50}

Estado actual:
   Puntos obtenidos: {puntos_totales:.2f}/40 ({porcentaje_actual:.2f}%)
   Puntos necesarios: {puntos_necesarios:.2f}/40 (94%)
   
❌ Aún no alcanzas la exoneración.
   Te faltan: {puntos_faltantes:.2f} puntos ({(puntos_faltantes/40)*100:.2f}%)
   
💡 Tendrás que rendir el examen final (60% del total).
"""


def verificar_riesgo_cancelacion_matricula(aplazos: int, total_materias_plan: int) -> str:
    """
    Verifica si un estudiante está en riesgo de cancelación de matrícula según el Art. 71.
    
    Args:
        aplazos: Número de aplazos acumulados durante la carrera
        total_materias_plan: Número total de materias en el plan de estudios
    
    Returns:
        String con el análisis del riesgo
    """
    porcentaje_aplazos = (aplazos / total_materias_plan) * 100
    limite_aplazos = int(total_materias_plan * 0.30)
    aplazos_disponibles = limite_aplazos - aplazos
    
    if aplazos >= limite_aplazos:
        return f"""
⚠️ ALERTA CRÍTICA - Art. 71
{'='*50}

❌ MATRÍCULA CANCELADA

Has acumulado {aplazos} aplazos de {total_materias_plan} materias ({porcentaje_aplazos:.1f}%).
Límite permitido: {limite_aplazos} aplazos (30% del plan de estudios).

Según el Artículo 71, tu matrícula ha sido cancelada automática y definitivamente.
Debes contactar a la secretaría académica para más información.
"""
    elif porcentaje_aplazos >= 20:
        return f"""
⚠️ ADVERTENCIA - Riesgo Alto
{'='*50}

Tienes {aplazos} aplazos de {total_materias_plan} materias ({porcentaje_aplazos:.1f}%).
Límite permitido: {limite_aplazos} aplazos (30% del plan).

⚠️ Estás cerca del límite. Solo te quedan {aplazos_disponibles} aplazos disponibles.

Recomendaciones:
- Planifica cuidadosamente tus estudios
- Busca apoyo académico si lo necesitas
- Considera recursar materias en las que tengas dificultades
"""
    else:
        return f"""
✅ Estado Normal
{'='*50}

Tienes {aplazos} aplazos de {total_materias_plan} materias ({porcentaje_aplazos:.1f}%).
Límite permitido: {limite_aplazos} aplazos (30% del plan).

Aplazos disponibles: {aplazos_disponibles}

Mantén un buen rendimiento académico para evitar complicaciones futuras.
"""


def verificar_estado_asignatura(aplazos_asignatura: int) -> str:
    """
    Verifica el estado de un estudiante en una asignatura específica según el Art. 70.
    
    Args:
        aplazos_asignatura: Número de veces que ha sido aplazado en la misma asignatura
    
    Returns:
        String con el estado y las restricciones
    """
    if aplazos_asignatura >= 3:
        return f"""
⚠️ RESTRICCIÓN APLICADA - Art. 70
{'='*50}

❌ Has sido aplazado {aplazos_asignatura} veces en esta asignatura.

Según el Artículo 70:
No podrás presentarte a otra evaluación final sin antes:
1. Volver a cursar la asignatura
2. Satisfacer nuevamente todos los requisitos exigidos

Debes inscribirte nuevamente en la materia para poder rendirla.
"""
    elif aplazos_asignatura == 2:
        return f"""
⚠️ ADVERTENCIA - Última Oportunidad
{'='*50}

Has sido aplazado {aplazos_asignatura} veces en esta asignatura.

⚠️ Este es tu ÚLTIMO intento antes de tener que recursar.

Si vuelves a reprobar:
- Deberás cursar la materia nuevamente
- Tendrás que cumplir todos los requisitos otra vez

¡Prepárate bien para este examen!
"""
    else:
        return f"""
✅ Estado: {aplazos_asignatura} aplazo(s) en esta asignatura

Oportunidades restantes: {3 - aplazos_asignatura}

{' Mantén el esfuerzo y prepárate bien.' if aplazos_asignatura == 0 else 'Considera buscar apoyo académico si tienes dificultades.'}
"""