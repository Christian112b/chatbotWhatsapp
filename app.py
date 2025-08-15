from dotenv import load_dotenv
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

import os

load_dotenv()
app = Flask(__name__)

@app.route("/whatsapp", methods=['POST'])
def whatsapp_webhook():
    incoming_msg = request.values.get('Body', '').strip()
    sender = request.values.get('From')
    
    resp = MessagingResponse()
    msg = resp.message()

    if incoming_msg.lower() == 'hola':
        msg.body("¡Hola! ¿Cómo puedo ayudarte hoy?")
    elif incoming_msg.lower() == 'adiós':
        msg.body("¡Adiós! Que tengas un buen día.")
    else:
        msg.body("Lo siento, no entendí tu mensaje. Por favor, escribe 'hola' o 'adiós'.")

    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)