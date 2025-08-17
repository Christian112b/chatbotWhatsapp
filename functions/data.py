menu_bienvenida = (
    "Hola, gracias por escribir al Club Deportivo. ¿Qué te interesa saber: precios, clases o cómo inscribirte?"
)

menu_no_inscritos = (
    "¿Te gustaría saber más sobre nuestros planes, clases o cómo inscribirte?"
)

precio_keywords = [
    "cuesta", "precios", "tarifas", "costo", "mensualidad", "precio"
]

clase_keywords = [
    "clase", "clases", 
]

inscripcion_keywords = [
    "inscripcion", "inscribirme", "inscribir", "registrar", "registro", "alta"
]


acepto_keywords = [
    "me gustaria", "claro", "por supuesto", "acepto", 
    "de acuerdo", "ok"
]

no_acepto_keywords = [
    "no", "no quiero", "no me interesa", "no gracias", "rechazo", "prefiero no", 
    "no por ahora", "no deseo", "no acepto", "no estoy seguro", "no puedo", 
    "no es posible", "no me gusta", "no funciona", "no aplica", "no lo haré"
]

menu_precios_opcion_clase = [
    "agendar", "clase prueba", "clase", "reservar", "probar clase", 
    "quiero clase", "quiero agendar", "quiero reservar", "inscribirme", 
    "inscripción", "clase de prueba"
]

menu_precios_informacion = [
    "mas informacion", "info", "detalles", "informacion", "dime mas",
    "saber mas"
]

menu_precios = """
    Estos son nuestros planes disponibles:\n
    1. Plan mensual general: $500 MXN
       - Acceso ilimitado al gimnasio
       - Clases grupales incluidas\n
    2. Plan personalizado: $750 MXN
       - Entrenamiento individual
       - Seguimiento nutricional\n
    3. Clase individual: $100 MXN
       - Ideal para probar una sesión específica\n
    4. Promoción actual:
       - Inscríbete esta semana y recibe una clase personalizada gratis\n\n
    ¿Te gustaría agendar una clase de prueba o recibir más información?
    """

planes = [
    "1. Plan mensual general: $500 MXN",
    "2. Plan personalizado: $750 MXN",
    "3. Clase individual: $100 MXN"
]


respuestas = {
    "saludo": 
        "Hola, bienvenido a Club Forma.\n\n"
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
    "desconocido": "Lo siento, no entendí tu mensaje. ¿Podrías reformularlo?",
    "respuesta_precios": "Aquí tienes la información sobre precios..."
}   



# Opciones para gente ya inscrita y activa
bienvenido_activo = (
    "Bienvenido nuevamente al Club Deportivo. ¿Deseas ver los detalles de tu plan o agendar una clase?"
)

planes_keyword = [
    "detalles", "plan", "planes", "informacion"
    ]

agendar_keyword = [
    "agendar", "clase prueba", "clase", "reservar", "clase", 
    "agendar", "reservar", "clase de prueba"
    ]





# ----------------------------------------------


bienvenido_no_activo = (
    "Lo sentimos, no estás activo en el club. ¿Te gustaría reactivar tu membresía o saber más sobre nuestros planes?"
)
