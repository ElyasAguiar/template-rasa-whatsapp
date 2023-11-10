# import requests
#
# url = "https://evolutionapi.elyasaguiar.com.br/message/sendText/aguiardev"
# api_key = "30599B41-98EF-4CF2-808B-6CB9608D4956"
# payload = {
#     "number": "5579998480537",
#     "options": {
#         "delay": 1200,
#         "presence": "composing",
#         "linkPreview": False,
#     },
#     "textMessage": {"text": "Olá thio!!"},
# }
#
# message = requests.post(
#     url=url,
#     headers={"Content-Type": "application/json", "apikey": api_key},
#     json=payload,
# )


class WhatsAppOutput(OutputChannel):
    """Output channel for WhatsApp."""

    @classmethod
    def name(cls) -> Text:
        return "whatsappio"

    def __init__(
        self,
        whatsapp_number: Optional[Text],
        api_key: Optional[Text],
        remoteJid: Optional[Text],
    ) -> None:
        self.whatsapp_number = whatsapp_number
        self.api_key = api_key
        self.send_retry = 0
        self.max_retry = 5
        self.remote_jid = remoteJid
        self.url = "http://evolutionapi.elyasaguiar.com.br/message/sendText/aguiardev"

    async def _send_message(self, message_data: Dict[Text, Any]) -> Dict:
        message = None
        try:
            while not message and self.send_retry < self.max_retry:
                message = requests.post(
                    url=self.url,
                    headers={"apikey": self.api_key},
                    json=message_data,
                )
                logger.info("Response", message)
                self.send_retry += 1
        except Exception as e:
            logger.error("Something went wrong " + repr(e))
        finally:
            self.send_retry = 0

        if not message and self.send_retry == self.max_retry:
            logger.error("Failed to send message. Max number of retires exceeded.")

        return json.dumps(message)

    async def send_text_message(
        self, recipient_id: Text, text: Text, **kwargs: Any
    ) -> None:
        """Sends text message."""
        message_data = {
            "number": f"{self.remote_jid}",
            "options": {"delay": 1200, "presence": "composing", "linkPreview": False},
            "textMessage": {"text": "Olá thio!!"},
        }

        await self._send_message(message_data)
