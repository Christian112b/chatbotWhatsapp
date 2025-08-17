from functions.sqlLite import * 

from twilio.twiml.messaging_response import MessagingResponse


def reiniciar_estado(user_id):

    usuarios_estado[user_id] = {}

    usuarios_estado[user_id]["estado"] = "Inicio"
    usuarios_estado[user_id]["telefono"] = None
    usuarios_estado[user_id]["nombre"] = None
    usuarios_estado[user_id]["plan"] = None
    usuarios_estado[user_id]["inscrito"] = False

    msg = resp.message()
    msg.body("Reiniciando Estado")
    db.limpiar_base()

    return msg, usuarios_estado