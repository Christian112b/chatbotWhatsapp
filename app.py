from dotenv import load_dotenv
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

from functions.textValidations import *

import os

load_dotenv()
app = Flask(__name__)



@app.route("/whatsapp", methods=['POST'])
def whatsapp_webhook():
    incoming_msg = request.values.get('Body', '').strip()
    sender = request.values.get('From')
    
    resp = MessagingResponse()
    msg = resp.message()

    msg.body(clasificacion_mensaje(incoming_msg))

    return Response(str(resp), mimetype="application/xml", status=200)

if __name__ == "__main__":
    app.run(debug=True)

    