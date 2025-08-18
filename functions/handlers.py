from functions.sqlLite import * 

from functions.data import *
from functions.validations import *
from functions.whapi import *

usuarios_estado = {}

def inicializar_estado(user_id):
    if user_id not in usuarios_estado:
        usuarios_estado[user_id] = {
            "estado": "Inicio",
            "nombre": None,
            "plan": None,
            "activo": False,
            "telefono": limpiar_telefono(user_id)
        }

def manejar_comando_reiniciar(user_id, incoming_msg, db):
    if incoming_msg.lower() == "reiniciar":
        usuarios_estado[user_id] = {"estado": "Inicio"}
        db.borrar_tabla()
        send_whapi_message(user_id, "Estado reiniciado. ¿Cómo puedo ayudarte hoy?")
        return True
    return False

def manejar_consulta(user_id, incoming_msg, userdata):
    if incoming_msg.lower() == "consulta":
        if userdata:
            mensaje = f"Nombre: {userdata['nombre']}, Plan: {userdata['plan']}, Inscrito: {userdata['duracion']}"
        else:
            mensaje = "No se encontró información con este número de teléfono"
        send_whapi_message(user_id, mensaje)
        usuarios_estado[user_id]["estado"] = "Inicio"
        return True
    return False

def manejar_usuario_inscrito(user_id, incoming_msg, userdata):
    estado_actual = usuarios_estado[user_id]["estado"]
    usuarios_estado[user_id]["nombre"] = userdata["nombre"]
    usuarios_estado[user_id]["plan"] = userdata["plan"]
    usuarios_estado[user_id]["activo"] = userdata["activo"]

    if userdata["activo"] == 1 and estado_actual == "Inicio":
        send_whapi_message(user_id, bienvenido_activo)
        usuarios_estado[user_id]["estado"] = "menu_inscrito"
    elif estado_actual == "menu_inscrito":
        send_whapi_message(user_id, f"Mensaje: {incoming_msg}")
    else:
        send_whapi_message(user_id, bienvenido_no_activo)
        usuarios_estado[user_id]["estado"] = "menu_no_inscrito"

def manejar_menu_no_inscrito(user_id, incoming_msg):
    opcion = validacion_menu_no_activo(incoming_msg)
    if opcion == "agendar_clase":
        send_whapi_message(user_id, "Para agendar una clase, visita nuestro sitio web o contáctanos al +52 123 456 7890.")
        usuarios_estado[user_id]["estado"] = "generando_clase"
    elif opcion == "info_precios":
        send_whapi_message(user_id, "Para más información sobre precios, visita nuestro sitio web o contáctanos.")
        usuarios_estado[user_id]["estado"] = "info_precios"
    elif opcion == "nueva_inscripcion":
        send_whapi_message(user_id, "Para iniciar una nueva inscripción, por favor ingresa tu nombre completo.")
        usuarios_estado[user_id]["estado"] = "validando_nombre"
    else:
        send_whapi_message(user_id, "Lo siento, no entendí tu opción. ¿Podrías reformularla?")

def manejar_validacion_nombre(user_id, incoming_msg):
    usuarios_estado[user_id]["nombre"] = incoming_msg
    usuarios_estado[user_id]["estado"] = "confirmando_nombre"
    send_whapi_message(user_id, f'Nombre recibido: {incoming_msg}. ¿Es correcto?\nEscribe "Sí" para continuar, o escribe tu nombre para reintentarlo.')

def manejar_confirmacion_nombre(user_id, incoming_msg):
    if incoming_msg.lower() in ["sí", "si"]:
        usuarios_estado[user_id]["estado"] = "validando_plan"
        send_whapi_message(user_id, f"¡Genial! Ahora elige el plan que deseas:\n\n" + "\n".join(planes))
    else:
        usuarios_estado[user_id]["nombre"] = incoming_msg
        usuarios_estado[user_id]["estado"] = "validando_nombre"
        send_whapi_message(user_id, f'Nombre recibido: {incoming_msg}. ¿Es correcto?\nEscribe "Continuar" para continuar, o escribe tu nombre para reintentarlo.')

def manejar_validacion_plan(user_id, incoming_msg):
    if incoming_msg in ["1", "2", "3"]:
        usuarios_estado[user_id]["plan"] = incoming_msg
        usuarios_estado[user_id]["estado"] = "validando_inscripcion"
        send_whapi_message(user_id, f"Has seleccionado el {planes[int(incoming_msg) - 1]}.")
        send_whapi_message(user_id, "Elige la duración de tu membresía:\n1. 1 mes\n2. 3 meses\n3. 6 meses\n4. 9 meses\n5. 12 meses")
    else:
        send_whapi_message(user_id, "Opción no válida. Por favor, selecciona un plan válido.")

def manejar_validacion_inscripcion(user_id, incoming_msg):
    duracion = incoming_msg
    plan = usuarios_estado[user_id]["plan"]
    total = calcular_total(plan, duracion)
    usuarios_estado[user_id]["duracion"] = duracion
    usuarios_estado[user_id]["total"] = total
    usuarios_estado[user_id]["estado"] = "confirmando_inscripcion"
    send_whapi_message(user_id, f"Nombre: {usuarios_estado[user_id]['nombre']}\nPlan: {planes[int(plan) - 1]}\nDuración: {duracion}, Total: {total}")
    send_whapi_message(user_id, "Por favor, confirma tu inscripción respondiendo 'sí' o 'no'.")

def manejar_confirmacion_inscripcion(user_id, incoming_msg, db):
    if incoming_msg.lower() in ["sí", "si"]:
        db.guardar_inscripcion(usuarios_estado[user_id])
        send_whapi_message(user_id, "¡Genial! Listo, ahora eres parte de nuestra comunidad.")
        usuarios_estado[user_id]["estado"] = "Inicio"
    else:
        usuarios_estado[user_id] = {"estado": "Inicio"}
        send_whapi_message(user_id, "Inscripción cancelada. ¿Cómo puedo ayudarte hoy?")

def procesar_mensaje_whatsapp(user_id, incoming_msg):    
    db = dbClub()
    inicializar_estado(user_id)

    telefono = usuarios_estado[user_id]["telefono"]
    userdata = db.buscar_inscripcion(telefono)

    if incoming_msg.lower() == "reinicio":
        usuarios_estado[user_id] = {
            "estado": "Inicio",
            "nombre": None,
            "plan": None,
            "activo": False,
            "telefono": limpiar_telefono(user_id)
        }
        send_whapi_message(user_id, "✅ Estado reiniciado. ¿Cómo puedo ayudarte hoy?")
        return  

    if incoming_msg.lower() == "estado":
        estado = usuarios_estado.get(user_id, {}).get("estado", "Sin estado")
        nombre = usuarios_estado.get(user_id, {}).get("nombre", "No definido")
        plan = usuarios_estado.get(user_id, {}).get("plan", "No definido")
        activo = usuarios_estado.get(user_id, {}).get("activo", "No definido")

        mensaje = f"📍 Estado actual:\n- Estado: {estado}\n- Nombre: {nombre}\n- Plan: {plan}\n- Activo: {activo}"
        send_whapi_message(user_id, mensaje)
        return  

    if manejar_comando_reiniciar(user_id, incoming_msg, db): return
    if manejar_consulta(user_id, incoming_msg, userdata): return

    estado = usuarios_estado[user_id]["estado"]
    print("Estado para depurar: ", estado)

    if userdata:
        manejar_usuario_inscrito(user_id, incoming_msg, userdata)
    elif estado == "Inicio":
        send_whapi_message(user_id, menu_bienvenida)
        usuarios_estado[user_id]["estado"] = "menu_no_inscrito"
    elif estado == "menu_no_inscrito":
        manejar_menu_no_inscrito(user_id, incoming_msg)
    elif estado == "validando_nombre":
        manejar_validacion_nombre(user_id, incoming_msg)
    elif estado == "confirmando_nombre":
        manejar_confirmacion_nombre(user_id, incoming_msg)
    elif estado == "validando_plan":
        manejar_validacion_plan(user_id, incoming_msg)
    elif estado == "validando_inscripcion":
        manejar_validacion_inscripcion(user_id, incoming_msg)
    elif estado == "confirmando_inscripcion":
        manejar_confirmacion_inscripcion(user_id, incoming_msg, db)
