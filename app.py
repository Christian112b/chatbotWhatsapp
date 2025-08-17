from dotenv import load_dotenv
from flask import Flask, request, Response
from twilio.twiml.messaging_response import MessagingResponse

from functions.data import *
from functions.handlers import *
from functions.validations import *
from functions.sqlLite import dbClub

load_dotenv()
app = Flask(__name__)

# Diccionario para almacenar el estado de cada usuario
usuarios_estado = {}
"""
    usuarios_estados = {
        user_id: {
            estado: "Inicio",
            telefono: "123-456",
            nombre: "Nombre",
            plan: "Plan de club",
            inscrito: False
        }
    }
"""

@app.route("/webhook", methods=['POST'])
def whatsapp_webhook():
    incoming_msg = request.values.get('Body', '').strip()
    user_id = request.values.get('From', '')

    global usuarios_estado

    if user_id not in usuarios_estado:
        usuarios_estado[user_id] = {"estado": "Inicio", "nombre": None, "plan": None, "activo": False}
    
    estado = usuarios_estado[user_id]["estado"]
    usuarios_estado[user_id]["telefono"] = limpiar_telefono(user_id)

    resp = MessagingResponse()

    # SQLObject
    db = dbClub()
    userdata = db.buscar_inscripcion(usuarios_estado[user_id]["telefono"])    

    # Opciones para gente ya inscrita
    if userdata is not None:
        usuarios_estado[user_id]["nombre"] = userdata["nombre"]
        usuarios_estado[user_id]["plan"] = userdata["plan"]
        usuarios_estado[user_id]["activo"] = userdata["activo"]

        # Opciones para gente ya inscrita y activa
        if usuarios_estado[user_id]["activo"] == 1 and usuarios_estado[user_id]["estado"] != "menu_inscrito":
            msg = resp.message()
            msg.body(bienvenido_activo) # Bienvenido a usuario activo
            usuarios_estado[user_id]["estado"] = "menu_inscrito"

        elif usuarios_estado[user_id]["activo"] == 1 and usuarios_estado[user_id]["estado"] == "menu_inscrito":
            msg = resp.message()
            msg.body(f"Mensaje: {incoming_msg}")






        # Opciones para gente ya inscrita y NO activa
        else:
            msg = resp.message()
            msg.body(bienvenido_no_activo)
            usuarios_estado[user_id]["estado"] = "menu_no_inscrito"

    # Opciones para gente no inscrita
    elif userdata is None and usuarios_estado[user_id]["estado"] == "Inicio":
        msg = resp.message()
        msg.body(menu_bienvenida)
        usuarios_estado[user_id]["estado"] = "menu_no_inscrito"

    
    # DEV USE --------------------------------- BORRAR DESPUES DE PRUEBAS
    elif incoming_msg.lower() == "consulta" or usuarios_estado[user_id]["estado"] == "prueba":
        test = db.buscar_inscripcion(usuarios_estado[user_id]["telefono"])
        if test:
            msg = resp.message()
            msg.body(f"Nombre: {test['nombre']}, Plan: {test['plan']}, Inscrito: {test['activo']}")
        else:
            msg = resp.message()
            msg.body("No se encontró información con este numero de telefono")

        usuarios_estado[user_id]["estado"] = "Inicio"
    # ----------------------------------------- BORRAR DESPUES DE PRUEBAS



    # Opciones para gente no inscrita y en estado de menu_no_inscrito
    elif userdata is None and usuarios_estado[user_id]["estado"] == "menu_no_inscrito":
        opcion = validacion_menu_no_activo(incoming_msg)

        # Opciones de menu para usuarios no inscritos -------------------------------------------

        # Opcion de agendar clase
        if opcion == "agendar_clase":
            msg = resp.message()
            msg.body("Para agendar una clase, por favor visita nuestro sitio web o contáctanos directamente al número +52 123 456 7890. ¡Te esperamos!")
            usuarios_estado[user_id]["estado"] = "generando_clase"

        # Opcion para informacion de precios y planes
        elif opcion == "info_precios":
            msg = resp.message()
            msg.body("Para más información sobre nuestros precios y promociones, por favor visita nuestro sitio web o contáctanos directamente al número +52 123 456 7890. ¡Estamos aquí para ayudarte!")
            usuarios_estado[user_id]["estado"] = "info_precios"

        # Opcion para nueva inscripcion, formulario para crear usuario
        elif opcion == "nueva_inscripcion":
            msg = resp.message()
            msg.body("Para iniciar una nueva inscripción, por favor ingresa tu nombre completo.")
            usuarios_estado[user_id]["estado"] = "validando_nombre"

        # Opcion si no se encuentra la keyword
        else:
            msg = resp.message()
            msg.body("Lo siento, no entendí tu opcion. ¿Podrías reformularla?")


    elif usuarios_estado[user_id]["estado"] == "validando_nombre":
        msg = resp.message()
        nombre = incoming_msg

        mensaje = f'Nombre recibido: {nombre}. ¿Es correcto?\nEscribe "Sí" para continuar, o escribe tu nombre para reintentarlo.'
        msg.body(mensaje)
        
        usuarios_estado[user_id]["nombre"] = incoming_msg
        usuarios_estado[user_id]["estado"] = "confirmando_nombre"

    elif usuarios_estado[user_id]["estado"] == "confirmando_nombre":
        if incoming_msg.lower() == "sí" or incoming_msg.lower() == "si":
            msg = resp.message()
            msg.body(f"¡Genial! Ahora elige el plan que deseas:\n\n" + "\n".join(planes) + "\n\nResponde con el número del plan que prefieras.")

            usuarios_estado[user_id]["estado"] = "validando_plan"
        else:
            msg = resp.message()
            mensaje = f'Nombre recibido: {incoming_msg}. ¿Es correcto?\nEscribe "Continuar" para continuar, o escribe tu nombre para reintentarlo.'
            usuarios_estado[user_id]["nombre"] = incoming_msg
            usuarios_estado[user_id]["estado"] = "confirmando_nombre"

            
        
    elif usuarios_estado[user_id]["estado"] == "validando_plan":
        plan_seleccionado = incoming_msg
        if plan_seleccionado in ["1", "2", "3"]:
            msg = resp.message()
            msg2 = resp.message()   
            msg.body(f"Has seleccionado el {planes[int(plan_seleccionado) - 1 ]}.")
            msg2.body("Por favor, elige la duración de tu membresía:\n1. 1 mes\n2. 3 meses\n3. 6 meses\n4. 9 meses\n5. 12 meses\n\nResponde con el número de la opción que prefieras.")

            usuarios_estado[user_id]["plan"] = plan_seleccionado
            usuarios_estado[user_id]["estado"] = "validando_inscripcion"
        else:
            msg = resp.message()
            msg.body("Opción no válida. Por favor, selecciona un plan válido.")
            usuarios_estado[user_id]["estado"] = "validando_plan"

    elif usuarios_estado[user_id]["estado"] == "validando_inscripcion":
        plan_seleccionado = usuarios_estado[user_id]["plan"]
        duracion = incoming_msg
        total = calcular_total(plan_seleccionado, duracion)

        msg = resp.message()
        msg.body(f"Nombre: {usuarios_estado[user_id]['nombre']}\nPlan: {planes[int(plan_seleccionado) - 1 ]}\nDuración: {duracion}, Total: {total}")
        msg2 = resp.message()
        msg2.body("Por favor, confirma tu inscripción respondiendo 'sí' o 'no'.")
        usuarios_estado[user_id]["estado"] = "confirmando_inscripcion"
        usuarios_estado[user_id]["duracion"] = duracion
        usuarios_estado[user_id]["total"] = total

    elif usuarios_estado[user_id]["estado"] == "confirmando_inscripcion":
        if incoming_msg.lower() == "sí" or incoming_msg.lower() == "si":

            # Guardar la inscripción en la base de datos
            db.guardar_inscripcion(usuarios_estado[user_id])

            msg = resp.message()
            msg.body("¡Genial!. Listo, ahora eres parte de nuestra comunidad!")

            usuarios_estado[user_id]["estado"] = "prueba"
        else:
            usuarios_estado[user_id] = {}
            usuarios_estado[user_id]["estado"] = "Inicio"

        # ----------------------------------------------------------------------------------------







    # # DEV USE
    # if incoming_msg.lower() == "reiniciar":
    #     usuarios_estado.pop(user_id, None)
    #     msg = reiniciar_estado(user_id)
    
    # elif incoming_msg.lower() == "consulta":
    #     test = db.buscar_inscripcion(usuarios_estado[user_id]["telefono"])
    #     if test:
    #         msg = resp.message()
    #         msg.body(f"Nombre: {test['nombre']}, Plan: {test['plan']}, Inscrito: {test['activo']}")
    #     else:
    #         msg = resp.message()
    #         msg.body("No se encontró información con este numero de telefono")

    # #--------------------------

    # elif usuarios_estado[user_id]["inscrito"]:
    #     msg = resp.message()
    #     msg.body("Bienvenido de nuevo al club!")
    #     usuarios_estado[user_id]["estado"] = "inicio_inscrito"

    # elif usuarios_estado[user_id]["inscrito"] is False:
    #     if estado == "Inicio":
    #         msg = resp.message()
    #         msg.body(menu_bienvenida)
    #         usuarios_estado[user_id]["estado"] = "esperando_en_menu"

    #     elif estado == "esperando_en_menu":
    #         mensaje, nuevo_estado = respuesta_menu_precio(incoming_msg)
    #         msg = resp.message()
    #         msg.body(mensaje)
    #         usuarios_estado[user_id]["estado"] = nuevo_estado

    #     elif estado == "menu_precios":
    #         mensaje, nuevo_estado = respuesta_confirmacion(incoming_msg)
    #         msg = resp.message()
    #         msg.body(mensaje)
    #         usuarios_estado[user_id]["estado"] = nuevo_estado

    #     elif estado == "menu_inscripcion":
    #         mensaje, nuevo_estado, num_plan = seleccion_plan(incoming_msg)
    #         msg = resp.message()
    #         msg.body(mensaje)
    #         usuarios_estado[user_id]["estado"] = nuevo_estado
    #         usuarios_estado[user_id]["plan"] = num_plan

    #     elif estado == "confirmacion":
    #         plan = usuarios_estado[user_id]["plan"]
    #         telefono = usuarios_estado[user_id]["telefono"]
    #         mensaje, nuevo_estado = confirmacion(incoming_msg, plan, telefono)
    #         msg = resp.message()
    #         msg.body(mensaje)

    #         usuarios_estado[user_id]["nombre"] = incoming_msg
    #         usuarios_estado[user_id]["estado"] = nuevo_estado

    #     elif estado == "esperando_confirmacion":
    #         mensaje, nuevo_estado = esperando_confirmacion(incoming_msg)
    #         msg = resp.message()
    #         msg.body(mensaje)
    #         usuarios_estado[user_id]["estado"] = nuevo_estado

    #         telefono = usuarios_estado[user_id]["telefono"]
    #         nombre = usuarios_estado[user_id]["nombre"]
    #         plan = usuarios_estado[user_id]["plan"]

    #         db.guardar_inscripcion(telefono, nombre, plan, True)

    # else:
    #     msg = resp.message()
    #     msg.body("Bienvenido de nuevo")
    #     usuarios_estado[user_id]["estado"] = "Inicio"
    #     msg2 = resp.message()
    #     msg2.body(menu_bienvenida)

    return Response(str(resp), mimetype="application/xml", status=200)


if __name__ == "__main__":
    app.run(debug=True)

    