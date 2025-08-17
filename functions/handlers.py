from functions.sqlLite import * 

from twilio.twiml.messaging_response import MessagingResponse


def reiniciar_estado(user_id):

    msg = resp.message()
    msg.body("Reiniciando Estado")
    db.limpiar_base()

    return msg, usuarios_estado