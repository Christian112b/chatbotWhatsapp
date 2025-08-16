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

precio_keywords = [
    "Cuesta", "precios", "tarifas", "costo", "mensualidad", "precio"
]

menu_precios = """
    Estos son nuestros planes disponibles:\n\n
    1. Plan mensual general: $500 MXN\n
       - Acceso ilimitado al gimnasio\n
       - Clases grupales incluidas\n\n
    2. Plan personalizado: $750 MXN\n
       - Entrenamiento individual\n
       - Seguimiento nutricional\n\n
    3. Clase individual: $100 MXN\n
       - Ideal para probar una sesión específica\n\n
    4. Promoción actual:\n
       - Inscríbete esta semana y recibe una clase personalizada gratis\n\n
    ¿Te gustaría agendar una clase de prueba o recibir más información?
    """


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

faq_dict = {
    "horario": "Nuestro horario es de lunes a viernes de 6:00 a.m. a 10:00 p.m., y sábados de 8:00 a.m. a 4:00 p.m.",
    "precio": "La mensualidad general es de $500 MXN. También contamos con paquetes personalizados.",
    "clases": "Ofrecemos funcional, spinning, yoga, box y entrenamiento personalizado.",
    "ubicación": "Estamos en Av. Reforma #123, San Luis Potosí.",
    "inscripción": "Solo necesitas una identificación y llenar un formulario. También puedes iniciar por WhatsApp.",
    "higiene": "Sí, seguimos protocolos de limpieza y desinfección constantes."
}