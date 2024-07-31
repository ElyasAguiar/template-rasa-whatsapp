import ast
import logging
from rasa.core.channels.channel import (
    InputChannel,
    UserMessage,
    CollectingOutputChannel,
)
from sanic import Blueprint, response
from typing import Awaitable, Text, Any, Callable

from services.evolution_api import send_message


logger = logging.getLogger(__name__)


class CustomWhatsAppInput(InputChannel):
    @classmethod
    def name(cls) -> Text:
        return "custom_whatsapp"

    def blueprint(
        self, on_new_message: Callable[[UserMessage], Awaitable[None]]
    ) -> Blueprint:
        custom_webhook = Blueprint("custom_webhook", __name__)

        @custom_webhook.route("/", methods=["GET"])
        async def health(request):
            return response.json({"status": "ok"})

        @custom_webhook.route("/webhook", methods=["POST"])
        async def receive(request):
            payload = request.json
            data = payload.get("data")
            sender = data.get("key")
            message = data.get("message")

            if not sender.get("fromMe") and message:
                await on_new_message(
                    UserMessage(
                        message.get("conversation"),
                        CustomOutputChannel(),
                        sender,
                    )
                )

            return response.text(f"Message received {sender}")

        return custom_webhook


class CustomOutputChannel(CollectingOutputChannel):
    @classmethod
    def name(cls) -> Text:
        return "custom_output_channel"

    async def send_text_message(
        self, recipient: Text, text: Text, **kwargs: Any
    ) -> None:
        # Aqui você implementa a lógica para enviar uma mensagem para o WhatsApp
        # Isso pode incluir chamadas a APIs do WhatsApp, por exemplo
        logger.info(f"Sending message to {recipient}: {text}", recipient)
        sender = ast.literal_eval(recipient)
        send_message(sender, text)
