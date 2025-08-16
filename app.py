from dotenv import load_dotenv
from flask import Flask, request, Response
from twilio.twiml.messaging_response import MessagingResponse

from functions.validations import *

load_dotenv()
app = Flask(__name__)

# Diccionario para almacenar el estado de cada usuario

usuarios_estado = {}


@app.route("/whatsapp", methods=['POST'])
def whatsapp_webhook():
    incoming_msg = request.values.get('Body', '').strip()
    user_id = request.values.get('From', '')
    estado = usuarios_estado.get(user_id, "Inicio")

    resp = MessagingResponse()
    msg = resp.message()

    if estado == "Inicio":
        msg.body(
            "Hola, bienvenido al Club Deportivo.\n"
            "¿Te interesa conocer precios, clases o inscribirte?"
        )
        usuarios_estado[user_id] = "esperando_en_menu"

    elif estado == "esperando_en_menu":
        response = respuesta_menu_precio(incoming_msg) 
        msg.body(response[0])
        if response[1] == "precios":
            usuarios_estado[user_id] = "menu_precios"
        else:
            usuarios_estado[user_id] = "esperando_en_menu"

    else:
        msg.body("Reiniciando Estado")
        usuarios_estado[user_id] = "Inicio"

    return Response(str(resp), mimetype="application/xml", status=200)

if __name__ == "__main__":
    app.run(debug=True)

    