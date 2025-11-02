from src.agent import crear_agente, filtro_de_seguridad

def main():
    print("¡Hola! Soy tu asistente académico. ¿En qué puedo ayudarte?")
    print("Escribe 'salir' para terminar la conversación.")
    
    # Creamos una instancia del agente
    agente = crear_agente()
    
    while True:
        try:
            # Pedimos la entrada del usuario
            consulta_usuario = input("\nTú: ")
            
            if consulta_usuario.lower() == 'salir':
                print("Asistente: ¡Hasta luego! Que tengas un buen día.")
                break
            
            # Aplicamos el filtro de seguridad
            if not filtro_de_seguridad(consulta_usuario):
                print("Asistente: Lo siento, no puedo responder a esa solicitud por políticas de la institución.")
                continue
            
            # Invocamos al agente con la consulta
            respuesta = agente.invoke({"input": consulta_usuario})
            
            # Imprimimos la respuesta final
            print(f"Asistente: {respuesta['output']}")

        except Exception as e:
            print(f"Ha ocurrido un error inesperado: {e}")

if __name__ == "__main__":
    main()