saludos = [
    "hola", "buenas", "buenos días", "buenas tardes", "buenas noches",
    "hey", "qué tal", "saludos", "holi", "hello", "hi", "qué onda"
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
    "saludo": "¡Hola! ¿Cómo puedo ayudarte hoy?",
    "despedida": "¡Adiós! Que tengas un buen día.",
    "agradecimiento": "¡De nada! Si necesitas algo más, no dudes en preguntar.",
    "desconocido": "Lo siento, no entendí tu mensaje. Por favor, escribe 'hola' o 'adiós'."
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