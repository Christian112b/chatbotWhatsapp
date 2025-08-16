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

    if any(precio in mensaje for precio in respuesta_menu_precio):
        return menu_precios, "precios"
    elif any(clase in mensaje for clase in ["clases", "inscripción"]):
        return respuestas["respuesta_clases_inscripcion"], 200
    elif any(inscripcion in mensaje for inscripcion in ["inscripción", "inscribirme"]):
        return respuestas["respuesta_inscripcion"], 200
    else:
        return "Lo siento, no entiendo tu solicitud, intentalo de nuevo.", 400
