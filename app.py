from dotenv import load_dotenv
from flask import Flask, request, Response
from twilio.twiml.messaging_response import MessagingResponse

from functions.data import *
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
        msg.body(menu_bienvenida)
        usuarios_estado[user_id] = "esperando_en_menu"

    elif estado == "esperando_en_menu":
        mensaje, nuevo_estado = respuesta_menu_precio(incoming_msg) 
        msg.body(mensaje)
        usuarios_estado[user_id] = nuevo_estado
        
    elif estado == "menu_precios":
        mensaje, nuevo_estado = respuesta_confirmacion(incoming_msg)
        msg.body(mensaje)
        usuarios_estado[user_id] = nuevo_estado

    # elif estado == "menu_clase":
    #     mensaje, nuevo_estado = (None, "Inicio")  # Aquí deberías definir la lógica para el menú de clases
    #     msg.body(mensaje)
    #     usuarios_estado[user_id] = nuevo_estado

    # elif estado == "menu_inscripcion":
    #     mensaje, nuevo_estado = (None, "Inicio")  # Aquí deberías definir la lógica para el menú de clases
    #     msg.body(mensaje)
    #     usuarios_estado[user_id] = nuevo_estado
    
    else:
        msg.body("Reiniciando Estado")
        usuarios_estado[user_id] = "Inicio"
        msg2 = resp.message()
        msg2.body(menu_bienvenida)

    return Response(str(resp), mimetype="application/xml", status=200)

if __name__ == "__main__":
    app.run(debug=True)

    