from dotenv import load_dotenv
from flask import Flask, request, Response
from twilio.twiml.messaging_response import MessagingResponse

from functions.data import *
from functions.validations import *

load_dotenv()
app = Flask(__name__)

# Diccionario para almacenar el estado de cada usuario
usuarios_estado = {}
"""
    usuarios_estados = {
        user_id: {
            estado: "Inicio",
            Telefono: "123-456",
            Nombre: "Nombre",
            Plan: "Plan de club",
            Inscrito: False
        }
    }
"""




@app.route("/webhook", methods=['POST'])
def whatsapp_webhook():
    incoming_msg = request.values.get('Body', '').strip()
    user_id = request.values.get('From', '')

    if user_id not in usuarios_estado:
        usuarios_estado[user_id] = {"estado": "Inicio", "Nombre": None, "Plan": None, "Inscrito": False}
    
    estado = usuarios_estado[user_id]["estado"]
    usuarios_estado[user_id]["Telefono"] = limpiar_telefono(user_id)

    resp = MessagingResponse()

    if usuarios_estado[user_id]["Inscrito"] is False:
        if estado == "Inicio":
            msg = resp.message()
            msg.body(menu_bienvenida)
            usuarios_estado[user_id] = "esperando_en_menu"

        elif estado == "esperando_en_menu":
            mensaje, nuevo_estado = respuesta_menu_precio(incoming_msg)
            msg = resp.message()
            msg.body(mensaje)
            usuarios_estado[user_id]["estado"] = nuevo_estado

        elif estado == "menu_precios":
            mensaje, nuevo_estado = respuesta_confirmacion(incoming_msg)
            msg = resp.message()
            msg.body(mensaje)
            usuarios_estado[user_id]["estado"] = nuevo_estado

        elif estado == "menu_inscripcion":
            mensaje, nuevo_estado, num_plan = seleccion_plan(incoming_msg)
            msg = resp.message()
            msg.body(mensaje)
            usuarios_estado[user_id]["estado"] = nuevo_estado
            usuarios_estado[user_id]["Plan"] = num_plan

        elif estado == "confirmacion":
            plan = usuarios_estado[user_id]["Plan"]
            mensaje, nuevo_estado = confirmacion(mensaje, plan)

        elif estado == "esperando_confirmacion":
            mensaje, nuevo_estado = esperando_confirmacion(incoming_msg)
            msg = resp.message()
            msg.body(mensaje)
            usuarios_estado[user_id]["estado"] = nuevo_estado

        else:
            msg = resp.message()
            msg.body("Reiniciando Estado")
            usuarios_estado[user_id]["estado"] = "Inicio"
            msg2 = resp.message()
            msg2.body(menu_bienvenida)

    else:
        msg = resp.message()
        msg.body("Reiniciando Estado con usuario inscrito")
        usuarios_estado[user_id]["estado"] = "Inicio"
        msg2 = resp.message()
        msg2.body(menu_bienvenida)

    return Response(str(resp), mimetype="application/xml", status=200)


if __name__ == "__main__":
    app.run(debug=True)

    