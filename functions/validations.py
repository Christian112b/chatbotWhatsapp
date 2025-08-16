from .data import *

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

def respuesta_menu_precio(mensaje):
    mensaje = mensaje.lower()

    if any(precio in mensaje for precio in precio_keywords):
        return menu_precios, "precios"
    elif any(clase in mensaje for clase in ["clases", "inscripción"]):
        return respuestas["respuesta_clases_inscripcion"], 200
    elif any(inscripcion in mensaje for inscripcion in ["inscripción", "inscribirme"]):
        return respuestas["respuesta_inscripcion"], 200
    else:
        return "Lo siento, no entiendo tu solicitud, intentalo de nuevo.", 400

def respuesta_confirmacion(mensaje):
    mensaje = mensaje.lower()

    if any(opcion in mensaje for opcion in menu_precios_opcion_clase):
        return "¡Genial! Para agendar tu clase de prueba, por favor visita nuestro sitio web o contáctanos directamente al número +52 123 456 7890. ¡Te esperamos!", "agendar"
    elif any(opcion in mensaje for opcion in menu_precios_informacion):
        return "¡Claro! Para más información sobre nuestros precios y clases, por favor visita nuestro sitio web o contáctanos directamente al número +52 123 456 7890. ¡Estamos aquí para ayudarte!", "mas informacion"
    elif any(opcion in mensaje for opcion in no_acepto_keywords):
        return "Entiendo, si cambias de opinión o tienes alguna otra pregunta, no dudes en contactarnos. ¡Que tengas un excelente día!", "no acepto"
    else:
        return "Lo siento, no entiendo tu solicitud, intentalo de nuevo."