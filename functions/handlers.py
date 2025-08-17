from functions.sqlLite import * 

from twilio.twiml.messaging_response import MessagingResponse

db = dbClub()

def reiniciar_estado(user_id):
    resp = MessagingResponse()
    msg = resp.message()
    msg.body("Reiniciando Estado")
    db.limpiar_base()

    return msg