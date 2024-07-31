import requests
import re


def send_message(sender: dict, message):
    print(f"Sending message to {sender}: {message}")
    print(type)
    headers = {"apikey": "e6h1w5721u9ydnuvm7eyck", "Content-Type": "application/json"}
    url = "https://evolution.programadornoob.io/message/sendText/Elyas"
    phone_number = "".join(re.findall(r"\d", sender.get("remoteJid")))

    payload = {
        "number": f"+{phone_number}",
        "options": {
            "delay": 123,
            "presence": "composing",
            "linkPreview": False,
            # "quoted": {
            #     "key": {
            #         "remoteJid": "557998480537@s.whatsapp.net",
            #         "fromMe": True,
            #         "id": sender.get("id"),
            #         "participant": "Elyas",
            #     },
            #     "message": {"conversation": message},
            # },
            "mentions": {"everyOne": False, "mentioned": [phone_number]},
        },
        "textMessage": {"text": message},
    }

    response = requests.request("POST", url, json=payload, headers=headers)
    return response
