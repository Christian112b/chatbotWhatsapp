import requests
import os

def send_whapi_message(to, message):
    url = "https://gate.whapi.cloud/messages"
    headers = {
        "Authorization": f"Bearer {os.environ.get('WHAPI_TOKEN')}",
        "Content-Type": "application/json"
    }
    payload = {
        "to": to.replace("whatsapp:", "").replace("+", ""),
        "text": message
    }

    response = requests.post(url, headers=headers, json=payload)
    print(f"[Whapi] Estado: {response.status_code} | Respuesta: {response.text}")
    
    return response.status_code, response.text