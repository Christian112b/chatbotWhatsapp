from .data import *

def limpiar_telefono(tel):
    solo_digitos = ''.join(filter(str.isdigit, tel))
    return solo_digitos[-10:]

def respuesta_menu_precio(mensaje):
    mensaje = mensaje.lower()

    if any(precio in mensaje for precio in precio_keywords):
        return menu_precios, "menu_precios"
    
    elif any(clase in mensaje for clase in clase_keywords):
        return "Esta respuesta es de clase", "menu_clase"

    elif any(insc in mensaje for insc in inscripcion_keywords):
        return "¡Excelente! Por favor indica el número del plan (1-3) parainiciar tu inscripción.", "menu_inscripcion"

    else:
        return "Lo siento, no entiendo tu solicitud, intentalo de nuevo.", "Inicio"

def respuesta_confirmacion(mensaje):
    mensaje = mensaje.lower()

    if any(opcion in mensaje for opcion in menu_precios_opcion_clase):
        return "¡Genial! Para agendar tu clase de prueba, por favor visita nuestro sitio web o contáctanos directamente al número +52 123 456 7890. ¡Te esperamos!", "Inicio"
    elif any(opcion in mensaje for opcion in menu_precios_informacion):
        return "¡Claro! Para más información sobre nuestros precios y clases, por favor visita nuestro sitio web o contáctanos directamente al número +52 123 456 7890. ¡Estamos aquí para ayudarte!", "Inicio"
    elif any(opcion in mensaje for opcion in no_acepto_keywords):
        return "Entiendo, si cambias de opinión o tienes alguna otra pregunta, no dudes en contactarnos. ¡Que tengas un excelente día!", "Inicio"
    else:
        return "Lo siento, no entiendo tu solicitud, intentalo de nuevo.", "Inicio"
    
def seleccion_plan(mensaje):
    mensaje = mensaje.lower()
    match = re.search(r"\b(\d+)\b", mensaje)
    if match:
        num_plan = int(match.group(1))
        if 1 <= num_plan <= len(planes):
            return (
                f"¡Perfecto! Has elegido el plan {num_plan}: {planes[num_plan-1]}\n"
                "Por favor indícame tu nombre completo para finalizar la inscripción.",
                "confirmacion", num_plan
            )
        else:
            return (
                f"No existe el plan número {num_plan}. Por favor responde con un número entre 1 y {len(planes)}.",
                "menu_inscripcion", None
            )
    else:
        return (
            f"No pude identificar el número del plan. Por favor responde solo con un número entre 1 y {len(planes)}.",
            "menu_inscripcion", None
        )
    
def confirmacion(nombre, plan, telefono):
    
    return (
        f"{nombre}, con numero: {telefono}, elegiste el {plan}.\n"
        "¿Deseas confirmar tu inscripción?\n"
        "Responde con 'confirmar' para continuar o 'cancelar' para detener el proceso.",
        "esperando_confirmacion"
    )

def esperando_confirmacion(mensaje):
    if "confirmar" in mensaje:
        return (
            "¡Perfecto! Tu inscripción ha sido confirmada.\n"
            "Si tienes alguna pregunta, no dudes en contactarnos.",
            "Inicio"
        )
    elif "cancelar" in mensaje:
        return (
            "Tu inscripción ha sido cancelada.\n"
            "Si cambias de opinión, aquí estaremos.",
            "Inicio"
        )
    else:
        return (
            "Lo siento, no entiendo tu respuesta.\n"
            "Por favor responde con 'confirmar' o 'cancelar'.",
            "esperando_confirmacion"
        )