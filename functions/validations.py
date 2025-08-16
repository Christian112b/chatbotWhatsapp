from .data import *

def respuesta_menu_precio(mensaje):
    mensaje = mensaje.lower()

    if any(precio in mensaje for precio in precio_keywords):
        return menu_precios, "menu_precios"
    
    elif any(clase in mensaje for clase in clase_keywords):
        return respuestas["respuesta_clases_inscripcion"], "menu_clase"

    elif any(insc in mensaje for insc in inscripcion_keywords):
        return respuestas["respuesta_clases_inscripcion"], "menu_inscripcion"

    else:
        return "Lo siento, no entiendo tu solicitud, intentalo de nuevo.", 400

def respuesta_confirmacion(mensaje):
    mensaje = mensaje.lower()

    if any(opcion in mensaje for opcion in menu_precios_opcion_clase):
        return "¡Genial! Para agendar tu clase de prueba, por favor visita nuestro sitio web o contáctanos directamente al número +52 123 456 7890. ¡Te esperamos!"
    elif any(opcion in mensaje for opcion in menu_precios_informacion):
        return "¡Claro! Para más información sobre nuestros precios y clases, por favor visita nuestro sitio web o contáctanos directamente al número +52 123 456 7890. ¡Estamos aquí para ayudarte!"
    elif any(opcion in mensaje for opcion in no_acepto_keywords):
        return "Entiendo, si cambias de opinión o tienes alguna otra pregunta, no dudes en contactarnos. ¡Que tengas un excelente día!"
    else:
        return "Lo siento, no entiendo tu solicitud, intentalo de nuevo."