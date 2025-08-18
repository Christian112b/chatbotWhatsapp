import json

from dotenv import load_dotenv
from flask import Flask, request

from functions.handlers import *

load_dotenv()
app = Flask(__name__)

# Diccionario para almacenar el estado de cada usuario
usuarios_estado = {}

@app.route("/webhook", methods=["POST"])
def whatsapp_webhook():
    data = request.get_json()
    event_type = data.get("event", {}).get("type")

    if event_type != "messages":
        return "OK", 200

    message = data["messages"][0]

    # Ignorar mensajes enviados por el bot
    if message.get("from_me", False):
        return "OK", 200

    incoming_msg = message.get("text", {}).get("body", "")
    user_id = message.get("from")

    # Validar mensaje y número de usuario
    if not incoming_msg or not user_id:
        return "OK", 200

    print(f"[Webhook recibido] Mensaje: {incoming_msg} | De: {user_id}")
    procesar_mensaje_whatsapp(user_id, incoming_msg)
    return "OK", 200

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        agregar_pregunta(request.form['pregunta'], request.form['respuesta'])
        return redirect('/')
    preguntas = obtener_preguntas()
    return render_template('index.html', preguntas=preguntas)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

    