saludos = [
    "hola", "buenas", "buenos días", "buenas tardes", "buenas noches",
    "hey", "qué tal", "saludos", "holi", "hello", "hi", "buen dia"
]

agradecimientos = [
    "gracias", "muchas gracias", "mil gracias", "te agradezco",
    "gracias por tu ayuda"
]

despedidas = [
    "adiós", "nos vemos", "bye", "hasta luego",
    "chau", "me voy", "saludos", "hasta mañana"
]

respuestas = {
    "saludo": 
        "Hola, bienvenido al Club Deportivo [Nombre del Club].\n\n"
        "Estoy aquí para ayudarte. Puedes preguntarme sobre:\n"
        "1. Horarios de atención\n"
        "2. Precios y promociones\n"
        "3. Clases disponibles (funcional, spinning, yoga, etc.)\n"
        "4. Ubicación del club\n"
        "5. Cómo inscribirte\n"
        "6. Medidas de higiene y seguridad\n\n"
        "Escríbeme lo que necesitas o selecciona una opción para comenzar.",
        
    "despedida": "¡Adiós! Que tengas un buen día.",
    "agradecimiento": "¡De nada! Si necesitas algo más, no dudes en preguntar.",
    "desconocido": "Lo siento, no entendí tu mensaje. ¿Podrías reformularlo?"
}

def clasificacion_mensaje(mensaje):
    mensaje = mensaje.lower()
    if any(saludo in mensaje for saludo in saludos):
        return respuestas["saludo"]
    elif any(despedida in mensaje for despedida in despedidas):
        return respuestas["despedida"]
    elif any(agradecimiento in mensaje for agradecimiento in agradecimientos):
        return respuestas["agradecimiento"]
    else:
        return respuestas["desconocido"]

def contieneSaludo(mensaje):
    return any(saludo in mensaje.lower() for saludo in saludos)

def contieneDespedida(mensaje):
    return any(despedida in mensaje.lower() for despedida in despedidas)

def contieneAgradecimiento(mensaje):
    return any(agradecimiento in mensaje.lower() for agradecimiento in agradecimientos)