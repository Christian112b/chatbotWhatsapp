import requests
import os
import re

def send_whapi_message(to, message):
    to_clean = clean_whatsapp_id(to)
    
    if not is_valid_whapi_number(to_clean):
        print(f"[ERROR] Número inválido: {to_clean}")
        return 400, "Número inválido"
    
    WHAPI_URL = "https://gate.whapi.cloud/messages/text"

    HEADERS = {
        "Authorization": f"Bearer {os.environ.get('WHAPI_TOKEN')}",
        "Content-Type": "application/json"
    }

    payload = {
        "to": to_clean,
        "body": message
    }

    response = requests.post(WHAPI_URL, json=payload, headers=HEADERS)
    
    return response.status_code, response.text

def clean_whatsapp_id(raw_id):
    # Convierte "5214444014781@s.whatsapp.net" → "5214444014781"
    return raw_id.split('@')[0] if '@' in raw_id else raw_id

def is_valid_whapi_number(number):
    return re.match(r"^\d{9,15}$", number) is not None